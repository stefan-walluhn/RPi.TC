class TestSwitch:

    def test_on(self, switch, IO):
        switch.on()
        for out in switch.out:
            assert out.status == IO.ON
        assert switch.status == IO.ON

    def test_off(self, switch, IO):
        switch.off()
        for out in switch.out:
            assert out.status == IO.OFF
        assert switch.status == IO.OFF

    def test_toggle(self, switch, IO):
        switch.off()
        switch.toggle()
        for out in switch.out:
            assert out.status == IO.ON
        assert switch.status == IO.ON

    def test_multiple_out(self, out, trigger, IO):
        from rpitc.io.switch import Switch
        out.off()
        switch = Switch([out, trigger])
        switch.toggle()
        assert switch.status == IO.ON
        assert out.status == IO.ON
        assert trigger.status == IO.ON
