from rpitc.io import IO
from rpitc.section import (
    BareEntranceSection,
    BaseEntranceSection,
    BaseExitSection,
    Section)
from rpitc.section.block import (
    BareBlockSection,
    BaseBlockSection,
    BlockSection,
    ClassicBlockSection)
import fysom
import pytest


@pytest.fixture(scope='function')
def previous(mock):
    return mock()


@pytest.fixture(scope='function')
def base_entrance_section(previous):
    return BaseEntranceSection(previous=previous)


@pytest.fixture(scope='function')
def bare_entrance_section(previous):
    return BareEntranceSection(previous=previous)


@pytest.fixture(scope='function')
def base_exit_section():
    return BaseExitSection()


@pytest.fixture(scope='function')
def base_block_section(previous):
    return BaseBlockSection(previous=previous)


@pytest.fixture(scope='function')
def auto_await_block_section(previous, out):
    return BaseBlockSection(previous=previous, auto_await=True)


@pytest.yield_fixture(scope='function')
def block_section(previous, out):
    yield BlockSection(out=out, previous=previous)
    out.off()


@pytest.yield_fixture(scope='function')
def bare_section(previous, out):
    yield BareBlockSection(out=out, previous=previous)
    out.off()


@pytest.yield_fixture(scope='function')
def classic_section(previous, out):
    yield ClassicBlockSection(out=out, previous=previous)
    out.off()


class TestBaseEntranceSection:

    def test_inital_idle(self, base_entrance_section):
        assert base_entrance_section.blocked
        assert base_entrance_section.status == Section.IDLE

    def test_requires_previos_section(self):
        with pytest.raises(TypeError):
            BaseEntranceSection()

    def test_await(self, base_entrance_section):
        base_entrance_section.await()
        assert not base_entrance_section.blocked
        assert base_entrance_section.status == Section.AWAITING

    def test_await_only_once(self, base_entrance_section):
        base_entrance_section.await()
        with pytest.raises(fysom.FysomError):
            base_entrance_section.await()

    def test_arrive(self, base_entrance_section):
        base_entrance_section.await()
        base_entrance_section.arrive()
        assert base_entrance_section.blocked
        assert base_entrance_section.status == Section.ARRIVING

    def test_arrived(self, base_entrance_section):
        base_entrance_section.await()
        base_entrance_section.arrive()
        base_entrance_section.arrived()
        assert base_entrance_section.blocked
        assert base_entrance_section.status == Section.IDLE

    def test_onaawait(self, base_entrance_section):
        base_entrance_section.await()
        base_entrance_section._previous.depart.assert_called_once_with()

    def test_onarrive(self, base_entrance_section):
        base_entrance_section.await()
        base_entrance_section.arrive()
        base_entrance_section._previous.departed.assert_called_once_with()


class TestBareEntranceSection:
    def test_arrive(self, bare_entrance_section):
        bare_entrance_section.await()
        with pytest.raises(NotImplementedError):
            bare_entrance_section.arrive()

    def test_arrived(self, bare_entrance_section):
        bare_entrance_section.await()
        bare_entrance_section.arrived()
        bare_entrance_section._previous.departed.assert_called_once_with()


class TestBaseExitSection:

    def test_request_depart(self, base_exit_section):
        base_exit_section.request_depart()
        assert base_exit_section.status == Section.WAITING
        assert not base_exit_section.can_depart

    def test_request_depart_next_not_blocked(self, base_exit_section):
        base_exit_section._can_depart = True
        base_exit_section.request_depart()
        assert base_exit_section.status == Section.DEPARTING

    def test_depart(self, base_exit_section):
        base_exit_section.request_depart()
        base_exit_section.depart()
        assert base_exit_section.status == Section.DEPARTING

    def test_depart_on_idle(self, base_exit_section):
        base_exit_section.depart()
        assert base_exit_section.status == Section.IDLE

    def test_departed(self, base_exit_section):
        base_exit_section.request_depart()
        base_exit_section.depart()
        base_exit_section.departed()
        assert base_exit_section.status == Section.IDLE

    def test_ondepart(self, base_exit_section):
        base_exit_section.request_depart()
        base_exit_section.depart()
        assert not base_exit_section.can_depart

    def test_ondepart_on_idle(self, base_exit_section):
        base_exit_section.depart()
        assert base_exit_section.can_depart


class TestBaseBlockSection:

    def test_arrived(self, base_block_section):
        base_block_section.await()
        base_block_section.arrive()
        base_block_section.arrived()
        assert base_block_section.blocked
        assert base_block_section._exit.status == Section.WAITING

    def test_arrived_next_not_blocked(self, base_block_section):
        base_block_section._exit._can_depart = True
        base_block_section.await()
        base_block_section.arrive()
        base_block_section.arrived()
        assert base_block_section.blocked
        assert base_block_section._exit.status == Section.DEPARTING

    def test_auto_await_block_init(self, auto_await_block_section):
        assert not auto_await_block_section.blocked
        assert auto_await_block_section._entrance.status == Section.AWAITING

    def test_auto_await_block(self, auto_await_block_section):
        auto_await_block_section.arrive()
        auto_await_block_section.arrived()
        auto_await_block_section.depart()
        auto_await_block_section.departed()
        assert not auto_await_block_section.blocked
        assert auto_await_block_section._entrance.status == Section.AWAITING


class TestBlockSection:

    def test_has_out(self, block_section):
        assert block_section._out.status == IO.OFF

    def test_await(self, block_section):
        block_section.await()
        assert block_section._out.status == IO.ON

    def test_arrive(self, block_section):
        block_section.await()
        block_section.arrive()
        assert block_section._out.status == IO.ON

    def test_arrived(self, block_section):
        block_section.await()
        block_section.arrive()
        block_section.arrived()
        assert block_section._out.status == IO.OFF

    def test_arrived_next_not_blocked(self, block_section):
        block_section._exit._can_depart = True
        block_section.await()
        block_section.arrive()
        block_section.arrived()
        assert block_section._out.status == IO.ON

    def test_resolve(self, block_section):
        block_section.await()
        block_section.arrive()
        block_section.arrived()
        block_section.depart()
        block_section.departed()
        assert block_section._out.status == IO.OFF


class TestBareSection:
    def test_arrive(self, bare_section):
        bare_section.await()
        with pytest.raises(NotImplementedError):
            bare_section.arrive()

    def test_arrived(self, bare_section):
        bare_section.await()
        bare_section.arrived()
        bare_section._entrance._previous.departed.assert_called_once_with()


class TestClassicSection:
    def test_await(self, classic_section):
        classic_section.await()
        assert classic_section._out.status == IO.OFF

    def test_arrive(self, classic_section):
        classic_section.await()
        classic_section.arrive()
        classic_section._entrance._previous.departed.assert_called_once_with()
        assert classic_section._out.status == IO.OFF
        assert classic_section._exit.status == Section.WAITING

    def test_arrive_next_not_blocked(self, classic_section):
        classic_section._exit._can_depart = True
        classic_section.await()
        classic_section.arrive()
        assert classic_section._out.status == IO.ON

    def test_arrived(self, classic_section):
        classic_section.await()
        classic_section.arrive()
        with pytest.raises(NotImplementedError):
            classic_section.arrived()

    def test_depart(self, classic_section):
        classic_section.await()
        classic_section.arrive()
        classic_section.depart()
        assert classic_section._out.status == IO.ON

    def test_departed(self, classic_section):
        classic_section.await()
        classic_section.arrive()
        classic_section.depart()
        classic_section.departed()
        assert classic_section._out.status == IO.OFF
