import threading

class CmlAbstractCommand:
    def __init__(self, command_number):
        self.command_number = command_number
        #print('Created command {}'.format(command_number))

    def init(self, mqtt_client, logger, on_command_end):
        self.mqtt_client = mqtt_client
        self.logger = logger
        self.on_command_end = on_command_end
        self.logger.debug('Command %s initialized', self.command_number)

    def describe(self):
        return 'WARN: command {} is not providing any self-description'.format(self.command_number)

    def run(self, interrupt_event):
        self.logger.warn('Command {} is not providing any funcionality'.format(self.command_number))

    def run_wrapper(self, interrupt_event):
        self.run(interrupt_event)
        if self.on_command_end:
            self.on_command_end(self.command_number)

    def execute(self):
        interrupt_event = threading.Event()
        thread = threading.Thread(target=self.run_wrapper, args=(interrupt_event,), daemon=True)
        return (thread, interrupt_event)