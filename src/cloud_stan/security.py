from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class SecurityPolicy:
    """Execution policy for cluster-submitted Stan work."""

    allowed_stan_roots: tuple[Path, ...] = ()
    allowed_methods: frozenset[str] | None = None
    allow_private_methods: bool = False

    @classmethod
    def from_roots(
        cls,
        roots: Iterable[str | Path],
        *,
        allowed_methods: Iterable[str] | None = None,
        allow_private_methods: bool = False,
    ) -> "SecurityPolicy":
        return cls(
            allowed_stan_roots=tuple(Path(root).resolve() for root in roots),
            allowed_methods=frozenset(allowed_methods) if allowed_methods is not None else None,
            allow_private_methods=allow_private_methods,
        )


def validate_method_name(method_name: str, policy: SecurityPolicy | None = None) -> str:
    if not isinstance(method_name, str) or not method_name:
        raise ValueError("method_name must be a non-empty string.")
    if "." in method_name:
        raise ValueError("method_name must name a direct public method, not an attribute path.")

    active_policy = policy or SecurityPolicy()
    if not active_policy.allow_private_methods and method_name.startswith("_"):
        raise ValueError("Private methods cannot be submitted to a cluster wrapper.")
    if active_policy.allowed_methods is not None and method_name not in active_policy.allowed_methods:
        raise ValueError(f"Method '{method_name}' is not allowed by the security policy.")
    return method_name


def validate_stan_file(stan_file: str | Path, policy: SecurityPolicy | None = None) -> Path:
    path = Path(stan_file).expanduser().resolve()
    if path.suffix != ".stan":
        raise ValueError("Stan model path must end in '.stan'.")
    if not path.exists():
        raise FileNotFoundError(path)
    if not path.is_file():
        raise ValueError(f"Stan model path is not a file: {path}")

    active_policy = policy or SecurityPolicy()
    if active_policy.allowed_stan_roots and not any(path.is_relative_to(root) for root in active_policy.allowed_stan_roots):
        raise ValueError(f"Stan model path is outside the allowed roots: {path}")
    return path
