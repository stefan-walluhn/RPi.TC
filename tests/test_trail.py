import pytest
import fysom
from rpitc.trail import Trail

class Observer:

    def __init__(self):
        self.status = None

    def update(self, status):
        self.status = status


class TestTrail:

    def setup_method(self, method):
        self.trail = Trail()
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
        assert self.trail.status == Trail.REGISTERED

    def test_add_observer(self):
        self.trail.subscribe(self.observer)
        assert self.trail._observers == [self.observer]

    def test_callback_on_resolve(self):
        self.trail.subscribe(self.observer)
        self.trail.register()
        self.trail.resolve()
        assert self.observer.status == Trail.IDLE
