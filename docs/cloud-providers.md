# Cloud Provider Examples

The examples under `examples/cloud` are provider-specific values files for the
in-repo Helm charts. They assume you build and publish a cloud-stan image that
contains this package, CmdStanPy, BridgeStan, CmdStan/BridgeStan toolchains, Ray
or Dask as needed, and your job entrypoint.

## AWS EKS

Files:

- `examples/cloud/aws/dask-values.yaml`
- `examples/cloud/aws/ray-values.yaml`

The examples use EKS IRSA annotations on the service account.

```bash
helm upgrade --install cloud-stan-dask ./stan_dask_chart \
  --namespace cloud-stan \
  --create-namespace \
  --values examples/cloud/aws/dask-values.yaml
```

```bash
helm upgrade --install cloud-stan-ray ./stan_ray_chart/ray_cluster \
  --namespace cloud-stan \
  --create-namespace \
  --values examples/cloud/aws/ray-values.yaml
```

## Google GKE

Files:

- `examples/cloud/gcp/dask-values.yaml`
- `examples/cloud/gcp/ray-values.yaml`

The examples use GKE Workload Identity annotations on the service account.

```bash
helm upgrade --install cloud-stan-dask ./stan_dask_chart \
  --namespace cloud-stan \
  --create-namespace \
  --values examples/cloud/gcp/dask-values.yaml
```

```bash
helm upgrade --install cloud-stan-ray ./stan_ray_chart/ray_cluster \
  --namespace cloud-stan \
  --create-namespace \
  --values examples/cloud/gcp/ray-values.yaml
```

## Azure AKS

Files:

- `examples/cloud/azure/dask-values.yaml`
- `examples/cloud/azure/ray-values.yaml`

The examples use Azure Workload Identity labels and annotations.

```bash
helm upgrade --install cloud-stan-dask ./stan_dask_chart \
  --namespace cloud-stan \
  --create-namespace \
  --values examples/cloud/azure/dask-values.yaml
```

```bash
helm upgrade --install cloud-stan-ray ./stan_ray_chart/ray_cluster \
  --namespace cloud-stan \
  --create-namespace \
  --values examples/cloud/azure/ray-values.yaml
```

## Running the Bernoulli Examples

Use a job image with one of these module entrypoints:

- `examples.run_cmdstanpy_dask`
- `examples.run_cmdstanpy_ray`
- `examples.run_bridgestan_dask`
- `examples.run_bridgestan_ray`

The values files default to CmdStanPy examples. Change `stanJob.command` to run
BridgeStan or a project-specific module.

## Notes

- Pin image tags for production.
- Put output in provider object storage using workload identity, not static keys.
- Keep Dask and Ray dashboards private.
- For Ray on Kubernetes, install KubeRay first.
