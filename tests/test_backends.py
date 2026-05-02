import sys
import types

from cloud_stan.backends import DaskExecutor, RayExecutor


def add_one(value):
    return value + 1


class FakeRemoteFunction:
    def __init__(self, func):
        self.func = func

    def remote(self, *args, **kwargs):
        return ("ref", self.func(*args, **kwargs))


class FakeRay:
    def __init__(self):
        self.initialized = False

    def is_initialized(self):
        return self.initialized

    def init(self, **kwargs):
        self.initialized = True

    def remote(self, func):
        return FakeRemoteFunction(func)

    def get(self, value):
        return value[1]

    def shutdown(self):
        self.initialized = False


def test_dask_executor_submits_delayed_work():
    executor = DaskExecutor(scheduler="single-threaded")

    task = executor.submit(add_one, 1)

    assert executor.compute(task) == 2


def test_ray_executor_uses_native_ray_remote(monkeypatch):
    monkeypatch.setitem(sys.modules, "ray", FakeRay())
    executor = RayExecutor()

    ref = executor.submit(add_one, 1)

    assert executor.compute(ref) == 2
