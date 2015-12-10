from rpitc.io import IO
from collections import Iterable

class Switch(object):

    def __init__(self, out, status=IO.OFF):
        if isinstance(out, Iterable):
            self.out = out
        else:
            self.out = [out]
        self.status = status

    def on(self):
        if self.status==IO.OFF:
            self.status = IO.ON
            self._trigger()

    def off(self):
        if self.status==IO.ON:
            self.status = IO.OFF
            self._trigger()

    def toggle(self):
        if self.status==IO.OFF:
            self.on()
        else:
            self.off()

    def _trigger(self):
        for out in self.out:
            out.toggle()
