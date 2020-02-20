from .abstract_command import CmlAbstractCommand

class CmlCommand(CmlAbstractCommand):
    def describe(self):
        return 'spani z pracovny'

    def run(self, interrupt_event):
        self.light_pct(47, 30) # pracovna
        self.light_pct(30, 20) # schody
        self.light_pct(41, 50) # KH
        if interrupt_event.wait(timeout=30):
            return
        self.light_off(47) # KH
        self.light_pct(20, 30) # KD
        if interrupt_event.wait(timeout=120):
            return
        self.light_pct(41, 20) # KH
        if interrupt_event.wait(timeout=200):
            return
        self.light_off(12) # LED kuchyn
        self.light_off(20) # KD
        if interrupt_event.wait(timeout=30):
            return
        self.light_off(41) # KH
        if interrupt_event.wait(timeout=30):
            return
        self.light_off(30) # schody
