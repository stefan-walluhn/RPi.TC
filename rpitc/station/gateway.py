from fysom import Fysom, Canceled
from rpitc.section import Section


class Entrance(object):

    IDLE = 'idle'
    AWAITING = 'awaiting'
    ARRIVING = 'arriving'

    def __init__(self, previous):
        self._previous = previous
        self._fsm = Fysom(
            initial=Section.IDLE,
            final=Section.IDLE,
            events=[
                ('await', Section.IDLE, Section.AWAITING),
                ('arrive', Section.AWAITING, Section.ARRIVING),
                ('resolve', Section.ARRIVING, Section.IDLE)],
            callbacks=[
                ('onawait', self._onawait),
                ('onarrive', self._onarrive),
                ('onresolve', self._onresolve)])

    @property
    def blocked(self):
        return self.status is not Section.AWAITING

    @property
    def status(self):
        return self._fsm.current

    def await(self):
        self._fsm.await()

    def arrive(self):
        self._fsm.arrive()

    def arrived(self):
        self._fsm.resolve()

    def _onawait(self, e):
        self._previous.depart()

    def _onarrive(self, e):
        self._previous.departed()

    def _onresolve(self, e):
        pass


class BareEntrance(Entrance):
    def arrive(self):
        raise NotImplementedError

    def arrived(self):
        super(BareEntrance, self).arrive()
        super(BareEntrance, self).arrived()


class Exit(object):

    IDLE = 'idle'
    WAITING = 'waiting'
    DEPARTING = 'departing'

    def __init__(self):
        self._can_depart = False
        self._fsm = Fysom(
            initial=Section.IDLE,
            final=Section.IDLE,
            events=[
                ('wait', Section.IDLE, Section.WAITING),
                ('depart', Section.IDLE, Section.DEPARTING),
                ('depart', Section.WAITING, Section.DEPARTING),
                ('resolve', Section.DEPARTING, Section.IDLE)],
            callbacks=[
                ('onbeforedepart', self._onbeforedepart),
                ('ondepart', self.__ondepart__)])


    @property
    def can_depart(self):
        return self._can_depart

    @property
    def status(self):
        return self._fsm.current

    def request_depart(self):
        try:
            self._fsm.depart()
        except Canceled:
            self._fsm.wait()

    def depart(self):
        self._can_depart = True
        # The section may be in idle state
        if self.status == Section.WAITING:
            self._fsm.depart()

    def departed(self):
        self._fsm.resolve()

    def _onbeforedepart(self, e):
        return self.can_depart

    def __ondepart__(self, e):
        self._can_depart = False
        self._ondepart(e)

    def _ondepart(self, e):
        pass
