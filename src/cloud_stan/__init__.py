"""Run Stan interfaces on Dask, Dask-on-Ray, or native Ray executors."""

from .backends import DaskExecutor, RayExecutor, compute_dask_on_ray, dask_on_ray_scheduler
from .cmdstanpy import bernoulli_stan_file
from .security import SecurityPolicy

__version__ = "0.1.0"

__all__ = [
    "DaskExecutor",
    "RayExecutor",
    "SecurityPolicy",
    "bernoulli_stan_file",
    "compute_dask_on_ray",
    "dask_on_ray_scheduler",
]
