import uasyncio as asyncio
from machine import ADC
from cmllog import logger
import env
from machine import Pin

class BatService:
    def __init__(self, mqtt_service):
        self.mqtt_service = mqtt_service
        self.adc = ADC(Pin(env.PIN_NO_BAT))
        self.adc.atten(ADC.ATTN_11DB)
        voltage = self.adc.read()
        logger.debug("BatService alieve with voltage " + str(voltage))
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.watcher())

    async def watcher(self):
        while True:
            await asyncio.sleep(env.BAT_REPORT_SEC)
            voltage = self.adc.read()
            #await logger.adebug("BatService battery voltage " + str(voltage))
            #message = f'{{"data":{{"battery":{voltage}}}}}'
            await self.mqtt_service.publish(env.BAT_TOPIC, str(voltage))