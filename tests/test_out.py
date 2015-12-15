from rpitc.io import IO


class TestOut:
    def test_init_on(self, gpio):
        from rpitc.io.out import Out
        out = Out(7, status=IO.ON)
        assert out.status == IO.ON
        out.off()

    def test_set_pin(self, out):
        assert out.set_pin(IO.ON) == IO.ON

    def test_on(self, out):
        out.on()
        assert out.status == IO.ON

    def test_off(self, out):
        out.off()
        assert out.status == IO.OFF

    def test_toggle(self, out):
        out.off()
        out.toggle()
        assert out.status == IO.ON

        out.toggle()
        assert out.status == IO.OFF
