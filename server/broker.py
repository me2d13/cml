import threading
import config
import log
import commands

#print('In broker we have commands', commands.commands)
logger = log.create_logger(__name__)

class Broker:
    def __init__(self):
        self.thread_pool = {}

    def init_commands(self, mqtt_client):
        for key, command in commands.commands.items():
            command.init(mqtt_client, log.create_logger('command_{}'.format(key)), self.on_command_end)

    def describe_commands(self):
        logger.info('Available commands')
        logger.info('==================')
        for command in commands.commands.values():
            logger.info(command.describe())
        logger.info('99: cancel all running commands')
    
    def on_command_end(self, command_key):
        logger.debug('Command %s ended', command_key)
        del self.thread_pool[command_key]

    def on_command(self, command):
        logger.debug('Broker recevied command %s', command)
        exec_class = commands.commands.get(command)
        if exec_class:
            logger.debug('Executing command %s', command)
            current = self.thread_pool.get(command)
            if current != None:
                thread, event = current
                logger.debug('Command instance running in %s, cancelling...', thread.name)
                event.set()
                thread.join()
            thread, interrupt_event = exec_class.execute()
            self.thread_pool[command] = thread, interrupt_event
            if thread:
                thread.start()
        elif command == '99':
            for key, current in self.thread_pool.items():
                thread, event = current
                logger.debug('Cancelling command %s in thread %s', key, thread.name)
                event.set()
        else:
            logger.warn('Command %s not defined', command)
