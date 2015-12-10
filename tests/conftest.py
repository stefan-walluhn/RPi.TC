from rpitc.adapter import Adapter
from rpitc.element.turnout import Turnout
from rpitc.trail import Trail, Event
import sys
import imp
import pytest
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock


@pytest.fixture(scope='session')
def gpio():
    rpi = imp.new_module("rpi")
    rpi.GPIO = Mock()
    sys.modules['RPi'] = rpi
    sys.modules['RPi.GPIO'] = imp.new_module("gpio")
    return sys


@pytest.fixture(scope='session')
def IO(gpio):
    from rpitc.io import IO
    return IO


# XXX
@pytest.fixture(scope='session')
def Out(gpio):
    from rpitc.io.out import Out
    return Out


@pytest.yield_fixture(scope='class')
def out(gpio):
    from rpitc.io.out import Out
    out = Out(7)
    yield out
    out.off()


@pytest.yield_fixture(scope='class')
def trigger(IO):
    from rpitc.io.trigger import Trigger
    trigger = Trigger(7, delay=1, status=IO.OFF)
    yield trigger
    trigger.out.off()


# XXX
@pytest.yield_fixture(scope='class')
def trigger2(IO):
    from rpitc.io.trigger import Trigger
    trigger = Trigger(5, status=IO.ON, trigger_on=IO.OFF)
    yield trigger
    trigger.out.off()


@pytest.fixture(scope='class')
def switch(out, IO):
    from rpitc.io.switch import Switch
    switch = Switch(out, status=IO.OFF)
    return switch


@pytest.fixture(scope='class')
def turnout():
    return Turnout()


@pytest.yield_fixture(scope='function')
def trail(turnout):
    path = [
        (turnout, Turnout.STRAIGHT),
        (Turnout(), Turnout.TURNOUT),
        (Turnout(), Turnout.STRAIGHT)]
    trail = Trail(path=path)
    yield trail
    trail.resolve()


@pytest.fixture(scope='session')
def observer():
    class Observer(Adapter):

        def __init__(self):
            self.status = None

        def update(self, event):
            self.status = event.dst

    return Observer()
