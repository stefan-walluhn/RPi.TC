from fysom import FysomError
from rpitc.adapter import Adapter
from rpitc.element.turnout import Turnout
from rpitc.io import IO
from rpitc.station.gateway import Entrance, Exit
from rpitc.station.trail import Trail
from rpitc.store import Store
import sys
import imp
import pytest


@pytest.fixture(scope='session')
def mock():
    try:
        from unittest.mock import Mock
    except ImportError:
        from mock import Mock
    return Mock


@pytest.fixture(scope='session')
def gpio(mock):
    rpi = imp.new_module("rpi")
    rpi.GPIO = mock()
    sys.modules['RPi'] = rpi
    sys.modules['RPi.GPIO'] = imp.new_module("gpio")
    return sys


@pytest.yield_fixture(scope='class')
def out(gpio):
    from rpitc.io.out import Out
    out = Out(7)
    yield out
    out.off()


@pytest.yield_fixture(scope='class')
def trigger(gpio):
    from rpitc.io.out import Out
    from rpitc.io.trigger import Trigger
    out = Out(5)
    trigger = Trigger(out)
    yield trigger
    out.off()


@pytest.yield_fixture(scope='class')
def switch(gpio):
    from rpitc.io.out import Out
    from rpitc.io.switch import Switch
    out = Out(9)
    switch = Switch(out, status=IO.OFF)
    yield switch
    out.off()


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
    try:
        trail.resolve()
    except FysomError:
        if trail.status is Trail.IDLE: pass

@pytest.yield_fixture(scope='function')
def store():
    store = Store()
    yield store
    for path in store._paths:
        store.unregister(path)
