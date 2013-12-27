from rpitc.io import IO
from rpitc.io.out import Out
from rpitc.io.switch import Switch
import RPi.GPIO as GPIO

class TestSwitch:

    def setup_method(self, method):
        self.out = Out(7, status=IO.OFF)
        self.switch = Switch(self.out, status=IO.OFF)

    def teardown_method(self, method):
        GPIO.output(self.out.pin, GPIO.LOW)
        GPIO.cleanup()

    def test_init(self):
        assert isinstance(self.switch, Switch)

    def test_on(self):
        self.switch.on()
        assert self.out.status == IO.ON
        assert self.switch.status == IO.ON

    def test_off(self):
        self.switch.off()
        assert self.out.status == IO.OFF
        assert self.switch.status == IO.OFF

    def test_toggle(self):
        self.switch.off()
        self.switch.toggle()
        assert self.out.status == IO.ON
        assert self.switch.status == IO.ON

