from rpitc.exceptions import PathCollisionError
from rpitc.element.turnout import Turnout
from rpitc.store import Store
from rpitc.station.trail import Trail
import pytest

class TestStore:

    turnout1 = Turnout()
    turnout2 = Turnout()
    turnout3 = Turnout()
    turnout4 = Turnout()

    path1 = [(turnout1, Turnout.STRAIGHT),
             (turnout2, Turnout.TURNOUT),
             (turnout3, Turnout.STRAIGHT)]
    path2 = [(turnout1, Turnout.STRAIGHT),
             (turnout4, Turnout.TURNOUT)]

    trail = Trail(path=path1)

    store = Store()

    def test_init(self):
        assert isinstance(self.store, Store)

    def test_singleton(self):
        another_store = Store()
        assert self.store.instance is another_store.instance

    def test_register(self):
        self.store.register(self.trail)
        assert self.store.trails == [self.trail]

    def test_refuse_colliding_trail(self):
        trail = Trail(path=self.path2)
        with pytest.raises(PathCollisionError) as e:
            self.store.register(trail)
        assert e.value.colliding_trail.path is self.path1

    def test_unregister(self):
        self.store.unregister(self.trail)
        assert self.store.trails == []

