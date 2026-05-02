from pathlib import Path

import pytest

from cloud_stan.security import SecurityPolicy, validate_method_name, validate_stan_file


def test_validate_stan_file_accepts_embedded_model(bernoulli_stan_file):
    assert validate_stan_file(bernoulli_stan_file) == bernoulli_stan_file.resolve()


def test_validate_stan_file_rejects_non_stan_file(tmp_path):
    data_file = tmp_path / "data.json"
    data_file.write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match="'.stan'"):
        validate_stan_file(data_file)


def test_security_policy_restricts_model_roots(tmp_path, bernoulli_stan_file):
    policy = SecurityPolicy.from_roots([tmp_path])

    with pytest.raises(ValueError, match="outside the allowed roots"):
        validate_stan_file(bernoulli_stan_file, policy)


def test_method_validation_rejects_private_methods():
    with pytest.raises(ValueError, match="Private methods"):
        validate_method_name("__getattribute__")


def test_method_validation_respects_allowlist():
    policy = SecurityPolicy(allowed_methods=frozenset({"sample"}))

    assert validate_method_name("sample", policy) == "sample"
    with pytest.raises(ValueError, match="not allowed"):
        validate_method_name("optimize", policy)
