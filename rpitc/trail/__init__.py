from fysom import Fysom

class Trail:

    IDLE = 'idle'
    REGISTERED = 'registered'
    HOLD = 'hold'
    ACTIVE = 'active'

    _observers = []
    
    def __init__(self):
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
                    ('onidle', self._onidle),
                    ('onbeforeregister', self._onbeforeregister)])

    def subscribe(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)

    @property
    def status(self):
        return self._fsm.current

    def register(self):
        self._fsm.register()

    def activate(self):
        self._fsm.activate()

    def resolve(self):
        self._fsm.resolve()

    def _onbeforeregister(self, e):
        return True

    def _onidle(self, e):
        self._update(e)

    def _update(self, e):
        for observer in self._observers:
            observer.update(e.dst)
