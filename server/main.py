#!/usr/bin/python3

import log
import time 
import mqtt 
import broker
import httpd

# py -m pip install paho-mqtt


logger = log.create_logger(__name__)

def main():
    logger.debug('CML server starting...')

    command_broker = broker.Broker()

    client = mqtt.MqttClient(command_broker)
    client.init()

    command_broker.init_commands(client)
    command_broker.describe_commands()

    httpd.start_httpd(command_broker)

    try:
        while True:
            #print("Tick")
            #tick()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.debug("Breaking the loop on ctrl+c")

    logger.info('Cleanup...')
    client.cleanup()


main()
logger.info('Exit')
