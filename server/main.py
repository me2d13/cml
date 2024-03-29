#!/usr/bin/python3

import log
import time 
import mqtt 
import broker
import httpd

# py -m pip install paho-mqtt
# pip install cherrypy
# pip install PyJWT
# pip install pyjwt[crypto]
# pip install python-elastic-logstash


logger = log.create_logger(__name__)
es_logger = log.create_es_logger('CMLmain')

def main():
    logger.debug('CML server starting...')
    es_logger.info("CML server starting...")

    command_broker = broker.Broker()

    client = mqtt.MqttClient(command_broker)
    client.init()

    command_broker.init_commands(client)
    logger.info("\nAvailable commands:\n===================\n{}".format(command_broker.describe_commands()))

    httpd.start_httpd(command_broker, client)

    logger.info('Cleanup...')
    client.cleanup()


main()
logger.info('Exit')
