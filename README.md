# cloud-stan

cloud-stan is a proof-of-concept execution layer for running Stan Python
workloads on Dask, Dask-on-Ray, and native Ray clusters.

It is for Stan users who already have CmdStanPy or BridgeStan programs and want
to move the expensive parts onto distributed compute without rewriting their
model code around a cloud provider SDK.

## Why This Exists

Stan users often have a workflow like this:

1. Write and test a Stan model locally.
2. Run CmdStanPy sampling, optimization, variational inference, or generated
   quantities.
3. Use BridgeStan for log densities, gradients, transforms, or custom inference
   algorithms.
4. Eventually need more CPU, memory, chains, models, simulated datasets, or
   repeated jobs than one machine should handle.

cloud-stan gives those workflows a small distributed execution surface:

- Dask delayed tasks for CmdStanPy and BridgeStan calls.
- Dask-on-Ray execution when Ray should be the cluster runtime.
- Native Ray execution for direct Ray object refs.
- Helm charts and cloud-provider values examples for Kubernetes clusters on
  AWS EKS, Google GKE, and Azure AKS.
- Security checks around model paths and method dispatch.

The embedded `src/stan/bernoulli.stan` model is used as a smoke-test model and
as a minimal example for users wiring up a cluster.

## What This Repo Can Help With

- Run CmdStanPy model methods on Dask or Ray:
  `sample`, `optimize`, `variational`, `generate_quantities`, `pathfinder`,
  `laplace_sample`, plus generic model-method dispatch.
- Run CmdStanPy top-level helpers such as `diagnose` and `from_csv`.
- Run BridgeStan methods on Dask or Ray:
  `log_density`, `log_density_gradient`, `param_unc_num`,
  `param_unc_names`, `constrain_pars`, `unconstrain_pars`, plus generic
  model-method dispatch.
- Use a local Dask scheduler, a remote Dask cluster, Dask-on-Ray, or native Ray.
- Deploy starter Dask and Ray/KubeRay workloads to Kubernetes.
- Adapt provider-specific Helm values for AWS, GCP, and Azure.

## What This Repo Does Not Do

- It does not replace CmdStanPy, CmdStan, BridgeStan, Dask, Ray, or KubeRay.
- It does not install a C++ toolchain, CmdStan, or BridgeStan system
  dependencies on your machines.
- It does not guarantee that arbitrary Stan models compile on every worker.
- It does not manage secrets, IAM, object storage buckets, VPCs, Kubernetes
  clusters, or container registries for you.
- It does not make Dask or Ray a security sandbox. Workers execute Python code.
- It does not automatically optimize Stan model performance, choose priors,
  diagnose sampling pathologies, or fix divergent transitions.
- It does not yet provide a polished production API. The repo is still a POC
  intended to become a useful foundation.

## What You Need

For local development:

- Python 3.9+
- Dask and distributed
- CmdStanPy and a working CmdStan install for CmdStanPy examples
- BridgeStan and its toolchain for BridgeStan examples
- Ray if you want native Ray or Dask-on-Ray

For Kubernetes/cloud use:

- A container image containing this repo/package and all Stan dependencies
- A Kubernetes cluster such as EKS, GKE, or AKS
- Helm 3
- KubeRay installed before using the Ray chart
- Worker nodes with enough CPU and memory for Stan compilation and execution
- A private network or authenticated ingress for dashboards and schedulers
- Cloud identity configured through IRSA, Workload Identity, or Azure Workload
  Identity if jobs write to object storage

## Install

From a checkout:

```bash
python -m pip install -e .
```

Install optional runtime dependencies as needed:

```bash
python -m pip install -e ".[cmdstanpy,bridgestan,ray,test]"
```

For CmdStanPy, you still need CmdStan itself. For BridgeStan, you still need a
working BridgeStan-compatible build environment.

## Quick CmdStanPy Example on Local Dask

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

fit = task.compute(scheduler="threads")
print(fit.summary())
```

## CmdStanPy on a Remote Dask Cluster

```python
from dask.distributed import Client

from cloud_stan.cmdstanpy import bernoulli_stan_file, optimize

client = Client("tcp://your-dask-scheduler:8786")
data = {"N": 10, "y": [0, 1, 0, 1, 1, 0, 1, 1, 0, 1]}

task = optimize(bernoulli_stan_file(), data=data, algorithm="LBFGS")
future = client.compute(task)
mle = future.result()
```

## CmdStanPy with Dask-on-Ray

```python
import ray

from cloud_stan.backends import compute_dask_on_ray
from cloud_stan.cmdstanpy import bernoulli_stan_file, variational

ray.init(address="auto")

data = {"N": 10, "y": [0, 1, 0, 1, 1, 0, 1, 1, 0, 1]}
task = variational(bernoulli_stan_file(), data=data, algorithm="meanfield")
fit = compute_dask_on_ray(task)
```

## CmdStanPy on Native Ray

```python
from cloud_stan.backends import RayExecutor
from cloud_stan.cmdstanpy import bernoulli_stan_file, call_model_method

data = {"N": 10, "y": [0, 1, 0, 1, 1, 0, 1, 1, 0, 1]}

