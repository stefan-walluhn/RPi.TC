from rpitc.element.turnout import Turnout

class TestTurnout:

    def setup_method(self, method):
        self.turnout = Turnout()

    def test_init(self):
        assert isinstance(self.turnout, Turnout)

    def test_straight(self):
        self.turnout.switch(Turnout.STRAIGHT)
        assert self.turnout.status == Turnout.STRAIGHT 
