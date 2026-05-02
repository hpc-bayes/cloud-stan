from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from dask import delayed

from .security import SecurityPolicy, validate_method_name, validate_stan_file


def _cmdstanpy() -> Any:
    try:
        import cmdstanpy
    except ImportError as exc:
        raise RuntimeError("CmdStanPy is required. Install the 'cmdstanpy' extra.") from exc
    return cmdstanpy


def bernoulli_stan_file() -> Path:
    return Path(__file__).resolve().parents[1] / "stan" / "bernoulli.stan"


def build_model(stan_file: str | Path, *, security_policy: SecurityPolicy | None = None, **kwargs: Any) -> Any:
    path = validate_stan_file(stan_file, security_policy)
    return _cmdstanpy().CmdStanModel(stan_file=str(path), **kwargs)


def call_model_method(
    stan_file: str | Path,
    method_name: str,
    *args: Any,
    model_kwargs: dict[str, Any] | None = None,
    security_policy: SecurityPolicy | None = None,
    **kwargs: Any,
) -> Any:
    method = validate_method_name(method_name, security_policy)
    model = build_model(stan_file, security_policy=security_policy, **(model_kwargs or {}))
    return getattr(model, method)(*args, **kwargs)


def delayed_model_method(
    stan_file: str | Path,
    method_name: str,
    *args: Any,
    model_kwargs: dict[str, Any] | None = None,
    security_policy: SecurityPolicy | None = None,
    **kwargs: Any,
) -> Any:
    return delayed(call_model_method)(
        stan_file,
        method_name,
        *args,
        model_kwargs=model_kwargs,
        security_policy=security_policy,
        **kwargs,
    )


def delayed_function(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    return delayed(func)(*args, **kwargs)


def call_function(function_name: str, *args: Any, security_policy: SecurityPolicy | None = None, **kwargs: Any) -> Any:
    function = validate_method_name(function_name, security_policy)
    return getattr(_cmdstanpy(), function)(*args, **kwargs)


def delayed_function_name(
    function_name: str,
    *args: Any,
    security_policy: SecurityPolicy | None = None,
    **kwargs: Any,
) -> Any:
    return delayed(call_function)(function_name, *args, security_policy=security_policy, **kwargs)


def sample(stan_file: str | Path, data: Any = None, *, security_policy: SecurityPolicy | None = None, **kwargs: Any) -> Any:
    return delayed_model_method(stan_file, "sample", data=data, security_policy=security_policy, **kwargs)


def optimize(stan_file: str | Path, data: Any = None, *, security_policy: SecurityPolicy | None = None, **kwargs: Any) -> Any:
    return delayed_model_method(stan_file, "optimize", data=data, security_policy=security_policy, **kwargs)


def variational(stan_file: str | Path, data: Any = None, *, security_policy: SecurityPolicy | None = None, **kwargs: Any) -> Any:
    return delayed_model_method(stan_file, "variational", data=data, security_policy=security_policy, **kwargs)


def generate_quantities(
    stan_file: str | Path,
    previous_fit: Any,
    data: Any = None,
    *,
    security_policy: SecurityPolicy | None = None,
    **kwargs: Any,
) -> Any:
    return delayed_model_method(
        stan_file,
        "generate_quantities",
        previous_fit=previous_fit,
        data=data,
        security_policy=security_policy,
        **kwargs,
    )


def pathfinder(stan_file: str | Path, data: Any = None, *, security_policy: SecurityPolicy | None = None, **kwargs: Any) -> Any:
    return delayed_model_method(stan_file, "pathfinder", data=data, security_policy=security_policy, **kwargs)


def laplace_sample(
    stan_file: str | Path,
    mode: Any,
    data: Any = None,
    *,
    security_policy: SecurityPolicy | None = None,
    **kwargs: Any,
) -> Any:
    return delayed_model_method(stan_file, "laplace_sample", mode=mode, data=data, security_policy=security_policy, **kwargs)


def diagnose(csv_files: Any, *, security_policy: SecurityPolicy | None = None, **kwargs: Any) -> Any:
    return delayed_function_name("diagnose", csv_files, security_policy=security_policy, **kwargs)


def from_csv(path: Any, *, security_policy: SecurityPolicy | None = None, **kwargs: Any) -> Any:
    return delayed_function_name("from_csv", path, security_policy=security_policy, **kwargs)
