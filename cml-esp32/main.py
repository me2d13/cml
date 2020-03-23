import env
#from umqttsimple import MQTTClient
from machine import Pin
import micropython
import network
import esp
esp.osdebug(None)
import gc
import uasyncio as asyncio
import led
import mqtt
import keypad

gc.collect()

p2 = Pin(2, Pin.OUT)

led_service = led.LedService()
mqtt_service = mqtt.MqttService()
keypad_service = keypad.KeypadService(led_service, mqtt_service)

async def connect():
  led_service.set_rgb(1,0,0)
  led_service.start_blinking(1, 200, 500)
  await mqtt_service.connect()
  led_service.stop_blinking()

async def killer():
    await asyncio.sleep(10)

loop = asyncio.get_event_loop()
loop.create_task(connect())
loop.run_until_complete(killer())  # Run for 10s
#loop.run_forever()
#loop.close()
