import env
import uasyncio as asyncio

class CmlLogger:

    def __init__(self):
        self.mqtt_service = None

    def debug(self, message):
        print(message)
        if self.mqtt_service is not None:
            asyncio.run(self.mqtt_service.publish(env.LOG_TOPIC, message))

    async def adebug(self, message):
        print(message)
        if self.mqtt_service is not None:
            await self.mqtt_service.publish(env.LOG_TOPIC, message)


logger = CmlLogger()