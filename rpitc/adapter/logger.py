from rpitc.adapter import Adapter
import logging


class Logger(Adapter):

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    
    def update(self, event):
        self.logger.info(
                "{} changed status from <{}> to <{}>".format(
                    event.trail,
                    event.src,
                    event.dst))
