from rpitc import PathCollision
import threading


class Store:

    instance = None

    def __init__(self):
        if not Store.instance:
            Store.instance = Store.__Store()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __Store:

        trails = []

        def __init__(self):
            self.lock = threading.Lock()

        def register(self, trail):
            with self.lock:
                for stored_trail in self.trails:
                    for turnout in trail.path:
                        if turnout in stored_trail.path:
                            raise PathCollision('path collision detected', stored_trail)
                self.trails.append(trail)

        def unregister(self, trail):
            try:
                self.trails.remove(trail)
            except ValueError:
                pass
