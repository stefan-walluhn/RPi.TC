from fysom import Fysom


class Section(object):

    IDLE = 'idle'
    AWAITING = 'awaiting'
    ARRIVING = 'arriving'
    WAITING = 'waiting'
    DEPARTING = 'departing'

    def __init__(self, next, previous):
        self.next = next
        self.previous = previous
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
                ('ondepart', self._ondepart)])

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
        if not self.next.blocked:
            self._fsm.depart()
            return
        self._fsm.wait()

    def depart(self):
        # The section may be in awaiting or arriving state
        if self.status == Section.WAITING:
            self._fsm.depart()

    def departed(self):
        self._fsm.resolve()

    def _onawait(self, e):
        self.previous.depart()

    def _onarrive(self, e):
        self.previous.departed()

    def _onwait(self, e):
        pass

    def _ondepart(self, e):
        pass


class FooSection(Section):

    def _onarrive(self, e):
        pass

    def _onwait(self, e):
        self.previous.departed()

    def _ondepart(self, e):
        if e.src == Section.ARRIVING:
            self.previous.departed()

