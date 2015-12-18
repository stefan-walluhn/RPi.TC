from rpitc.io import IO
from rpitc.io.out import Out, BaseOut
from threading import Thread
import time

class Trigger(BaseOut):

    def __init__(self, out, status=IO.OFF, trigger_on=IO.ON, delay=0.2):
        self.out = out
        self.trigger_on = trigger_on
        self.delay = delay
        self._trigger_thread = Thread(target=self.trigger)
        super(Trigger, self).__init__(status)

    def _on(self):
        if self.status==IO.OFF and self.trigger_on==IO.ON:
            self._trigger_thread.start()
        return super(Trigger, self)._on()

    def _off(self):
        if self.status==IO.ON and self.trigger_on==IO.OFF:
            self._trigger_thread.start()
        return super(Trigger, self)._off()

    def trigger(self):
        self.out.toggle()
        time.sleep(self.delay)
        self.out.toggle()
