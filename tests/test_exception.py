from rpitc import PathCollision
from rpitc.trail import Trail
import pytest

class TestException:

    def test_pathcollision(self):
        trail = Trail()
        with pytest.raises(PathCollision) as e:
            raise PathCollision('path collision', trail)
        assert e.value.args[0] == 'path collision'
