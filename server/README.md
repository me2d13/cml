# Server
This is core component to enable numbered commands for home automation. See parent readme for details.

# Commands
Commands are defined as files in `commands` folder. E.g. 2.py for command number 2 etc. Command (the python file) needs to provide definition of class `CmlCommand` which needs to provide several methods. The easiest way is to use `CmlAbstractCommand` as parent class. Then command need to implement just 2 methods
* __describe__ which returns string describing what command does - including the number. For example: _2: switch off all lights_
* __run__ the code itself. The code will do actual work - publish mqtt message, sends http requests... whatever

# Delays
Commands can run for long time as they may cover some scenarios like _turn on light for 5 minutes, then switch it off_. So each command runs in dedicated thread to not block other commands. If command still runs and another request (for the same command) arrives, the execution is interrupted and new command is started.

How can Python interrupt running code? Only in delays and only if delays are implemented in specific way. `time.sleep()` would not work here. _Server_ code needs to request command's termination and it can't be done when process is sleeping. Because of that the `run` method provides Python event instance as argument and the command should use `event.wait(timeout=some_time_in_seconds)` to wait. When this call is over command's code should check the return value to check if wait stopped on timeout (and continue) or was interrupted from _server_ code to stop the execution. So typical wait for 1 minute would be
```python
        if interrupt_event.wait(timeout=60):
            return # was interrupted
```
See existing command for examples.

# Cancel all
With long delays you can easily get lost not being sure what's running and what light will be switched on or off. So there's built in command number __99__ which just terminates all running commands. However if you define your own file `99.py` it will be used instead of this built in behavior.