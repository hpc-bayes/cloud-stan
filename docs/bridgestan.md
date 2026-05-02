# BridgeStan Wrappers

All BridgeStan wrappers return Dask delayed tasks. Use `.compute()` for local
Dask, `compute_dask_on_ray(task)` for Dask-on-Ray, or `RayExecutor.submit(...)`
with `call_model_method` for native Ray.

Shared setup:

```python
from cloud_stan.backends import RayExecutor, compute_dask_on_ray
from cloud_stan.bridgestan import (
    call_model_method,
    constrain_pars,
    delayed_model_method,
    log_density,
    log_density_gradient,
    param_unc_names,
    param_unc_num,
    unconstrain_pars,
)
from cloud_stan.cmdstanpy import bernoulli_stan_file

stan_file = bernoulli_stan_file()
data = {"N": 10, "y": [0, 1, 0, 1, 1, 0, 1, 1, 0, 1]}
theta_unc = [0.0]
theta = [0.5]
```

## log_density

```python
lp = log_density(stan_file, theta_unc, data=data).compute()
```

```python
lp = compute_dask_on_ray(log_density(stan_file, theta_unc, data=data))
```

```python
with RayExecutor(address="auto") as ray:
    ref = ray.submit(call_model_method, stan_file, "log_density", theta_unc, data=data)
    lp = ray.compute(ref)
```

## log_density_gradient

```python
lp, grad = log_density_gradient(stan_file, theta_unc, data=data).compute()
```

```python
lp, grad = compute_dask_on_ray(log_density_gradient(stan_file, theta_unc, data=data))
```

```python
with RayExecutor(address="auto") as ray:
    ref = ray.submit(call_model_method, stan_file, "log_density_gradient", theta_unc, data=data)
    lp, grad = ray.compute(ref)
```

## param_unc_num

```python
num = param_unc_num(stan_file, data=data).compute()
```

```python
num = compute_dask_on_ray(param_unc_num(stan_file, data=data))
```

```python
with RayExecutor(address="auto") as ray:
    ref = ray.submit(call_model_method, stan_file, "param_unc_num", data=data)
    num = ray.compute(ref)
```

## param_unc_names

```python
names = param_unc_names(stan_file, data=data).compute()
```

```python
names = compute_dask_on_ray(param_unc_names(stan_file, data=data))
```

```python
with RayExecutor(address="auto") as ray:
    ref = ray.submit(call_model_method, stan_file, "param_unc_names", data=data)
    names = ray.compute(ref)
```

## constrain_pars

```python
constrained = constrain_pars(stan_file, theta_unc, data=data).compute()
```

```python
constrained = compute_dask_on_ray(constrain_pars(stan_file, theta_unc, data=data))
```

```python
with RayExecutor(address="auto") as ray:
    ref = ray.submit(call_model_method, stan_file, "constrain_pars", theta_unc, data=data)
    constrained = ray.compute(ref)
```

## unconstrain_pars

```python
unconstrained = unconstrain_pars(stan_file, theta, data=data).compute()
```

```python
unconstrained = compute_dask_on_ray(unconstrain_pars(stan_file, theta, data=data))
```

```python
with RayExecutor(address="auto") as ray:
    ref = ray.submit(call_model_method, stan_file, "unconstrain_pars", theta, data=data)
    unconstrained = ray.compute(ref)
```

## delayed_model_method

Use this for BridgeStan model methods that do not yet have a named convenience
wrapper.

```python
result = delayed_model_method(stan_file, "log_density", theta_unc, data=data).compute()
```

```python
result = compute_dask_on_ray(delayed_model_method(stan_file, "log_density", theta_unc, data=data))
```

```python
with RayExecutor(address="auto") as ray:
    ref = ray.submit(call_model_method, stan_file, "log_density", theta_unc, data=data)
    result = ray.compute(ref)
```
