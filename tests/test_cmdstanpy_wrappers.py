import sys
import types

from cloud_stan import cmdstanpy as cloud_cmdstanpy
from stan_integration.cmdstanpy import dask_cmdstanpy


class FakeCmdStanModel:
    calls = []

    def __init__(self, stan_file, **kwargs):
        self.stan_file = stan_file
        self.kwargs = kwargs

    def sample(self, **kwargs):
        self.calls.append(("sample", self.stan_file, kwargs))
        return {"method": "sample", "stan_file": self.stan_file, "kwargs": kwargs}

    def optimize(self, **kwargs):
        self.calls.append(("optimize", self.stan_file, kwargs))
        return {"method": "optimize", "stan_file": self.stan_file, "kwargs": kwargs}


def install_fake_cmdstanpy(monkeypatch):
    fake = types.SimpleNamespace(
        CmdStanModel=FakeCmdStanModel,
        diagnose=lambda csv_files, **kwargs: {"csv_files": csv_files, "kwargs": kwargs},
        from_csv=lambda path, **kwargs: {"path": path, "kwargs": kwargs},
    )
    monkeypatch.setitem(sys.modules, "cmdstanpy", fake)


def test_sample_uses_embedded_bernoulli_file(monkeypatch, bernoulli_stan_file, bernoulli_data):
    install_fake_cmdstanpy(monkeypatch)

    result = cloud_cmdstanpy.sample(
        bernoulli_stan_file,
        data=bernoulli_data,
        chains=1,
        iter_warmup=5,
        iter_sampling=5,
    ).compute(scheduler="single-threaded")

    assert result["method"] == "sample"
    assert result["stan_file"] == str(bernoulli_stan_file)
    assert result["kwargs"]["data"] == bernoulli_data
    assert result["kwargs"]["chains"] == 1


def test_generic_cmdstanpy_model_method_supports_any_method(monkeypatch, bernoulli_stan_file):
    install_fake_cmdstanpy(monkeypatch)

    result = cloud_cmdstanpy.delayed_model_method(
        bernoulli_stan_file,
        "optimize",
        data={"N": 1, "y": [1]},
        algorithm="LBFGS",
    ).compute(scheduler="single-threaded")

    assert result["method"] == "optimize"
    assert result["kwargs"]["algorithm"] == "LBFGS"


def test_cmdstanpy_top_level_functions_are_delayed(monkeypatch, bernoulli_stan_file):
    install_fake_cmdstanpy(monkeypatch)

    result = cloud_cmdstanpy.from_csv(bernoulli_stan_file).compute(scheduler="single-threaded")

    assert result["path"] == bernoulli_stan_file


def test_legacy_cmdstanpy_import_path_reexports_wrappers():
    assert dask_cmdstanpy.sample is cloud_cmdstanpy.sample
