"""Backward-compatible CmdStanPy-on-Dask wrappers."""

from cloud_stan.cmdstanpy import (
    bernoulli_stan_file,
    build_model,
    call_function,
    call_model_method,
    delayed_function,
    delayed_function_name,
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

__all__ = [
    "bernoulli_stan_file",
    "build_model",
    "call_function",
    "call_model_method",
    "delayed_function",
    "delayed_function_name",
    "delayed_model_method",
    "diagnose",
    "from_csv",
    "generate_quantities",
    "laplace_sample",
    "optimize",
    "pathfinder",
    "sample",
    "variational",
]
