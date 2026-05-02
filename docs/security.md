# Security

Running Stan jobs on Dask or Ray means Python callables, model files, data, and
compiled artifacts move across a cluster. Treat workers as trusted execution
nodes and do not submit untrusted code or unreviewed Stan programs.

## Code Safeguards

cloud-stan validates cluster-dispatched model calls by default:

- Stan model paths must exist, be files, and end in `.stan`.
- Private method dispatch such as `__dunder__` methods is rejected.
- Optional `SecurityPolicy` objects can restrict model files to approved roots.
- Optional `SecurityPolicy.allowed_methods` can restrict which CmdStanPy or
  BridgeStan methods may be submitted.

```python
from cloud_stan import SecurityPolicy
from cloud_stan.cmdstanpy import bernoulli_stan_file, sample

policy = SecurityPolicy.from_roots(
    [bernoulli_stan_file().parent],
    allowed_methods={"sample"},
)

task = sample(
    bernoulli_stan_file(),
    data={"N": 3, "y": [0, 1, 1]},
    chains=1,
    security_policy=policy,
)
fit = task.compute()
```

## Cluster Hardening Checklist

- Put Dask and Ray dashboards behind authentication or a private network.
- Do not expose scheduler, head node, object store, or worker ports publicly.
- Use TLS for scheduler and dashboard traffic when the cluster crosses hosts.
- Run workers with least-privilege service accounts.
- Keep cloud credentials out of task arguments and logs.
- Use short-lived credentials for object storage and artifact upload.
- Restrict writable output directories.
- Store Stan data files without secrets when possible.
- Pin dependency versions for production images and rebuild images on security
  updates.
- Avoid compiling arbitrary user-submitted Stan code on shared clusters.

## Trust Boundary

Dask and Ray both execute serialized Python work on workers. The security model
is therefore closer to "remote code execution by authorized users" than to a
sandbox. cloud-stan narrows accidental misuse around method dispatch and model
paths, but it does not sandbox Python, CmdStan, BridgeStan, C++ compilation, or
worker filesystem access.
