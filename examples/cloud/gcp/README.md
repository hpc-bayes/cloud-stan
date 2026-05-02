# Google GKE

These values files assume:

- GKE Workload Identity is enabled.
- A Kubernetes service account bound to a Google service account.
- A cloud-stan image in Artifact Registry.

Replace:

- `your-project`
- `us-central1`
- `cloud-stan-runner@your-project.iam.gserviceaccount.com`
- `gs://your-cloud-stan-bucket/results`
