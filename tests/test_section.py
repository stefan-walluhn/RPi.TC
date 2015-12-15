from rpitc.io import IO
from rpitc.section import Section, BareSection, ClassicSection
import fysom
import pytest
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock


@pytest.fixture(scope='function')
def auto_await_section(out):
    return Section(out=out, previous=Mock(), auto_await=True)


@pytest.fixture(scope='function')
def bare_section(out):
    return BareSection(out=out, previous=Mock())


@pytest.fixture(scope='function')
def classic_section(out):
    return ClassicSection(out=out, previous=Mock())


class TestSection:

    def test_inital_idle(self, section):
        assert section.blocked
        assert section.status == Section.IDLE

    def test_has_out(self, section):
        assert section._out.status == IO.OFF

    def test_requires_previos_section(self):
        with pytest.raises(TypeError):
            Section()

    def test_await(self, section):
        section.await()
        assert not section.blocked
        assert section._out.status == IO.ON
        assert section.status == Section.AWAITING

    def test_arrive(self, section):
        section.await()
        section.arrive()
        assert section.blocked
        assert section._out.status == IO.ON
        assert section.status == Section.ARRIVING

    def test_arrive_only_once(self, section):
        section.await()
        section.arrive()
        with pytest.raises(fysom.FysomError):
            section.arrive()

    def test_wait_next_blocked(self, section):
        section.await()
        section.arrive()
        section.arrived()
        assert section.blocked
        assert section._out.status == IO.OFF
        assert section.status == Section.WAITING

    def test_depart_next_not_blocked(self, section):
        section._can_depart = True
        section.await()
        section.arrive()
        section.arrived()
        assert section.blocked
        assert section._out.status == IO.ON
        assert section.status == Section.DEPARTING

    def test_depart(self, section):
        section.await()
        section.arrive()
        section.arrived()
        section.depart()
        assert section.blocked
        assert section._out.status == IO.ON
        assert section.status == Section.DEPARTING

    def test_resolve(self, section):
        section.await()
        section.arrive()
        section.arrived()
        section.depart()
        section.departed()
        assert section.blocked
        assert section._out.status == IO.OFF
        assert section.status == Section.IDLE

    def test_onarrive(self, section):
        section.await()
        section.arrive()
        section._previous.departed.assert_called_once_with()

    def test_ondepart(self, section):
        section.await()
        section.arrive()
        section.arrived()
        section.depart()
        assert not section.can_depart

    def test_ondeparted(self, section):
        section.await()
        section._previous.depart.assert_called_once_with()
        section._previous.depart.reset_mock()
        section.arrive()
        section.arrived()
        section.depart()
        section.departed()
        section._previous.depart.assert_not_called()

    def test_ondeparted_previous_idle_does_not_raise(self, out, section):
        section._previous = Section(out=out, previous=Mock())
        section.await()
        section._previous.await()
        section._previous.arrive()
        section._previous.arrived()
        section.arrive()
        section.arrived()
        section.depart()
        try:
            section.departed()
        except fysom.FysomError:
            pytest.fail("Last section idle, should not raise")

    def test_auto_await_init(self, auto_await_section):
        assert not auto_await_section.blocked
        assert auto_await_section.status == Section.AWAITING

    def test_auto_await(self, auto_await_section):
        auto_await_section.arrive()
        auto_await_section.arrived()
        auto_await_section.depart()
        auto_await_section.departed()
        assert not auto_await_section.blocked
        assert auto_await_section.status == Section.AWAITING


class TestBareSection:
    def test_arrive(self, bare_section):
        bare_section.await()
        with pytest.raises(NotImplementedError):
            bare_section.arrive()

    def test_arrived(self, bare_section):
        bare_section.await()
        bare_section.arrived()
        bare_section._previous.departed.assert_called_once_with()


class TestClassicSection:
    def test_await(self, classic_section):
        classic_section.await()
        assert classic_section._out.status == IO.OFF

    def test_arrive(self, classic_section):
        classic_section.await()
        classic_section.arrive()
        classic_section._previous.departed.assert_called_once_with()
        assert classic_section._out.status == IO.OFF
        assert classic_section.status == Section.WAITING

    def test_arrived(self, classic_section):
        classic_section.await()
        classic_section.arrive()
        with pytest.raises(NotImplementedError):
            classic_section.arrived()

    def test_depart(self, classic_section):
        classic_section.await()
        classic_section.arrive()
        classic_section.depart()
        assert classic_section._out.status == IO.ON

    def test_depart_next_not_blocked(self, classic_section):
        classic_section._can_depart = True
        classic_section.await()
        classic_section.arrive()
        assert classic_section._out.status == IO.ON

    def test_departed(self, classic_section):
        classic_section.await()
        classic_section.arrive()
        classic_section.depart()
        classic_section.departed()
        assert classic_section._out.status == IO.OFF
