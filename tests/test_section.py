from rpitc.section import Section
import fysom
import pytest
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock


class TestSection:

    def test_inital_idle(self, section):
        assert section.blocked
        assert section.status == Section.IDLE

    def test_requires_next(self):
        with pytest.raises(TypeError):
            Section(previous=None)

    def test_requires_last(self):
        with pytest.raises(TypeError):
            Section(next=None)

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

    def test_wait_if_next_blocked(self, section):
        section.await()
        section.arrive()
        section.arrived()
        assert section.blocked
        assert section.status == Section.WAITING

    def test_depart_if_next_not_blocked(self, section):
        section.next.blocked = False
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

# XXX Test case for section subclass
#    def test_ondepart(self, section):
#        section.await()
#        section.arrive()
#        section.arrived()
#        section.depart()
#        section.previous.departed.assert_called_once_with()
#
#    def test_ondeparting_not_blocked(self, section):
#        section.next.blocked = False
#        section.await()
#        section.arrive()
#        section.arrived()
#        section.previous.departed.assert_called_once_with()

    def test_ondeparted(self, section):
        section.await()
        section.previous.depart.assert_called_once_with()
        section.arrive()
        section.arrived()
        section.depart()
        section.departed()
        section.previous.depart.assert_not_called()

    def test_ondeparted_previous_idle_does_not_raise(self, section):
        section.previous = Section(next=section, previous=Mock())
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
