from rpitc.io import IO
from rpitc.io.out import Out
from rpitc.io.trigger import Trigger
from rpitc.io.switch import Switch

class TestSwitch:

    def setup_method(self, method):
        self.out = Out(7, status=IO.OFF)
        self.trigger = Trigger(5)
        self.switch = Switch(self.out, status=IO.OFF)

    def teardown_method(self, method):
        self.out.off()
        self.trigger.off()

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

    def test_multiple_out(self):
        self.out.off()
        self.switch = Switch([self.out, self.trigger])
        self.switch.toggle()
        assert self.switch.status == IO.ON
        assert self.out.status == IO.ON
        assert self.trigger.status == IO.ON

