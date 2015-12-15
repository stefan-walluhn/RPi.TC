from rpitc.section import Section
from rpitc.station.gateway import Entrance, BareEntrance
import fysom
import pytest
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock


@pytest.fixture(scope='function')
def bare_entrance():
    return BareEntrance(previous=Mock())


class TestEntrance:

    def test_initial_idle(self, entrance):
        assert entrance.blocked
        assert entrance.status == Section.IDLE

    def test_requires_previos_section(self):
        with pytest.raises(TypeError):
            Entrance()

    def test_await(self, entrance):
        entrance.await()
        assert not entrance.blocked
        assert entrance.status == Section.AWAITING

    def test_arrive(self, entrance):
        entrance.await()
        entrance.arrive()
        assert entrance.blocked
        assert entrance.status == Section.ARRIVING

    def test_arrive_only_once(self, entrance):
        entrance.await()
        entrance.arrive()
        with pytest.raises(fysom.FysomError):
            entrance.arrive()

    def test_resolve(self, entrance):
        entrance.await()
        entrance.arrive()
        entrance.arrived()
        assert entrance.blocked
        assert entrance.status == Section.IDLE

    def test_onarrive(self, entrance):
        entrance.await()
        entrance._previous.depart.assert_called_once_with()

    def test_onarrive(self, entrance):
        entrance.await()
        entrance.arrive()
        entrance._previous.departed.assert_called_once_with()

    def test_onarrived(self, entrance):
        entrance.await()
        entrance._previous.depart.assert_called_once_with()
        entrance._previous.depart.reset_mock()
        entrance.arrive()
        entrance.arrived()
        entrance._previous.depart.assert_not_called()


class TestBareEntrance:
    def test_arrive(self, bare_entrance):
        bare_entrance.await()
        with pytest.raises(NotImplementedError):
            bare_entrance.arrive()

    def test_arrived(self, bare_entrance):
        bare_entrance.await()
        bare_entrance.arrived()
        bare_entrance._previous.departed.assert_called_once_with()


class TestExit:
    def test_inital_idle(self, exit):
        assert exit.status == Section.IDLE

    def test_depart_next_blocked(self, exit):
        exit.request_depart()
        assert exit.status == Section.WAITING

    def test_depart_next_not_blocked(self, exit):
        exit._can_depart = True
        exit.request_depart()
        assert exit.status == Section.DEPARTING

    def test_depart(self, exit):
        exit.request_depart()
        exit.depart()
        assert exit.status == Section.DEPARTING

    def test_resolve(self, exit):
        exit.request_depart()
        exit.depart()
        exit.departed()
        assert exit.status == Section.IDLE

    def test_ondepart(self, exit):
        exit.request_depart()
        exit.depart()
        assert not exit.can_depart
