import env
from machine import Pin, PWM
import micropython
import uasyncio as asyncio
import asyn
from ucollections import namedtuple

BlinkDef = namedtuple("BlinkDef", ("red", "green", "blue", "rep", "on_ms", "off_ms", "rep_ms", "priority"))

default_blink_def = BlinkDef(0,1,0,1,100, 500, 50, 1)

class LedService:
    """Class that can controls RGB LED. Can create ad hoc blicks or continuous blinking.
    Continuous blinking requests can overlap and have priorities. When higher prio blinking
    is stopped service will reuse blinking with lower prio which was not stopped yet"""

    def __init__(self):
        self.p_red = Pin(env.PIN_NO_RED, Pin.OUT)
        self.p_green = Pin(env.PIN_NO_GREEN, Pin.OUT)
        self.p_blue = Pin(env.PIN_NO_BLUE, Pin.OUT)
        self.off()
        #p_red = PWM(Pin(env.PIN_NO_RED, Pin.OUT), freq=1000)
        #p_green = PWM(Pin(env.PIN_NO_GREEN, Pin.OUT), freq=1000)
        #p_blue = PWM(Pin(env.PIN_NO_BLUE, Pin.OUT), freq=1000)
        self.blinking_defs = {}
        self.blinking_def_id_sequence = 1
        self.blinking_def_id = None
        self.event = asyn.Event()
        loop = asyncio.get_event_loop()
        loop.create_task(self.blinking_watcher())


    def do_rgb(self, red, green, blue):
        """Controls directly RGB pins so LED will shine after this call"""

        self.p_red.value(1-red)
        self.p_green.value(1-green)
        self.p_blue.value(1-blue)
        #self.p_red.duty(1023-red)
        #self.p_green.duty(1023-green)
        #self.p_blue.duty(1023-blue)

    def off(self):
        """Turns the LED off"""

        self.do_rgb(0, 0, 0)

    async def blick(self, red, green, blue, num_of = 1):
        """Ad hoc blick with defined RGB and number of repetitions. Delays are hardcoded. This is async coro"""

        for _ in range(num_of):
            self.do_rgb(red, green, blue)
            await asyncio.sleep_ms(50)
            self.off()
            await asyncio.sleep_ms(500)

    def start_blinking(self, blinking_def):
        """The interface method to start blinking. Just adds definition to internal list to support overlaps.
        Then calls decision routine. Returns id that is used to stop this blinking"""

        self.blinking_defs[self.blinking_def_id_sequence] = blinking_def
        self.blinking_def_id_sequence += 1
        self.pick_and_start_blinking()
        return self.blinking_def_id_sequence - 1

    def replace_blinking(self, blinking_id, blinking_def):
        """Change blinking definition for existing id"""

        self.blinking_defs[blinking_id] = blinking_def
        self.pick_and_start_blinking()
        return blinking_id

    def pick_and_start_blinking(self):
        """Internal method that finds blinking definition with the highest prio and set it as active.
        If there are no definitions it just switch the LED off"""

        highest_prio = 0
        highest_id = 0
        for id, b_def in self.blinking_defs.items():
            if b_def.priority > highest_prio:
                highest_prio = b_def.priority
                highest_id = id
        self.blinking_def_id = highest_id
        if highest_id:
            if not self.event.is_set():
                self.event.set()
        else:
            self.off()

    def stop_blinking(self, id):
        """Stops blinking by definition id, returned by start_blinking request"""

        self.blinking_defs.pop(id, {})
        self.pick_and_start_blinking()

    def prepare_deep_sleep(self):
        Pin(env.PIN_NO_RED, Pin.IN, Pin.PULL_UP)
        Pin(env.PIN_NO_GREEN, Pin.IN, Pin.PULL_UP)
        Pin(env.PIN_NO_BLUE, Pin.IN, Pin.PULL_UP)

    async def blinking_watcher(self):
        """The coro handling LED (turning on and off) for continuos blinking based on active definition"""

        while True:
            await self.event
            while self.blinking_def_id:
                # blinking is (repetition x [ON for on_ms, OFF for between_rep_ms]) OFF for off_ms
                b_def = self.blinking_defs[self.blinking_def_id]
                for i in range(b_def.rep):
                    self.do_rgb(b_def.red, b_def.green, b_def.blue)
                    await asyncio.sleep_ms(b_def.on_ms)
                    self.off()
                    if i + 1 < b_def.rep:
                        await asyncio.sleep_ms(b_def.rep_ms)
                await asyncio.sleep_ms(b_def.off_ms)
            self.event.clear()

# testing

async def killer(ls):
    await asyncio.sleep(3)
    # strat long red blinks, prio 2
    id1 = ls.start_blinking(BlinkDef(1,0,0,1,300, 500, 50, 2))
    await asyncio.sleep(1)
    # strat short blue double-blinks, but prio 1, so red stays active
    id2 = ls.start_blinking(BlinkDef(0,0,1,2,100, 500, 50, 1))
    await asyncio.sleep(4)
    # stop red with higher prio, so service revert to blue double-blicks
    ls.stop_blinking(id1)
    await asyncio.sleep(3)
    # stop blue doubles
    ls.stop_blinking(id2)

def test():
    loop = asyncio.get_event_loop()
    ls = LedService()
    # do adhoc blink, twice green
    loop.create_task(ls.blick(0,1,0,2))
    loop.run_until_complete(killer(ls))  # Run for 10s

#test()
