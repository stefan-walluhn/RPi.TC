from rpitc.exceptions import PathCollisionError
from rpitc.element.turnout import Turnout
from rpitc.station.trail import Trail
import fysom
import pytest


class TestTrail:
    def test_status(self, trail):
        assert trail.status == Trail.IDLE

    def test_exception_on_activate(self, trail):
        with pytest.raises(fysom.FysomError):
            trail.activate()

    def test_register(self, trail):
        trail.register()
        assert trail.status == Trail.HOLD

    def test_register_colliding(self, turnout, trail):
        trail.register()
        path = [(turnout, Turnout.STRAIGHT), (Turnout(), Turnout.TURNOUT)]
        another_trail = Trail(path)
        with pytest.raises(PathCollisionError):
            another_trail.register()

    def test_activate(self, trail):
        trail.register()
        trail.activate()
        assert trail.status == Trail.ACTIVE

    def test_resolve(self, trail):
        trail.register()
        trail.resolve()
        assert trail.status == Trail.IDLE

    def test_unregister_on_resolve(self, trail):
        trail.register()
        trail.resolve()
        trail.register()
        assert trail.status == Trail.HOLD
