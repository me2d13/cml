import threading

class CmlAbstractCommand:
    def __init__(self, command_number):
        self.command_number = command_number
        #print('Created command {}'.format(command_number))

    def init(self, mqtt_client, logger, on_command_end):
        self.mqtt_client = mqtt_client
        self.logger = logger
        self.on_command_end = on_command_end
        self.logger.debug('Command %s initialized', self.command_number)

    def describe(self):
        return 'WARN: command {} is not providing any self-description'.format(self.command_number)

    def run(self, interrupt_event):
        self.logger.warn('Command {} is not providing any funcionality'.format(self.command_number))

    def run_wrapper(self, interrupt_event):
        self.run(interrupt_event)
        if self.on_command_end:
            self.on_command_end(self.command_number)

    def execute(self):
        interrupt_event = threading.Event()
        thread = threading.Thread(target=self.run_wrapper, args=(interrupt_event,), daemon=True)
        return (thread, interrupt_event)

    def light_on(self, dp_no):
        topic = '/xcfgw/lr/command/{}'.format(dp_no)
        payload = '{"event": 10, "data":1}'
        self.mqtt_client.publish(topic, payload)

    def light_off(self, dp_no):
        topic = '/xcfgw/lr/command/{}'.format(dp_no)
        payload = '{"event": 10, "data":0}'
        self.mqtt_client.publish(topic, payload)

    def light_pct(self, dp_no, percent):
        topic = '/xcfgw/lr/command/{}'.format(dp_no)
        payload = '{"event": 13, "data":64, "percent": %d}' % percent
        self.mqtt_client.publish(topic, payload)

JALO_DOWN = 0
JALO_UP = 1
JALO_STOP = 2

class JaloCommand(CmlAbstractCommand):
    def __init__(self, command_number, description, dp_no, jalo_command):
        super().__init__(command_number)
        self.description = description
        self.dp_no = dp_no
        self.jalo_command = jalo_command

    def describe(self):
        return self.description

    def run(self, interrupt_event):
        topic = '/xcfgw/lr/command/{}'.format(self.dp_no)
        payload = '{"event": 14, "data": %d}' % self.jalo_command
        self.logger.debug('Sending mqtt message topic %s payload %s', topic, payload)
        self.mqtt_client.publish(topic, payload)