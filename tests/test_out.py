class TestOut:

    def test_init_on(self, IO):
        from rpitc.io.out import Out
        out = Out(7, status=IO.ON)
        assert out.status == IO.ON
        out.off()

    def test_on(self, out, IO):
        out.on()
        assert out.status == IO.ON

    def test_off(self, out, IO):
        out.off()
        assert out.status == IO.OFF

    def test_toggle(self, out, IO):
        out.off()
        out.toggle()
        assert out.status == IO.ON

        out.toggle()
        assert out.status == IO.OFF
