from .abstract_command import CmlAbstractCommand

class CmlCommand(CmlAbstractCommand):
    def describe(self):
        return 'blik v pracovne 1 minuta'

    def run(self, interrupt_event):
        self.light_on(47)
        if interrupt_event.wait(timeout=60):
            return
        self.light_off(47)