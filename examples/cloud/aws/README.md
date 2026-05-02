# AWS EKS

These values files assume:

- EKS with IAM Roles for Service Accounts enabled.
- A service account role with access to your S3 output bucket.
- A cloud-stan image in ECR or GHCR.

Replace:

- `123456789012`
- `us-east-1`
- `cloud-stan`
- `arn:aws:iam::123456789012:role/cloud-stan-runner`
- `s3://your-cloud-stan-bucket/results`
