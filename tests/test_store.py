from rpitc.exceptions import PathCollisionError
from rpitc.store import Store
import pytest


class TestStore:

    def test_singleton(self, store):
        another_store = Store()
        assert store is another_store

    def test_register(self, store, trail):
        store.register(trail.path)
        assert store._paths == [trail.path]

    def test_refuse_colliding_trail(self, store, trail):
        store.register(trail.path)
        with pytest.raises(PathCollisionError) as e:
            store.register(trail.path)
        assert e.value.colliding_path is trail.path

    def test_unregister(self, store, trail):
        store.register(trail.path)
        store.unregister(trail.path)
        assert store._paths == []

