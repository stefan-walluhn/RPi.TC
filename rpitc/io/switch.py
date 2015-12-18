from rpitc.io import IO, BaseOut
from collections import Iterable


class Switch(BaseOut):

    def __init__(self, out, status=IO.OFF):
        if isinstance(out, Iterable):
            self._out = out
        else:
            self._out = [out]
        super(Switch, self).__init__(status)

    def _on(self):
        if self.status==IO.OFF:
            self._toggle_all()
        return super(Switch, self)._on()

    def _off(self):
        if self.status==IO.ON:
            self._toggle_all()
        return super(Switch, self)._off()

    def _toggle_all(self):
        for out in self._out:
            out.toggle()
