# CmdStanPy Wrappers

All CmdStanPy wrappers return Dask delayed tasks. Use `.compute()` for local
Dask, `compute_dask_on_ray(task)` for Dask-on-Ray, or `RayExecutor.submit(...)`
with `call_model_method` / `call_function` for native Ray.

Shared setup:

```python
from cloud_stan.backends import RayExecutor, compute_dask_on_ray
from cloud_stan.cmdstanpy import (
    bernoulli_stan_file,
    call_function,
    call_model_method,
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

stan_file = bernoulli_stan_file()
data = {"N": 10, "y": [0, 1, 0, 1, 1, 0, 1, 1, 0, 1]}
```

## sample

```python
fit = sample(stan_file, data=data, chains=1).compute()
```

```python
fit = compute_dask_on_ray(sample(stan_file, data=data, chains=1))
```

```python
with RayExecutor(address="auto") as ray:
    ref = ray.submit(call_model_method, stan_file, "sample", data=data, chains=1)
    fit = ray.compute(ref)
```

## optimize

```python
mle = optimize(stan_file, data=data, algorithm="LBFGS").compute()
```

```python
mle = compute_dask_on_ray(optimize(stan_file, data=data, algorithm="LBFGS"))
```

```python
with RayExecutor(address="auto") as ray:
    ref = ray.submit(call_model_method, stan_file, "optimize", data=data, algorithm="LBFGS")
    mle = ray.compute(ref)
```

## variational

```python
vb = variational(stan_file, data=data, algorithm="meanfield").compute()
```

```python
vb = compute_dask_on_ray(variational(stan_file, data=data, algorithm="meanfield"))
```

```python
with RayExecutor(address="auto") as ray:
    ref = ray.submit(call_model_method, stan_file, "variational", data=data, algorithm="meanfield")
    vb = ray.compute(ref)
```

## generate_quantities

`previous_fit` is normally a `CmdStanMCMC`, `CmdStanMLE`, or compatible fit
object produced by CmdStanPy.

```python
gq = generate_quantities(stan_file, previous_fit=fit, data=data).compute()
```

```python
gq = compute_dask_on_ray(generate_quantities(stan_file, previous_fit=fit, data=data))
```

```python
with RayExecutor(address="auto") as ray:
    ref = ray.submit(call_model_method, stan_file, "generate_quantities", previous_fit=fit, data=data)
    gq = ray.compute(ref)
```

## pathfinder

```python
pf = pathfinder(stan_file, data=data).compute()
```

```python
pf = compute_dask_on_ray(pathfinder(stan_file, data=data))
```

```python
with RayExecutor(address="auto") as ray:
    ref = ray.submit(call_model_method, stan_file, "pathfinder", data=data)
    pf = ray.compute(ref)
```

## laplace_sample

`mode` is normally a previous CmdStanPy optimization or pathfinder result.

```python
laplace = laplace_sample(stan_file, mode=mle, data=data).compute()
```

```python
laplace = compute_dask_on_ray(laplace_sample(stan_file, mode=mle, data=data))
```

```python
with RayExecutor(address="auto") as ray:
    ref = ray.submit(call_model_method, stan_file, "laplace_sample", mode=mle, data=data)
    laplace = ray.compute(ref)
```

## diagnose

```python
report = diagnose(fit.runset.csv_files).compute()
```

```python
report = compute_dask_on_ray(diagnose(fit.runset.csv_files))
```

```python
with RayExecutor(address="auto") as ray:
    ref = ray.submit(call_function, "diagnose", fit.runset.csv_files)
    report = ray.compute(ref)
```

## from_csv

```python
fit_from_disk = from_csv(fit.runset.csv_files).compute()
```

```python
fit_from_disk = compute_dask_on_ray(from_csv(fit.runset.csv_files))
```

```python
with RayExecutor(address="auto") as ray:
    ref = ray.submit(call_function, "from_csv", fit.runset.csv_files)
    fit_from_disk = ray.compute(ref)
```

## delayed_model_method

Use this for CmdStanPy model methods that do not yet have a named convenience
wrapper.

```python
result = delayed_model_method(stan_file, "sample", data=data, chains=1).compute()
```

```python
result = compute_dask_on_ray(delayed_model_method(stan_file, "sample", data=data, chains=1))
```

```python
with RayExecutor(address="auto") as ray:
    ref = ray.submit(call_model_method, stan_file, "sample", data=data, chains=1)
    result = ray.compute(ref)
```
