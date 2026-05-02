# cloud-stan

A small execution layer for running Stan Python interfaces on Dask, Dask-on-Ray,
or native Ray.

The current proof of concept focuses on:

- CmdStanPy model methods such as `sample`, `optimize`, `variational`,
  `generate_quantities`, `pathfinder`, and `laplace_sample`
- BridgeStan model methods such as `log_density`, `log_density_gradient`,
  `constrain_pars`, and `unconstrain_pars`
- Generic method wrappers so new CmdStanPy or BridgeStan APIs can be scheduled
  without adding a new wrapper first
- A standalone embedded Bernoulli model at `src/stan/bernoulli.stan`

## Example

```python
from cloud_stan.cmdstanpy import bernoulli_stan_file, sample

data = {"N": 10, "y": [0, 1, 0, 1, 1, 0, 1, 1, 0, 1]}
task = sample(
    bernoulli_stan_file(),
    data=data,
    chains=1,
    iter_warmup=100,
    iter_sampling=100,
)
fit = task.compute()
```

BridgeStan works the same way:

```python
from cloud_stan.bridgestan import log_density
from cloud_stan.cmdstanpy import bernoulli_stan_file

task = log_density(bernoulli_stan_file(), [0.0], data={"N": 1, "y": [1]})
value = task.compute()
```

## Tests

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q
```

The unit tests use fake CmdStanPy and BridgeStan modules so they verify the
cloud-stan scheduling behavior without requiring a local CmdStan or BridgeStan
toolchain.

## Documentation

- [Cluster execution](docs/clusters.md)
- [CmdStanPy wrappers](docs/cmdstanpy.md)
- [BridgeStan wrappers](docs/bridgestan.md)
- [Security](docs/security.md)
