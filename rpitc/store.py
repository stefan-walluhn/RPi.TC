from rpitc.exceptions import PathCollisionError
import threading


class Store(object):
    class __Store__(object):
        def __init__(self):
            self._paths = []
            self.__lock__ = threading.Lock()

        def register(self, path):
            with self.__lock__:
                for p in self._paths:
                    for element in path:
                        if element in p:
                            raise PathCollisionError(
                                'path collision detected', p)
                self._paths.append(path)

        def unregister(self, path):
            self._paths.remove(path)

    __instance__ = None
    def __new__(cls):
        if not Store.__instance__:
            Store.__instance__ = Store.__Store__()
        return Store.__instance__
