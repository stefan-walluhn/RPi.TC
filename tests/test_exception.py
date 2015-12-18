from rpitc.exceptions import PathCollisionError
import pytest


class TestException:

    def test_pathcollision(self, trail):
        with pytest.raises(PathCollisionError) as e:
            raise PathCollisionError('path collision', trail.path)
        assert e.value.colliding_path == trail.path
