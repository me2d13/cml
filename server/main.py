#!/usr/bin/python3

import log
import time 
import mqtt 

# py -m pip install paho-mqtt


logger = log.create_logger(__name__)

def main():
    logger.debug('CML server starting...')

    client = mqtt.MqttClient()
    client.init()

    try:
        while True:
            #print("Tick")
            #tick()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Breaking the loop on ctrl+c")

    logger.info('Cleanup...')
    client.cleanup()


main()
logger.info('Exit')
