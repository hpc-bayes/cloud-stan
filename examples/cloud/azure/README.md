# Azure AKS

These values files assume:

- Azure Workload Identity is enabled on the AKS cluster.
- A federated identity credential connects the Kubernetes service account to a
  user-assigned managed identity.
- A cloud-stan image in Azure Container Registry.

Replace:

- `yourregistry`
- `00000000-0000-0000-0000-000000000000`
- `https://youraccount.blob.core.windows.net/cloud-stan/results`
