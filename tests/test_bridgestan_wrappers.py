import sys
import types

from cloud_stan import bridgestan as cloud_bridgestan
from stan_integration.bridgestan import dask_bridgestan


class FakeBridgeStanModel:
    def __init__(self, stan_file, data=None, **kwargs):
        self.stan_file = stan_file
        self.data = data
        self.kwargs = kwargs

    def log_density(self, unconstrained_parameters, **kwargs):
        return {
            "method": "log_density",
            "stan_file": self.stan_file,
            "data": self.data,
            "parameters": unconstrained_parameters,
            "kwargs": kwargs,
        }

    def param_unc_num(self):
        return 1


def install_fake_bridgestan(monkeypatch):
    monkeypatch.setitem(sys.modules, "bridgestan", types.SimpleNamespace(StanModel=FakeBridgeStanModel))


def test_log_density_uses_embedded_bernoulli_file(monkeypatch, bernoulli_stan_file):
    install_fake_bridgestan(monkeypatch)

    result = cloud_bridgestan.log_density(
        bernoulli_stan_file,
        [0.0],
        data={"N": 1, "y": [1]},
    ).compute(scheduler="single-threaded")

    assert result["method"] == "log_density"
    assert result["stan_file"] == str(bernoulli_stan_file)
    assert result["data"] == {"N": 1, "y": [1]}
    assert result["parameters"] == [0.0]


def test_generic_bridgestan_model_method_supports_any_method(monkeypatch, bernoulli_stan_file):
    install_fake_bridgestan(monkeypatch)

    result = cloud_bridgestan.delayed_model_method(
        bernoulli_stan_file,
        "param_unc_num",
    ).compute(scheduler="single-threaded")

    assert result == 1


def test_legacy_bridgestan_import_path_reexports_wrappers():
    assert dask_bridgestan.log_density is cloud_bridgestan.log_density
