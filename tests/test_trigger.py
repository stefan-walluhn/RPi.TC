import time

class TestTrigger:

    def test_trigger_on(self, trigger, IO):
        trigger.off()
        trigger.on()
        assert trigger.status == IO.ON
        assert trigger.out.status == IO.ON

        time.sleep(trigger.delay + 0.1)
        assert trigger.status == IO.ON
        assert trigger.out.status == IO.OFF

    def test_trigger_not_on(self, trigger2, IO):
        trigger2.off()
        time.sleep(trigger2.delay + 0.1)
        trigger2.on()
        assert trigger2.status == IO.ON
        assert trigger2.out.status == IO.ON
        time.sleep(trigger2.delay + 0.1)
        assert trigger2.status == IO.ON
        assert trigger2.out.status == IO.ON

    def test_trigger_off(self, trigger2, IO):
        trigger2.on()
        trigger2.off()
        assert trigger2.status == IO.OFF
        assert trigger2.out.status == IO.OFF
        time.sleep(trigger2.delay + 0.1)
        assert trigger2.status == IO.OFF
        assert trigger2.out.status == IO.ON
