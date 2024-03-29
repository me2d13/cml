import env
from machine import Pin, PWM, reset
import esp32
import uasyncio as asyncio
import keypad_uasyncio
import beep
import led

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
        self.blinking_id = 0
        self.watchdog = None

    def clear_command(self):
        self.command = ''
        self.led_service.stop_blinking(self.blinking_id)
        self.blinking_id = 0

    def add_watchdog(self, watchdog):
        self.watchdog = watchdog

    async def keypad_watcher(self):
        while True:
            key = await self.keypad.get_key()
            #print("Got key:", key)
            if self.watchdog:
                self.watchdog.kick()
            if key == '*':
                beep.beep(1, 50)
                self.clear_command()
            elif key == '#':
                if self.command == '380':
                    print("Starting FTP server")
                    await self.mqtt_service.publish(env.LOG_TOPIC, 'Starting FTP server')
                    #await self.mqtt_service.client.disconnect()
                    import ftp
                    ftp.ftpserver()
                elif self.command == '73738':
                    print("Resetting...")
                    reset()
                else:
                    print("Sending:", self.command)
                    beep.beep(2)
                    await self.mqtt_service.publish(env.MQTT_TOPIC + self.command, '')
                self.clear_command()
            else:
                self.command = self.command + key
                beep.beep()
                print("Command:", self.command)
                b_def = led.BlinkDef(0,0,1,len(self.command),100,500,70,5)
                if self.blinking_id:
                    self.led_service.replace_blinking(self.blinking_id, b_def)
                else:
                    self.blinking_id = self.led_service.start_blinking(b_def)

    def prepare_deep_sleep(self):
        self.keypad.stop()
        for pin in env.KEYPAD_ROW_PINS:
            Pin(pin, mode=Pin.OUT, pull=Pin.PULL_HOLD)
        esp32.wake_on_ext1(pins = self.keypad.col_pins, level = esp32.WAKEUP_ANY_HIGH)
