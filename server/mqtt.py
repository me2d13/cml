import config
import log
import paho.mqtt.client as mqtt
import re
import traceback

logger = log.create_logger(__name__)

client = None

class MqttClient:
    def __init__(self, broker):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.broker = broker

    def init(self):
        self.topic_pattern = re.compile("{}/([0-9]+)".format(config.MQTT_ROOT), re.IGNORECASE)

        self.client.connect(config.MQTT_BROKER, 1883, 60)
        logger.info('Mqtt loop start...')
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        logger.debug("Mqtt connected with result code %s", rc)
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.subscribe()

    def on_message(self, client, userdata, msg):
        logger.debug("Got mqtt message topic %s, payload %s", msg.topic, str(msg.payload))
        match = self.topic_pattern.match(msg.topic)
        if match:
            command = match.group(1)
            logger.debug("Recognized command %s", command)
            try:
                self.broker.on_command(command)
            except:
                traceback.print_exc()
        else:
            logger.warning("Unexpected topic {}, cannot be parsed".format(msg.topic))

    def publish(self, topic, payload):
        logger.debug("Publishing mqtt message topic %s, payload %s", topic, payload)
        self.client.publish(topic, payload)

    def subscribe(self):
        topic = config.MQTT_ROOT + '/#'
        logger.info("Subscribing to MQTT topic %s", topic)
        self.client.subscribe(topic)

    def cleanup(self):
        logger.info('Stopping mqtt loop...')
        self.client.loop_stop()



