from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Callable, Iterable

from dask import delayed


def _resolve(value: Any) -> Any:
    if hasattr(value, "compute"):
        return value.compute()
    return value


def _call_function(func: Callable[..., Any], args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    return func(*args, **kwargs)


def _call_method(target: Any, method_name: str, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    return getattr(target, method_name)(*args, **kwargs)


@dataclass
class DaskExecutor:
    """Small adapter around Dask delayed and distributed clients."""

    client: Any | None = None
    scheduler: Any | None = None

    def submit(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        task = delayed(_call_function)(func, args, kwargs)
        if self.client is not None:
            return self.client.compute(task)
        return task

    def submit_method(self, target: Any, method_name: str, *args: Any, **kwargs: Any) -> Any:
        task = delayed(_call_method)(target, method_name, args, kwargs)
        if self.client is not None:
            return self.client.compute(task)
        return task

    def compute(self, value: Any) -> Any:
        if self.client is not None:
            return self.client.gather(value)
        if hasattr(value, "compute"):
            return value.compute(scheduler=self.scheduler)
        return value

    def map(self, func: Callable[..., Any], items: Iterable[Any], **kwargs: Any) -> list[Any]:
        return [self.submit(func, item, **kwargs) for item in items]


class RayExecutor:
    """Native Ray executor with lazy imports so Ray remains optional."""

    def __init__(self, *, address: str | None = None, init: bool = False, **ray_kwargs: Any) -> None:
        self.address = address
        self.ray_kwargs = ray_kwargs
        self._ray = None
        if init:
            self.start()

    @property
    def ray(self) -> Any:
        if self._ray is None:
            try:
                import ray
            except ImportError as exc:
                raise RuntimeError("Ray is required for RayExecutor. Install the 'ray' extra.") from exc
            self._ray = ray
        return self._ray

    def start(self) -> None:
        if not self.ray.is_initialized():
            init_kwargs = dict(self.ray_kwargs)
            if self.address is not None:
                init_kwargs["address"] = self.address
            self.ray.init(**init_kwargs)

    def submit(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        self.start()
        return self.ray.remote(func).remote(*args, **kwargs)

    def submit_method(self, target: Any, method_name: str, *args: Any, **kwargs: Any) -> Any:
        self.start()
        return self.ray.remote(_call_method).remote(target, method_name, args, kwargs)

    def compute(self, value: Any) -> Any:
        return self.ray.get(value)

    def map(self, func: Callable[..., Any], items: Iterable[Any], **kwargs: Any) -> list[Any]:
        return [self.submit(func, item, **kwargs) for item in items]

    def shutdown(self) -> None:
        if self._ray is not None and self._ray.is_initialized():
            self._ray.shutdown()

    def __enter__(self) -> "RayExecutor":
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        self.shutdown()


@contextmanager
def dask_on_ray_scheduler() -> Any:
    try:
        import dask
        from ray.util.dask import ray_dask_get
    except ImportError as exc:
        raise RuntimeError("Ray and ray.util.dask are required for Dask-on-Ray execution.") from exc

    with dask.config.set(scheduler=ray_dask_get):
        yield


def compute_dask_on_ray(value: Any) -> Any:
    with dask_on_ray_scheduler():
        return _resolve(value)
