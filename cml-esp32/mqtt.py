from mqtt_as import config, MQTTClient
import env
import uasyncio as asyncio

config['server'] = env.MQTT_BROKER

config['ssid'] = env.WIFI_SSID
config['wifi_pw'] = env.WIFI_PASSWORD

class MqttService:
    def __init__(self):
        MQTTClient.DEBUG = True  # Optional: print diagnostic messages
        self.client = MQTTClient(config)
        print('MqttService: Client created')

    async def connect(self):
        print('MqttService: Going to connect')
        await self.client.connect()
        print('MqttService: Was connected')


    def callback(self, topic, msg, retained):
        print((topic, msg, retained))

    async def conn_han(self, client):
        print('MqttService: MQTT connected')
        #await client.subscribe('foo_topic', 1)

    async def publish(self, topic, msg):
        print('MqttService: publish to ' + topic)
        # If WiFi is down the following will pause for the duration.
        await self.client.publish(topic, msg, qos = 1)

    def close(self):
        self.client.close()  # Prevent LmacRxBlk:1 errors