from mqtt_as import config, MQTTClient
import env
import uasyncio as asyncio


class MqttService:
    def __init__(self):
        MQTTClient.DEBUG = True  # Optional: print diagnostic messages
        config['server'] = env.MQTT_BROKER
        config['ssid'] = env.WIFI_SSID
        config['wifi_pw'] = env.WIFI_PASSWORD
        config['connect_coro'] = self.conn_han
        self.client = MQTTClient(config)
        self.pending_messages = []
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
        while len(self.pending_messages) > 0:
            topic, msg = self.pending_messages[0]
            print('MqttService: processing pending messages, sending topic ' + topic)
            await self.client.publish(topic, msg, qos = 1)
            self.pending_messages.pop(0)

    async def publish(self, topic, msg):
        if self.client.isconnected():
            print('MqttService: publish to ' + topic)
            # If WiFi is down the following will pause for the duration.
            await self.client.publish(topic, msg, qos = 1)
        else:
            print('MqttService: adding topic to pending messages ' + topic)
            self.pending_messages.append((topic, msg))


    def close(self):
        self.client.close()  # Prevent LmacRxBlk:1 errors