import env
from machine import Pin, PWM
import micropython
import uasyncio as asyncio
import keypad_uasyncio
import beep

class KeypadService:
    def __init__(self, led_service, mqtt_service):
        self.led_service = led_service
        self.mqtt_service = mqtt_service
        self.keypad = keypad_uasyncio.Keypad_uasyncio()
        self.keypad.start()
        self.command = ''
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.keypad.scan_coro())
        self.loop.create_task(self.keypad_watcher())

    async def keypad_watcher(self):
        while True:
            key = await self.keypad.get_key()
            print("Got key:", key)
            if key == '*':
                beep.beep(1, 50)
                self.command = ''
            elif key == '#':
                print("Sending:", self.command)
                beep.beep(2)
                await self.mqtt_service.publish(env.MQTT_TOPIC + self.command, '')
                self.command = ''
            else:
                self.command = self.command + key
                beep.beep()
                print("Command:", self.command)


