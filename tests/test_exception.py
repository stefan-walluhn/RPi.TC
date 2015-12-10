from rpitc import PathCollisionError, SectionBlockedError
from rpitc.trail import Trail
import pytest


class TestException:

    def test_pathcollision(self):
        trail = Trail()
        with pytest.raises(PathCollisionError) as e:
            raise PathCollisionError('path collision', trail)
        assert e.value.colliding_trail == trail

    def test_blocktaken(self):
        with pytest.raises(SectionBlockedError) as e:
            raise SectionBlockedError('section is blocked')
        assert e.errisinstance(SectionBlockedError)
