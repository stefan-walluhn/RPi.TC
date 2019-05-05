from rpitc.element.turnout import Turnout


class TestTurnout:

    def test_straight(self, turnout):
        turnout.switch(Turnout.STRAIGHT)
        assert turnout.status == Turnout.STRAIGHT
