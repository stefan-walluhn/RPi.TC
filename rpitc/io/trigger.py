from rpitc.io import IO
from rpitc.io.out import Out
import threading
import time

class Trigger(object):

    def __init__(self, out, status=IO.OFF, trigger_on=IO.ON, delay=0.2):
        self.out = out
        self.status = status
        self.trigger_on = trigger_on
        self.delay = delay

    def on(self):
        if self.status==IO.OFF and self.trigger_on==IO.ON:
            thread = TriggerThread(self)
            thread.start()
        self.status = IO.ON

    def off(self):
        if self.status==IO.ON and self.trigger_on==IO.OFF:
            thread = TriggerThread(self)
            thread.start()
        self.status = IO.OFF

    def toggle(self):
        if self.status==IO.ON:
            self.off()
        else:
            self.on()


class TriggerThread(threading.Thread):

    def __init__(self, trigger):
        threading.Thread.__init__(self)
        self.trigger = trigger

    def run(self):
        self.trigger.out.toggle()
        time.sleep(self.trigger.delay)
        self.trigger.out.toggle()

