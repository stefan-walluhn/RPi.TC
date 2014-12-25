from rpitc import PathCollision
from rpitc.element.turnout import Turnout
from rpitc.trail import Trail
import fysom
import pytest

class Observer:

    def __init__(self):
        self.status = None

    def update(self, status):
        self.status = status


class TestTrail:

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

    def setup_method(self, method):
        self.observer = Observer()

    def test_init(self):
        assert isinstance(self.trail, Trail)

    def test_status(self):
        assert self.trail.status == Trail.IDLE

    def test_exception_on_activate(self):
        with pytest.raises(fysom.FysomError) as e:
            self.trail.activate()
        assert e.value.args[0] == 'event activate inappropriate in current state idle'

    def test_register(self):
        self.trail.register()
        assert self.trail.status == Trail.HOLD

    def test_register_colliding(self):
        another_trail = Trail(self.path2)
        with pytest.raises(PathCollision) as e:
            another_trail.register()

    def test_unregister(self):
        self.trail.resolve()
        assert self.trail.status == Trail.IDLE
        self.trail.register()
        assert self.trail.status == Trail.HOLD

    def test_add_observer(self):
        self.trail.subscribe(self.observer)
        assert self.trail._observers == [self.observer]

    def test_callback_on_resolve(self):
        self.trail.subscribe(self.observer)
        self.trail.resolve()
        self.trail.register()
        self.trail.resolve()
        assert self.observer.status == Trail.IDLE