with RayExecutor(address="auto") as ray:
    ref = ray.submit(
        call_model_method,
        bernoulli_stan_file(),
        "sample",
        data=data,
        chains=1,
        iter_warmup=100,
        iter_sampling=100,
    )
    fit = ray.compute(ref)
```

## BridgeStan Example

```python
from cloud_stan.bridgestan import log_density, log_density_gradient
from cloud_stan.cmdstanpy import bernoulli_stan_file

data = {"N": 10, "y": [0, 1, 0, 1, 1, 0, 1, 1, 0, 1]}
theta_unc = [0.0]

lp = log_density(bernoulli_stan_file(), theta_unc, data=data).compute()
lp2, grad = log_density_gradient(bernoulli_stan_file(), theta_unc, data=data).compute()
```

## Security Policy Example

Use `SecurityPolicy` when accepting model paths or method choices from a config
file, API, or user input.

```python
from cloud_stan import SecurityPolicy
from cloud_stan.cmdstanpy import bernoulli_stan_file, sample

stan_file = bernoulli_stan_file()
policy = SecurityPolicy.from_roots(
    [stan_file.parent],
    allowed_methods={"sample"},
)

task = sample(
    stan_file,
    data={"N": 3, "y": [0, 1, 1]},
    chains=1,
    security_policy=policy,
)
fit = task.compute()
```

This validates that the Stan file is under an approved root and that only the
allowed method can be dispatched through the wrapper.

## Kubernetes and Cloud Providers

This repo includes starter Helm charts:

- `stan_dask_chart`: Dask scheduler, Dask workers, and an optional cloud-stan
  Kubernetes Job.
- `stan_ray_chart/ray_cluster`: KubeRay `RayCluster` and an optional cloud-stan
  Kubernetes Job.

Example provider values live under:

- `examples/cloud/aws`
- `examples/cloud/gcp`
- `examples/cloud/azure`

Install Dask:

```bash
helm upgrade --install cloud-stan-dask ./stan_dask_chart \
  --namespace cloud-stan \
  --create-namespace \
  --values examples/cloud/aws/dask-values.yaml
```

Install KubeRay first, then Ray:

```bash
helm repo add kuberay https://ray-project.github.io/kuberay-helm/
helm repo update
helm upgrade --install kuberay-operator kuberay/kuberay-operator \
  --namespace kuberay-system \
  --create-namespace

helm upgrade --install cloud-stan-ray ./stan_ray_chart/ray_cluster \
  --namespace cloud-stan \
  --create-namespace \
  --values examples/cloud/aws/ray-values.yaml
```

The AWS, GCP, and Azure values files are templates. Replace the image
repositories, identity annotations, regions, project IDs, and output URIs before
using them.

## CI/CD and Docker

The repository includes GitHub Actions workflows:

- `.github/workflows/ci.yml` runs unit tests on Python 3.11, 3.12, and 3.13,
  compiles Python sources, lints/renders Helm charts, and builds the Docker
  image without pushing it.
- `.github/workflows/docker-publish.yml` publishes images to GitHub Container
  Registry on `main`, version tags such as `v0.1.0`, or manual dispatch.

Build the image locally:

```bash
docker build \
  --build-arg INSTALL_EXTRAS=cmdstanpy,bridgestan,ray \
  --build-arg INSTALL_CMDSTAN=false \
  -t cloud-stan:dev .
```

Build with CmdStan included:

```bash
docker build \
  --build-arg INSTALL_EXTRAS=cmdstanpy,bridgestan,ray \
  --build-arg INSTALL_CMDSTAN=true \
  --build-arg CMDSTAN_VERSION=2.37.0 \
  -t cloud-stan:cmdstan .
```

The default image installs the Python interfaces and cluster runtime packages,
but does not download CmdStan. That keeps CI builds lighter. Production images
should pin package versions and usually preinstall CmdStan or BridgeStan build
artifacts so worker pods do not compile everything at startup.

## Example Entrypoints

The Helm job examples point at these modules:

- `examples.run_cmdstanpy_dask`
- `examples.run_cmdstanpy_ray`
- `examples.run_bridgestan_dask`
- `examples.run_bridgestan_ray`

Change `stanJob.command` in a values file to switch between them.

## Practical Guidance

- Start with the Bernoulli model to verify your local environment or cluster.
- Build one container image for Dask workers that includes cloud-stan,
  CmdStanPy, BridgeStan, CmdStan, BridgeStan dependencies, and compilers.
- Use the same image and dependency versions on the scheduler, workers, Ray
  head, Ray workers, and job pods when possible.
- Keep CmdStan output paths on shared storage or collect results before worker
  pods exit.
- Avoid public scheduler and dashboard endpoints.
- Pin image tags and Python package versions for repeatable runs.
- Compile models ahead of time in your image if startup latency matters.

## Tests

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q
```

The unit tests use fake CmdStanPy and BridgeStan modules so they verify the
cloud-stan scheduling behavior without requiring a local CmdStan or BridgeStan
toolchain.

## More Documentation

- [Cluster execution](docs/clusters.md)
- [CmdStanPy wrappers](docs/cmdstanpy.md)
- [BridgeStan wrappers](docs/bridgestan.md)
- [Security](docs/security.md)
- [Helm charts](docs/helm.md)
- [Cloud provider examples](docs/cloud-providers.md)
