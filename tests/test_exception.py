from rpitc.exceptions import PathCollisionError
from rpitc.station.trail import Trail
import pytest


class TestException:

    def test_pathcollision(self):
        trail = Trail()
        with pytest.raises(PathCollisionError) as e:
            raise PathCollisionError('path collision', trail)
        assert e.value.colliding_trail == trail
