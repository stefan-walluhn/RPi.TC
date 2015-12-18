from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass


class IO(object):
    ON = True
    OFF = False


class BaseOut(with_metaclass(ABCMeta)):

    def __init__(self, status=IO.OFF):
        self._status = status

    @property
    def status(self):
        return self._status

    @abstractmethod
    def _on(self):
        return IO.ON

    @abstractmethod
    def _off(self):
        return IO.OFF

    def on(self):
        self._status = self._on()

    def off(self):
        self._status = self._off()

    def toggle(self):
        if self.status is IO.OFF:
            self.on()
        else:
            self.off()
