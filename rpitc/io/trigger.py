from rpitc.io import IO
from rpitc.io.out import Out
import threading
import time

class Trigger(Out):

    def __init__(self, pin, status=IO.OFF, delay=0.2):
        Out.__init__(self, pin)
        self.delay = delay

    def trigger(self):
        thread = TriggerThread(self)
        thread.start()


class TriggerThread(threading.Thread):

    def __init__(self, trigger):
        threading.Thread.__init__(self)
        self.trigger = trigger

    def run(self):
        self.trigger.toggle()
        time.sleep(self.trigger.delay)
        self.trigger.toggle()

