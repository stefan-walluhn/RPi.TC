from rpitc.io import IO
from rpitc.io.trigger import Trigger
import time

class TestTrigger:

    def setup_method(self, method):
        self.trigger = Trigger(7, delay=1, status=IO.OFF)
        self.trigger2 = Trigger(5, status=IO.ON, trigger_on=IO.OFF)

    def teardown_method(self, method):
        self.trigger.out.off()
        self.trigger2.out.off()

    def test_init(self):
        assert isinstance(self.trigger, Trigger)

    def test_trigger_on(self):
        self.trigger.off()
        self.trigger.on()
        assert self.trigger.status == IO.ON
        assert self.trigger.out.status == IO.ON
        time.sleep(self.trigger.delay + 0.1)
        assert self.trigger.status == IO.ON
        assert self.trigger.out.status == IO.OFF

    def test_trigger_not_on(self):
        self.trigger2.off()
        time.sleep(self.trigger2.delay + 0.1)
        self.trigger2.on()
        assert self.trigger2.status == IO.ON
        assert self.trigger2.out.status == IO.ON
        time.sleep(self.trigger2.delay + 0.1)
        assert self.trigger2.status == IO.ON
        assert self.trigger2.out.status == IO.ON

    def test_trigger_off(self):
        self.trigger2.on()
        self.trigger2.off()
        assert self.trigger2.status == IO.OFF
        assert self.trigger2.out.status == IO.OFF
        time.sleep(self.trigger2.delay + 0.1)
        assert self.trigger2.status == IO.OFF
        assert self.trigger2.out.status == IO.ON
