import env
import uasyncio as asyncio
from machine import Pin

p_beep = Pin(env.PIN_NO_BEEP, Pin.OUT)
p_beep.off()

async def do_beep(objPin, num_of, time_on, time_off):
  for _ in range(num_of):
    objPin.on()
    await asyncio.sleep_ms(time_on)
    objPin.off()
    await asyncio.sleep_ms(time_off)

def beep(num_of = 1, time_on = 2, time_off = 100):
    loop = asyncio.get_event_loop()
    loop.create_task(do_beep(p_beep, num_of, time_on, time_off))