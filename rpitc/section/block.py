from rpitc.section import (
    Section,
    BareMixIn,
    BaseEntranceSection,
    BaseExitSection)


class BaseBlockSection(object):

    def __init__(self, previous, auto_await=False):
        self._auto_await = auto_await
        self._entrance = BaseEntranceSection(previous)
        self._exit = BaseExitSection()
        self._exit._fsm.onresolve = self._onresolve

        if self._auto_await:
            self._entrance.await()

    @property
    def blocked(self):
        return self._entrance.blocked

    def await(self):
        self._entrance.await()

    def arrive(self):
        self._entrance.arrive()

    def arrived(self):
        self._entrance.arrived()
        self._exit.request_depart()

    def depart(self):
        self._exit.depart()

    def departed(self):
        self._exit.departed()

    def _onresolve(self, e):
        if self._auto_await:
            self._entrance.await()


class BlockSection(BaseBlockSection):
    """
    A full featured block. Trains have to trigger arriving() when entering
    the block to mark previous section to be resolved. Additional, trains have
    to trigger arrived() to mark they arrived waiting position. In waiting
    position the whole block is unpowered.
    """

    def __init__(self, out, previous, auto_await=False):
        super(BlockSection, self).__init__(previous, auto_await=auto_await)
        self._out = out
        self._entrance._fsm.onawaiting = self._onawaiting
        self._exit._fsm.onwaiting = self._onwaiting
        self._exit._fsm.onleavewaiting = self._onleavewaiting
        self._exit._fsm.onleavedeparting = self._onleavedeparting

    def _onawaiting(self, e):
        self._out.on()

    def _onwaiting(self, e):
        self._out.off()

    def _onleavewaiting(self, e):
        self._out.on()

    def _onleavedeparting(self, e):
        self._out.off()


class BareBlockSection(BareMixIn, BlockSection):
    """
    A bare block with reduced inputs. Trains must not signal arriving() but
    have to trigger arrived() to mark they arrived waiting position. In waiting
    position the whole block is unpowered. The previous section is resolved
    when waiting position is reached.
    """
    pass


class ClassicBlockSection(BlockSection):
    """
    A block that implements classic analog style behavior. Trains must trigger
    arriving() when entering the block to mark previous section to be resolved.
    A dedicated waiting segment of the block is unpowered in case departure is
    not allowed. Trains will stop on waiting segment if unpowered without any
    further action being required. The ClassicBlockSection in not suitable for
    pushed trains.
    """

    def __init__(self, out, previous, auto_await=False):
        super(ClassicBlockSection, self).__init__(
            out, previous, auto_await=auto_await)
        del self._entrance._fsm.onawaiting
        del self._exit._fsm.onwaiting
        del self._exit._fsm.onleavewaiting
        self._exit._fsm.ondeparting = self._ondeparting

    def arrive(self):
        super(ClassicBlockSection, self).arrive()
        super(ClassicBlockSection, self).arrived()

    def arrived(self):
        raise NotImplementedError

    def _ondeparting(self, e):
        self._out.on()
