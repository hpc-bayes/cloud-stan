"""CmdStanPy helpers for Dask graphs executed with Ray's Dask scheduler."""

from typing import Any

from cloud_stan.backends import compute_dask_on_ray
from cloud_stan.cmdstanpy import (
    delayed_model_method,
    diagnose,
    from_csv,
    generate_quantities,
    laplace_sample,
    optimize,
    pathfinder,
    sample,
    variational,
)


def run_on_ray(value: Any) -> Any:
    return compute_dask_on_ray(value)


__all__ = [
    "delayed_model_method",
    "diagnose",
    "from_csv",
    "generate_quantities",
    "laplace_sample",
    "optimize",
    "pathfinder",
    "run_on_ray",
    "sample",
    "variational",
]
