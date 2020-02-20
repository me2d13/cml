from .abstract_command import CmlAbstractCommand

class CmlCommand(CmlAbstractCommand):
    def describe(self):
        return 'vypnout pracovnu za 1 minutu'

    def run(self, interrupt_event):
        self.light_pct(47, 50)
        if interrupt_event.wait(timeout=60):
            return
        self.light_off(47)