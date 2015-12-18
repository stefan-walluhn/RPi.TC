from fysom import Fysom
from rpitc.store import Store


class Trail:
    IDLE = 'idle'
    REGISTERED = 'registered'
    HOLD = 'hold'
    ACTIVE = 'active'

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
                    ('resolve', Trail.REGISTERED, Trail.IDLE)],
                callbacks=[
                    ('onbeforeregister', self._onbeforeregister),
                    ('onregistered', self._registered),
                    ('onidle', self._onidle)])

    @property
    def status(self):
        return self._fsm.current

    def register(self):
        self._fsm.register()

    def prepare(self):
        self._fsm.prepare()

    def activate(self):
        self._fsm.activate()

    def resolve(self):
        self._fsm.resolve()

    def _onbeforeregister(self, e):
        self.store.register(self.path)

    def _registered(self, e):
        self.prepare()

    def _onidle(self, e):
        if e.src is not "none":
            self.store.unregister(self.path)
