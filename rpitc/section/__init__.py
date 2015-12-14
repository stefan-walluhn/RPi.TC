from fysom import Fysom, Canceled


class Section(object):

    IDLE = 'idle'
    AWAITING = 'awaiting'
    ARRIVING = 'arriving'
    WAITING = 'waiting'
    DEPARTING = 'departing'

    def __init__(self, previous, auto_await=False):
        self._previous = previous
        self._auto_await = auto_await
        self._can_depart = False
        self._fsm = Fysom(
            initial=Section.IDLE,
            final=Section.IDLE,
            events=[
                ('await', Section.IDLE, Section.AWAITING),
                ('arrive', Section.AWAITING, Section.ARRIVING),
                ('wait', Section.ARRIVING, Section.WAITING),
                ('depart', Section.ARRIVING, Section.DEPARTING),
                ('depart', Section.WAITING, Section.DEPARTING),
                ('resolve', Section.DEPARTING, Section.IDLE)],
            callbacks=[
                ('onawait', self._onawait),
                ('onarrive', self._onarrive),
                ('onwait', self._onwait),
                ('onbeforedepart', self._onbeforedepart),
                ('ondepart', self.__ondepart__),
                ('onresolve', self._onresolve)])

        if self._auto_await:
            self._fsm.await()

    @property
    def blocked(self):
        return self.status is not Section.AWAITING

    @property
    def can_depart(self):
        return self._can_depart

    @property
    def status(self):
        return self._fsm.current

    def await(self):
        self._fsm.await()

    def arrive(self):
        self._fsm.arrive()

    def arrived(self):
        try:
            self._fsm.depart()
        except Canceled:
            self._fsm.wait()

    def depart(self):
        self._can_depart = True
        # The section may be in awaiting or arriving state
        if self.status == Section.WAITING:
            self._fsm.depart()

    def departed(self):
        self._fsm.resolve()

    def _onawait(self, e):
        self._previous.depart()

    def _onarrive(self, e):
        self._previous.departed()

    def _onwait(self, e):
        pass

    def _onbeforedepart(self, e):
        return self.can_depart

    def __ondepart__(self, e):
        self._can_depart = False
        self._ondepart(e)

    def _ondepart(self, e):
        pass

    def _onresolve(self, e):
        if self._auto_await:
            self._fsm.await()


class BareSection(Section):

    def arrive(self):
        raise NotImplementedError

    def arrived(self):
        super(BareSection, self).arrive()
        super(BareSection, self).arrived()
