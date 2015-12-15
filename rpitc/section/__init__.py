from fysom import Fysom, Canceled


class Section(object):

    IDLE = 'idle'
    AWAITING = 'awaiting'
    ARRIVING = 'arriving'
    WAITING = 'waiting'
    DEPARTING = 'departing'

    def __init__(self, out, previous, auto_await=False):
        self._out = out
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
                ('onawaiting', self._onawaiting),
                ('onawait', self._onawait),
                ('onarrive', self._onarrive),
                ('onwaiting', self._onwaiting),
                ('onwait', self._onwait),
                ('onleavewaiting', self._onleavewaiting),
                ('onbeforedepart', self._onbeforedepart),
                ('ondeparting', self._ondeparting),
                ('ondepart', self.__ondepart__),
                ('onleavedeparting', self._onleavedeparting),
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

    def _onawaiting(self, e):
        self._out.on()

    def _onawait(self, e):
        self._previous.depart()

    def _onarrive(self, e):
        self._previous.departed()

    def _onwaiting(self, e):
        self._out.off()

    def _onwait(self, e):
        pass

    def _onleavewaiting(self, e):
        self._out.on()

    def _onbeforedepart(self, e):
        return self.can_depart

    def _ondeparting(self, e):
        pass

    def __ondepart__(self, e):
        self._can_depart = False
        self._ondepart(e)

    def _ondepart(self, e):
        pass

    def _onleavedeparting(self, e):
        self._out.off()

    def _onresolve(self, e):
        if self._auto_await:
            self._fsm.await()


class BareSection(Section):

    def arrive(self):
        raise NotImplementedError

    def arrived(self):
        super(BareSection, self).arrive()
        super(BareSection, self).arrived()


class ClassicSection(Section):

    def arrive(self):
        super(ClassicSection, self).arrive()
        super(ClassicSection, self).arrived()

    def arrived(self):
        raise NotImplementedError

    def _onawaiting(self, e):
        pass

    def _onwaiting(self, e):
        pass

    def _onleavewaiting(self, e):
        pass

    def _ondeparting(self, e):
        self._out.on()
