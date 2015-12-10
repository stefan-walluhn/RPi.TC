from fysom import Fysom


class Section(object):

    IDLE = 'idle'
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
                ('arrive', Section.IDLE, Section.ARRIVING),
                ('wait', Section.ARRIVING, Section.WAITING),
                ('depart', Section.ARRIVING, Section.DEPARTING),
                ('depart', Section.WAITING, Section.DEPARTING),
                ('resolve', Section.DEPARTING, Section.IDLE)],
            callbacks=[
                ('onwait', self._onwait),
                ('ondeparting', self._ondeparting),
                ('ondepart', self._ondepart),
                ('onresolve', self._onresolve)])

    @property
    def blocked(self):
        return not self._fsm.is_finished()

    @property
    def status(self):
        return self._fsm.current

    def arrive(self):
        self._fsm.arrive()

    def arrived(self):
        if not self.next.blocked:
            self._fsm.depart()
            return
        self._fsm.wait()

    def depart(self):
        # The section may be in idle or arriving state
        if self._fsm.can('depart'):
            self._fsm.depart()

    def departed(self):
        self._fsm.resolve()

    def _onwait(self, e):
        self.previous.departed()

    def _ondepart(self, e):
        if e.src == Section.ARRIVING:
            self.previous.departed()

    def _ondeparting(self, e):
        self.next.arrive()

    def _onresolve(self, e):
        self.previous.depart()
