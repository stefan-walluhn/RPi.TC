from rpitc.io import IO
import time


class TestTrigger:

    def test_sleep_injection(self, out):
        from rpitc.io.trigger import Trigger
        trigger = Trigger(out)
        assert trigger.sleep == time.sleep

    def test_trigger_on(self, trigger):
        trigger.on()
        assert trigger.status == IO.ON
        assert trigger.out.status == IO.ON
        time.sleep(trigger.delay + 0.2)
        assert trigger.status == IO.ON
        assert trigger.out.status == IO.OFF

    def test_trigger_not_on(self, out):
        from rpitc.io.trigger import Trigger
        out.on()
        trigger = Trigger(out, status=IO.OFF, trigger_on=IO.OFF)

        trigger.on()
        assert trigger.status == IO.ON
        assert trigger.out.status == IO.ON
        time.sleep(trigger.delay + 0.2)
        assert trigger.status == IO.ON
        assert trigger.out.status == IO.ON

    def test_trigger_off(self, out):
        from rpitc.io.trigger import Trigger
        out.on()
        trigger = Trigger(out, status=IO.ON, trigger_on=IO.OFF)

        trigger.off()
        time.sleep(0.1)
        assert trigger.status == IO.OFF
        assert trigger.out.status == IO.OFF
        time.sleep(trigger.delay + 0.2)
        assert trigger.status == IO.OFF
        assert trigger.out.status == IO.ON
