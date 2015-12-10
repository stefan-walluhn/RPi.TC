from fysom import Fysom


class Section:

    IDLE = 'idle'
    ARRIVING = 'arriving'
    WAITING = 'waiting'
    DEPARTING = 'departing'

    def __init__(self, next, previous):
        self.next = next
        self.previous = previous
        self._fsm = Fysom(
            initial=Section.IDLE,
            events=[
                ('arrive', Section.IDLE, Section.ARRIVING),
                ('wait', Section.ARRIVING, Section.WAITING),
                ('depart', Section.WAITING, Section.DEPARTING),
                ('resolve', Section.DEPARTING, Section.IDLE),
                ('resolve', Section.IDLE, Section.IDLE)],
            callbacks=[
                ('onleavedeparting', self._onleavedeparting),])

    @property
    def blocked(self):
        return not self._fsm.isstate(Section.IDLE)

    @property
    def status(self):
        return self._fsm.current

    def arrive(self):
        self._fsm.arrive()

    def wait(self):
        self._fsm.wait()

    def depart(self):
        self._fsm.depart()

    def resolve(self):
        self._fsm.resolve()

    def _onleavedeparting(self, e):
        self.previous.depart()
