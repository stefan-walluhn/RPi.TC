from rpitc.adapter import Adapter
from rpitc.section import Section
from rpitc.element.turnout import Turnout
from rpitc.io import IO
from rpitc.station.gateway import Entrance, Exit
from rpitc.station.trail import Trail, Event
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
    trigger = Trigger(out, delay=0.1, status=IO.OFF)
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


@pytest.fixture(scope='function')
def section(out):
    return Section(out=out, previous=Mock())


@pytest.fixture(scope='function')
def entrance():
    return Entrance(previous=Mock())


@pytest.fixture(scope='function')
def exit():
    return Exit()


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
