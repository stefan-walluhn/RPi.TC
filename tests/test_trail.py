from rpitc.adapter import Adapter
from rpitc.exceptions import PathCollisionError
from rpitc.element.turnout import Turnout
from rpitc.station.trail import Trail, TrailObserver
import fysom
import pytest


@pytest.fixture
def trail_observer(trail):
    return TrailObserver(trail)


@pytest.fixture
def adapter():
    return Adapter()


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

    def test_onchangestate(self, mock, trail):
        on_change = mock()
        trail.onchangestate(on_change)
        trail.register()
        assert on_change.call_count == 2


class TestTrailObserver:
    def test_init(self, trail, trail_observer):
        assert trail_observer._trail is trail

    def test_register_adapter(self, adapter, trail_observer):
        trail_observer.register_adapter(adapter)
        assert trail_observer._adapter == [adapter]

    def test_handle_events(self, mock, trail):
        class MockTrailObserver(TrailObserver):
            on_change = mock()
        trail_observer = MockTrailObserver(trail)
        trail.register()
        assert trail_observer.on_change.call_count == 2

    def test_on_change(self, mock, adapter, trail_observer):
        class _e_obj(object):
            event = 'test'
        e = _e_obj()
        adapter.publish = mock()
        trail_observer.register_adapter(adapter)
        trail_observer.on_change(e)
        adapter.publish.assert_called_once_with('test')
