from rpitc.section import Section, BareSection
import fysom
import pytest
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock


@pytest.fixture(scope='function')
def auto_await_section():
    m_sec = Mock()
    return Section(previous=m_sec, auto_await=True)


@pytest.fixture(scope='function')
def bare_section():
    m_sec = Mock()
    return BareSection(previous=m_sec)


class TestSection:

    def test_inital_idle(self, section):
        assert section.blocked
        assert section.status == Section.IDLE

    def test_requires_previos_section(self):
        with pytest.raises(TypeError):
            Section()

    def test_await(self, section):
        section.await()
        assert not section.blocked
        assert section.status == Section.AWAITING

    def test_arrive(self, section):
        section.await()
        section.arrive()
        assert section.blocked
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
        assert section.status == Section.WAITING

    def test_depart_next_not_blocked(self, section):
        section._can_depart = True
        section.await()
        section.arrive()
        section.arrived()
        assert section.blocked
        assert section.status == Section.DEPARTING

    def test_depart(self, section):
        section.await()
        section.arrive()
        section.arrived()
        section.depart()
        assert section.blocked
        assert section.status == Section.DEPARTING

    def test_resolve(self, section):
        section.await()
        section.arrive()
        section.arrived()
        section.depart()
        section.departed()
        assert section.blocked
        assert section.status == Section.IDLE

    def test_onarrive(self, section):
        section.await()
        section.arrive()
        section.previous.departed.assert_called_once_with()

    def test_ondepart(self, section):
        section.await()
        section.arrive()
        section.arrived()
        section.depart()
        assert not section._can_depart

    def test_ondeparted(self, section):
        section.await()
        section.previous.depart.assert_called_once_with()
        section.arrive()
        section.arrived()
        section.depart()
        section.departed()
        section.previous.depart.assert_not_called()

    def test_ondeparted_previous_idle_does_not_raise(self, section):
        section.previous = Section(previous=Mock())
        section.await()
        section.previous.await()
        section.previous.arrive()
        section.previous.arrived()
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
    def test_onarrive(self, bare_section):
        bare_section.await()
        bare_section.arrive()
        bare_section.previous.departed.assert_not_called()

    def test_onwait(self, bare_section):
        bare_section.await()
        bare_section.arrive()
        bare_section.arrived()
        bare_section.previous.departed.assert_called_once_with()

    def test_ondepart(self, bare_section):
        bare_section.await()
        bare_section.arrive()
        bare_section.arrived()
        bare_section.depart()
        bare_section.previous.departed.assert_called_once_with()

    def test_ondepart_next_not_blocked(self, bare_section):
        bare_section._can_depart = True
        bare_section.await()
        bare_section.arrive()
        bare_section.arrived()
        bare_section.previous.departed.assert_called_once_with()
