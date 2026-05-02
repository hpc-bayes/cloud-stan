from __future__ import annotations

from pathlib import Path
from typing import Any

from dask import delayed

from .security import SecurityPolicy, validate_method_name, validate_stan_file


def _bridgestan() -> Any:
    try:
        import bridgestan
    except ImportError as exc:
        raise RuntimeError("BridgeStan is required. Install the 'bridgestan' extra.") from exc
    return bridgestan


def build_model(
    stan_file: str | Path,
    data: Any = None,
    *,
    security_policy: SecurityPolicy | None = None,
    **kwargs: Any,
) -> Any:
    path = validate_stan_file(stan_file, security_policy)
    return _bridgestan().StanModel(str(path), data, **kwargs)


def call_model_method(
    stan_file: str | Path,
    method_name: str,
    *args: Any,
    data: Any = None,
    model_kwargs: dict[str, Any] | None = None,
    security_policy: SecurityPolicy | None = None,
    **kwargs: Any,
) -> Any:
    method = validate_method_name(method_name, security_policy)
    model_args = dict(model_kwargs or {})
    if data is not None:
        model_args["data"] = data
    model = build_model(stan_file, security_policy=security_policy, **model_args)
    return getattr(model, method)(*args, **kwargs)


def delayed_model_method(
    stan_file: str | Path,
    method_name: str,
    *args: Any,
    data: Any = None,
    model_kwargs: dict[str, Any] | None = None,
    security_policy: SecurityPolicy | None = None,
    **kwargs: Any,
) -> Any:
    return delayed(call_model_method)(
        stan_file,
        method_name,
        *args,
        data=data,
        model_kwargs=model_kwargs,
        security_policy=security_policy,
        **kwargs,
    )


def log_density(
    stan_file: str | Path,
    unconstrained_parameters: Any,
    data: Any = None,
    *,
    security_policy: SecurityPolicy | None = None,
    **kwargs: Any,
) -> Any:
    return delayed_model_method(
        stan_file,
        "log_density",
        unconstrained_parameters,
        data=data,
        security_policy=security_policy,
        **kwargs,
    )


def log_density_gradient(
    stan_file: str | Path,
    unconstrained_parameters: Any,
    data: Any = None,
    *,
    security_policy: SecurityPolicy | None = None,
    **kwargs: Any,
) -> Any:
    return delayed_model_method(
        stan_file,
        "log_density_gradient",
        unconstrained_parameters,
        data=data,
        security_policy=security_policy,
        **kwargs,
    )


def param_unc_num(stan_file: str | Path, data: Any = None, *, security_policy: SecurityPolicy | None = None, **kwargs: Any) -> Any:
    return delayed_model_method(stan_file, "param_unc_num", data=data, security_policy=security_policy, **kwargs)


def param_unc_names(stan_file: str | Path, data: Any = None, *, security_policy: SecurityPolicy | None = None, **kwargs: Any) -> Any:
    return delayed_model_method(stan_file, "param_unc_names", data=data, security_policy=security_policy, **kwargs)


def constrain_pars(
    stan_file: str | Path,
    unconstrained_parameters: Any,
    data: Any = None,
    *,
    security_policy: SecurityPolicy | None = None,
    **kwargs: Any,
) -> Any:
    return delayed_model_method(
        stan_file,
        "constrain_pars",
        unconstrained_parameters,
        data=data,
        security_policy=security_policy,
        **kwargs,
    )


def unconstrain_pars(
    stan_file: str | Path,
    constrained_parameters: Any,
    data: Any = None,
    *,
    security_policy: SecurityPolicy | None = None,
    **kwargs: Any,
) -> Any:
    return delayed_model_method(
        stan_file,
        "unconstrain_pars",
        constrained_parameters,
        data=data,
        security_policy=security_policy,
        **kwargs,
    )
