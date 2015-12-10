from rpitc import PathCollision
from rpitc.element.turnout import Turnout
from rpitc.trail import Trail, Event
import fysom
import pytest


class TestTrail:
    def test_status(self, trail):
        assert trail.status == Trail.IDLE

    def test_exception_on_activate(self, trail):
        with pytest.raises(fysom.FysomError) as e:
            trail.activate()
        assert e.value.args[0] == 'event activate inappropriate in current state idle'

    def test_register(self, trail):
        trail.register()
        assert trail.status == Trail.HOLD

    def test_register_colliding(self, turnout, trail):
        trail.register()
        path = [(turnout, Turnout.STRAIGHT), (Turnout(), Turnout.TURNOUT)]
        another_trail = Trail(path)
        with pytest.raises(PathCollision) as e:
            another_trail.register()

    def test_unregister(self, trail):
        trail.resolve()
        assert trail.status == Trail.IDLE
        trail.register()
        assert trail.status == Trail.HOLD

    def test_add_observer(self, trail, observer):
        trail.subscribe(observer)
        assert trail._observers == [observer]

    def test_callback_on_resolve(self, trail, observer):
        trail.subscribe(observer)
        trail.resolve()
        trail.register()
        trail.resolve()
        assert observer.status == Trail.IDLE


class TestEvent:

    def test_event(self):
        trail = Trail()
        e = Event(trail, src=Trail.IDLE, dst=Trail.REGISTERED)
        assert e.trail == trail
        assert e.src == Trail.IDLE
        assert e.dst == Trail.REGISTERED
