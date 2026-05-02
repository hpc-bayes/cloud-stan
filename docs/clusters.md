# Cluster Execution

cloud-stan supports three execution styles.

## Plain Dask

Use this when you have a Dask scheduler or want local Dask execution.

```python
from dask.distributed import Client

from cloud_stan.backends import DaskExecutor
from cloud_stan.cmdstanpy import bernoulli_stan_file, sample

client = Client("tcp://scheduler:8786")
executor = DaskExecutor(client=client)

task = sample(bernoulli_stan_file(), data={"N": 3, "y": [0, 1, 1]}, chains=1)
future = executor.submit(lambda x: x.compute(), task)
fit = executor.compute(future)
```

For local execution you can skip `Client` and call `task.compute()`, or use
`DaskExecutor(scheduler="threads")`.

## Dask on Ray

Use this when you want the Dask graph API but Ray should run the tasks.

```python
import ray

from cloud_stan.backends import compute_dask_on_ray
from cloud_stan.cmdstanpy import bernoulli_stan_file, sample

ray.init(address="auto")

task = sample(bernoulli_stan_file(), data={"N": 3, "y": [0, 1, 1]}, chains=1)
fit = compute_dask_on_ray(task)
```

## Native Ray

Use this when you want Ray object refs directly.

```python
from cloud_stan.backends import RayExecutor
from cloud_stan.cmdstanpy import bernoulli_stan_file, call_model_method

with RayExecutor(address="auto") as executor:
    ref = executor.submit(
        call_model_method,
        bernoulli_stan_file(),
        "sample",
        data={"N": 3, "y": [0, 1, 1]},
        chains=1,
    )
    fit = executor.compute(ref)
```

## Operational Notes

- Install the Stan interface and toolchain on every worker that may compile or
  run a model.
- Keep the same `cmdstanpy`, `bridgestan`, Dask, and Ray versions on all nodes.
- Prefer writing CmdStan output to worker-local scratch paths or a shared
  filesystem that all workers can access.
- Compile once per worker image when possible. Runtime compilation is useful for
  exploration but slower and expands the security boundary.
