from rpitc.io import IO, BaseOut
import pytest


@pytest.fixture
def io_status():
    return IO.OFF


@pytest.fixture(scope='function')
def implementation():
    class ImplementationMixin(object):
        def _on(self): return super(ImplementationMixin, self)._on()
        def _off(self): return super(ImplementationMixin, self)._off()
    return ImplementationMixin


@pytest.fixture
def base_out(io_status, implementation):
    class BaseOutImpl(implementation, BaseOut):
        pass
    return BaseOutImpl(status=io_status)


class TestIO:
    def test_io_on(self):
        assert IO.ON is True

    def test_io_off(self):
        assert IO.OFF is False

    def test_base_out_init(self, base_out):
        assert base_out.status is IO.OFF

    @pytest.mark.parametrize('io_status', [IO.ON])
    def test_base_out_init_on(self, base_out):
        assert base_out.status is IO.ON

    def test_base_out_on(self, base_out):
        base_out.on()
        assert base_out.status is IO.ON

    def test_off(self, base_out):
        base_out.on()
        base_out.off()
        assert base_out.status is IO.OFF

    def test_toggle(self, base_out):
        base_out.toggle()
        assert base_out.status is IO.ON

        base_out.toggle()
        assert base_out.status is IO.OFF

    def test_base_out_abstract_on(self, implementation):
        del implementation._on

        class BaseOutWithoutOn(implementation, BaseOut):
            pass

        with pytest.raises(TypeError):
            BaseOutWithoutOn()

    def test_base_out_abstract_off(self, implementation):
        del implementation._off

        class BaseOutWithoutOff(implementation, BaseOut):
            pass

        with pytest.raises(TypeError):
            BaseOutWithoutOff()
