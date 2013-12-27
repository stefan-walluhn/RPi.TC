from rpitc.io import IO
from rpitc.io.out import Out

class TestOut:

    def setup_method(self, method):
        self.out = Out(7)

    def teardown_method(self, method):
        self.out.off()

    def test_init(self):
        assert isinstance(self.out, Out)

    def test_init_on(self):
        out = Out(7, status=IO.ON)
        assert out.status == IO.ON
        out.off()

    def test_on(self):
        self.out.on()
        assert self.out.status == IO.ON

    def test_off(self):
        self.out.off()
        assert self.out.status == IO.OFF


    def test_toggle(self):
        self.out.off()

        self.out.toggle()
        assert self.out.status == IO.ON

        self.out.toggle()
        assert self.out.status == IO.OFF
