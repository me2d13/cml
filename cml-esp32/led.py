import env
from machine import Pin, PWM
import micropython
import uasyncio as asyncio
import asyn

class LedService:
    def __init__(self):
        self.p_red = Pin(env.PIN_NO_RED, Pin.OUT)
        self.p_green = Pin(env.PIN_NO_GREEN, Pin.OUT)
        self.p_blue = Pin(env.PIN_NO_BLUE, Pin.OUT)
        #p_red = PWM(Pin(env.PIN_NO_RED, Pin.OUT), freq=1000)
        #p_green = PWM(Pin(env.PIN_NO_GREEN, Pin.OUT), freq=1000)
        #p_blue = PWM(Pin(env.PIN_NO_BLUE, Pin.OUT), freq=1000)
        self.red_value = 0
        self.green_value = 0
        self.blue_value = 0
        self.blinking_rep = 1
        self.blinking_rep_ms = 50
        self.blinking_on_ms = 100
        self.blinking_off_ms = 500
        self.isBlinking = False
        self.event = asyn.Event()
        loop = asyncio.get_event_loop()
        loop.create_task(self.blinking_watcher())


    def do_rgb(self, red, green, blue):
        self.p_red.value(1-red)
        self.p_green.value(1-green)
        self.p_blue.value(1-blue)
        #self.p_red.duty(1023-red)
        #self.p_green.duty(1023-green)
        #self.p_blue.duty(1023-blue)

    def off(self):
        self.do_rgb(0, 0, 0)

    async def blick(self, red, green, blue, num_of = 1):
        for i in range(num_of):
            self.do_rgb(red, green, blue)
            await asyncio.sleep_ms(50)
            self.off()
            await asyncio.sleep_ms(500)

    def set_rgb(self, r, g, b):
        self.red_value = r
        self.green_value = g
        self.blue_value = b

    # blinking is (repetition x [ON for on_ms, OFF for between_rep_ms]) OFF for off_ms
    def start_blinking(self, repetition = 1, on_ms = 100, off_ms = 500, between_rep_ms = 100):
        self.blinking_on_ms = on_ms
        self.blinking_off_ms = off_ms
        self.blinking_rep = repetition
        self.blinking_rep_ms = between_rep_ms
        if not self.event.is_set():
            self.isBlinking = True
            self.event.set()

    def stop_blinking(self):
        self.isBlinking = False

    async def blinking_watcher(self):
        while True:
            await self.event
            while self.isBlinking:
                for i in range(self.blinking_rep):
                    self.do_rgb(self.red_value, self.green_value, self.blue_value)
                    await asyncio.sleep_ms(self.blinking_on_ms)
                    self.off()
                    if i + 1 < self.blinking_rep:
                        await asyncio.sleep_ms(self.blinking_rep_ms)
                await asyncio.sleep_ms(self.blinking_off_ms)
            self.event.clear()

# testing

async def killer(ls):
    await asyncio.sleep(3)
    ls.set_rgb(0,0,1)
    ls.start_blinking()
    await asyncio.sleep(3)
    ls.stop_blinking()
    await asyncio.sleep(3)
    ls.set_rgb(1,0,0)
    ls.start_blinking(3) # tripple blink
    await asyncio.sleep(3)
    ls.stop_blinking()

def test():
    loop = asyncio.get_event_loop()
    ls = LedService()
    loop.create_task(ls.blick(0,1,0,2))
    loop.run_until_complete(killer(ls))  # Run for 10s

#test()
