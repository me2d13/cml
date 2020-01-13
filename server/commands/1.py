from .abstract_command import CmlAbstractCommand

class CmlCommand(CmlAbstractCommand):
    def describe(self):
        return '{}: blik v pracovne'.format(self.command_number)

    def run(self, interrupt_event):
        print('BLIK')
        if interrupt_event.wait(timeout=15):
            return
        print('UNBLIK')
        
