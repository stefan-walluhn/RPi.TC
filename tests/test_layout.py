import pytest

from rpitc.layout import Layout, layout_factory


@pytest.fixture
def layout(shared_datadir):
    return layout_factory.from_file(shared_datadir / 'layout.yml')


class TestLayout(object):
    def test_layout(self, layout):
        assert isinstance(layout, Layout)

    def test_layout_from_file(self, layout):
        assert 'trails' in layout.raw

    def test_layout_turnouts(self, layout):
        assert layout.turnouts.keys() == layout.raw['turnouts'].keys()

    def test_layout_turnouts_readonly(self, layout):
        with pytest.raises(AttributeError):
            layout.turnouts = {'invalid': 'trail'}

    def test_layout_trails(self, layout):
        assert layout.trails.keys() == layout.raw['trails'].keys()

    def test_layout_trails_readonly(self, layout):
        with pytest.raises(AttributeError):
            layout.trails = {'invalid': 'trail'}

    def test_layout_turnout_in_trails(self, layout):
        turnout_a = layout.turnouts['test_turnout_a']
        turnout_b = layout.turnouts['test_turnout_b']

        assert turnout_a in layout.trails['test_trail_a'].path
        assert turnout_b in layout.trails['test_trail_a'].path
        assert turnout_a not in layout.trails['test_trail_b'].path
        assert turnout_b in layout.trails['test_trail_b'].path
