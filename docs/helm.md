# Helm Charts

The repository ships two lightweight charts for cloud-stan jobs:

- `stan_dask_chart`: Dask scheduler, Dask workers, and an optional cloud-stan job.
- `stan_ray_chart/ray_cluster`: a KubeRay `RayCluster` and an optional cloud-stan job.

These charts are intentionally small application charts. For production
multi-user Dask deployments, the community Dask Helm repository also publishes
`dask/dask`, `dask/daskhub`, `dask-gateway`, and the Dask Kubernetes operator.

## Dask Chart

```bash
helm upgrade --install cloud-stan-dask ./stan_dask_chart \
  --namespace cloud-stan \
  --create-namespace \
  --values examples/cloud/aws/dask-values.yaml
```

The job gets the scheduler address from `DASK_SCHEDULER_ADDRESS`.

## Ray Chart

Install KubeRay before installing the Ray chart:

```bash
helm repo add kuberay https://ray-project.github.io/kuberay-helm/
helm repo update
helm upgrade --install kuberay-operator kuberay/kuberay-operator \
  --namespace kuberay-system \
  --create-namespace
```

Then install cloud-stan's Ray chart:

```bash
helm upgrade --install cloud-stan-ray ./stan_ray_chart/ray_cluster \
  --namespace cloud-stan \
  --create-namespace \
  --values examples/cloud/aws/ray-values.yaml
```

The job gets the Ray client address from `RAY_ADDRESS`.

## Security Defaults

Both charts set:

- `runAsNonRoot`
- `seccompProfile: RuntimeDefault`
- `allowPrivilegeEscalation: false`
- dropped Linux capabilities
- `ClusterIP` services by default

Keep dashboards private. Use `kubectl port-forward`, an internal ingress, or a
VPN rather than public load balancers for scheduler and dashboard ports.
