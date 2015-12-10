from abc import ABCMeta, abstractmethod


class Adapter:
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, event):
        pass
