from rpitc.adapter.logger import Logger
from rpitc.station.trail import Trail, Event

class TestLogger:

    logger = Logger()

    def test_init(self):
        assert isinstance(self.logger, Logger)

    def test_logging(self):
        trail = Trail()
        e = Event(trail, src=Trail.IDLE, dst=Trail.ACTIVE)
        self.logger.update(e)
