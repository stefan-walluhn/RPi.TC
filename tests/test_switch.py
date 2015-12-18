from rpitc.io import IO


class TestSwitch:

    def test_on(self, switch):
        switch.on()
        for out in switch._out:
            assert out.status == IO.ON
        assert switch.status == IO.ON

    def test_off(self, switch):
        switch.off()
        for out in switch._out:
            assert out.status == IO.OFF
        assert switch.status == IO.OFF

    def test_toggle(self, switch):
        switch.off()
        switch.toggle()
        for out in switch._out:
            assert out.status == IO.ON
        assert switch.status == IO.ON

    def test_multiple_out(self, out, trigger):
        from rpitc.io.switch import Switch
        out.off()
        switch = Switch([out, trigger])
        switch.toggle()
        assert switch.status == IO.ON
        assert out.status == IO.ON
        assert trigger.status == IO.ON
