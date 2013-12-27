from rpitc.io import IO
from rpitc.io.trigger import Trigger
import RPi.GPIO as GPIO
import time

class TestTrigger:

    def setup_method(self, method):
        self.trigger = Trigger(7, delay=1, status=IO.OFF)

    def teardown_method(self, method):
        GPIO.output(self.trigger.pin, GPIO.LOW)
        GPIO.cleanup()

    def test_init(self):
        assert isinstance(self.trigger, Trigger)

    def test_trigger(self):
        self.trigger.trigger()
        assert self.trigger.status == IO.ON
        time.sleep(self.trigger.delay + 0.1)
        assert self.trigger.status == IO.OFF

