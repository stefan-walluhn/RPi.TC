import logging
from fysom import Fysom
from rpitc.store import Store


logger = logging.getLogger(__name__)


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

    def onchangestate(self, on_change):
        self._fsm.onchangestate = on_change

    def register(self):
        logger.debug('register {}'.format(self))
        self._fsm.register()

    def prepare(self):
        logger.debug('prepare {}'.format(self))
        self._fsm.prepare()

    def activate(self):
        logger.debug('activate {}'.format(self))
        self._fsm.activate()

    def resolve(self):
        logger.debug('resolve {}'.format(self))
        self._fsm.resolve()

    def _onbeforeregister(self, e):
        self.store.register(self.path)

    def _registered(self, e):
        self.prepare()

    def _onidle(self, e):
        if e.src is not "none":
            self.store.unregister(self.path)


class TrailObserver(object):

    def __init__(self, trail):
        self._adapter = []
        self._trail = trail
        self._trail.onchangestate(self.on_change)

    def register_adapter(self, adapter):
        self._adapter.append(adapter)

    def on_change(self, e):
        for adapter in self._adapter:
            adapter.publish(e.event)
