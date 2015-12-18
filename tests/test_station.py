from rpitc.section import Section
from rpitc.station.gateway import Entrance, BareEntrance
import fysom
import pytest


@pytest.fixture(scope='function')
def bare_entrance(mock):
    return BareEntrance(previous=mock())


class TestBareEntrance:
    def test_arrive(self, bare_entrance):
        bare_entrance.await()
        with pytest.raises(NotImplementedError):
            bare_entrance.arrive()

    def test_arrived(self, bare_entrance):
        bare_entrance.await()
        bare_entrance.arrived()
        bare_entrance._previous.departed.assert_called_once_with()
