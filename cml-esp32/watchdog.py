import uasyncio as asyncio
import time
import beep
import machine
import env
from cmllog import logger


class Watchdog:
    def __init__(self, keypad_service, led_service):
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.watcher())
        self.last_activity_ms = time.ticks_ms()
        self.keypad_service = keypad_service
        self.led_service = led_service

    async def watcher(self):
        while True:
            now = time.ticks_ms()
            diff = time.ticks_diff(now, self.last_activity_ms)
            #print("Diff {}".format(time.ticks_diff(self.last_activity_ms, now)))
            if self.keypad_service.command and diff > env.CANCEL_COMMAND_SEC * 1000:
                self.keypad_service.clear_command()
            if diff > env.DEEP_SLEEP_SEC * 1000:
                print("Preparing deep sleep...")
                self.keypad_service.prepare_deep_sleep()
                self.led_service.prepare_deep_sleep()
                machine.Pin(env.PIN_NO_BEEP, machine.Pin.IN, machine.Pin.PULL_DOWN)
                await logger.adebug("Entering deep sleep...")
                print("Entering deep sleep...")
                machine.deepsleep()
            await asyncio.sleep(1)
            print("Tick " + str(diff/1000))

    def kick(self):
        self.last_activity_ms = time.ticks_ms()