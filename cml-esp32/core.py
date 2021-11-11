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
import watchdog
import cmllog
import bat


gc.collect()
p2 = Pin(2, Pin.OUT)
led_service = led.LedService()
mqtt_service = mqtt.MqttService()
keypad_service = keypad.KeypadService(led_service, mqtt_service)
cmllog.logger.mqtt_service = mqtt_service

async def connect():
  connecting_blink = led_service.start_blinking(led.BlinkDef(1,0,0,1,200, 500, 50, 10))
  await mqtt_service.connect()
  led_service.stop_blinking(connecting_blink)
  cmllog.logger.debug("CML esp32 running")

async def killer():
  await asyncio.sleep(20)

async def heart_beat():
  for _ in range(10): # 10 blicks on start
    p2.on()
    await asyncio.sleep_ms(100)
    p2.off()
    await asyncio.sleep_ms(700)

def main():
  wd = watchdog.Watchdog(keypad_service, led_service)
  keypad_service.add_watchdog(wd)
  batteryService = bat.BatService(mqtt_service)

  loop = asyncio.get_event_loop()
  loop.create_task(connect())
  loop.create_task(heart_beat())
  loop.run_forever()

async def test():
  await mqtt_service.client.wifi_connect()
  try:
    import uftpd
    uftpd.start()
  except Exception:
    print('uftpd exception')
    raise