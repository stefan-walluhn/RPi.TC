from fysom import Fysom
from rpitc import PathCollision
from rpitc.store import Store

class Trail:

    IDLE = 'idle'
    REGISTERED = 'registered'
    HOLD = 'hold'
    ACTIVE = 'active'

    _observers = []
    
    def __init__(self, path=None):
        self.path = path
        self.store = Store()
        self._fsm = Fysom(
                initial=Trail.IDLE,
                events=[
                    ('register', Trail.IDLE, Trail.REGISTERED),
                    ('prepare', Trail.REGISTERED, Trail.HOLD),
                    ('activate', Trail.HOLD, Trail.ACTIVE),
                    ('resolve', Trail.ACTIVE, Trail.IDLE),
                    ('resolve', Trail.HOLD, Trail.IDLE),
                    ('resolve', Trail.REGISTERED, Trail.IDLE),
                    ('resolve', Trail.IDLE, Trail.IDLE)],
                callbacks=[
                    ('onidle', self._update),
                    ('onregistered', self._registered),
                    ('onhold', self._update),
                    ('onactive', self._update),
                    ('onbeforeresolve', self._onbeforeresolve),
                    ('onbeforeregister', self._onbeforeregister)])

    def subscribe(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)

    @property
    def status(self):
        return self._fsm.current

    def register(self):
        self._fsm.register()

    def _onbeforeregister(self, e):
        self.store.register(self)

    def _registered(self, e):
        self._update(e)
        self.prepare()

    def prepare(self):
        self._fsm.prepare()

    def activate(self):
        self._fsm.activate()

    def resolve(self):
        self._fsm.resolve()

    def _onbeforeresolve(self, e):
        self.store.unregister(self)
        return True

    def _update(self, e):
        for observer in self._observers:
            observer.update(Event(self, src=e.src, dst=e.dst))


class Event:

    def __init__(self, trail, src=None, dst=None):
        self.trail = trail
        self.src = src
        self.dst = dst

