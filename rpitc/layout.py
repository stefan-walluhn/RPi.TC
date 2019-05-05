import yaml

from rpitc.element.turnout import Turnout
from rpitc.station.trail import Trail


class Layout(object):
    def __init__(self, raw=None):
        self.raw = raw
        self._trails = {}

    def setup(self):
        def parse_turnouts(turnouts):
            for id, config in turnouts.items():
                yield (id, Turnout())

        def parse_trails(trails, turnouts):
            for id, config in trails.items():
                path = [v for (k,v) in turnouts.items() if k in config]
                yield (id, Trail(path))

        self._turnouts = dict(parse_turnouts(self.raw['turnouts']))
        self._trails = dict(parse_trails(self.raw['trails'], self._turnouts))

    @property
    def turnouts(self):
        return self._turnouts

    @property
    def trails(self):
        return self._trails


class LayoutFactory(object):
    def __init__(self):
        self.layout = None

    def from_file(self, src):
        if not self.layout:
            with open(src, 'r') as src_data:
                layout =  Layout(yaml.load(src_data, Loader=yaml.SafeLoader))
                layout.setup()
                self.layout = layout

        return self.layout


layout_factory = LayoutFactory()
