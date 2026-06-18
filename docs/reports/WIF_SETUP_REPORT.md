# Workload Identity Federation Setup Report

**Pool Name:** `github-pool`
**Provider Name:** `github-provider`
**Service Account Used:** `879775404804-compute@developer.gserviceaccount.com`

## IAM Bindings Applied
1. `roles/run.admin`
2. `roles/artifactregistry.writer`
3. `roles/iam.serviceAccountUser`

## GitHub Repository Bindings
- `attribute-mapping`: `google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository`
- `attribute-condition`: `assertion.repository == 'GovindaSaiKiran/prompt_wars_project_3'`

## Verification Commands Executed
```bash
gcloud iam workload-identity-pools create github-pool ...
gcloud iam workload-identity-pools providers create-oidc github-provider ...
gcloud projects add-iam-policy-binding ...
gcloud iam service-accounts add-iam-policy-binding ...
```

**Outcome:** Successfully created and securely linked to the GitHub repository to allow credential-less authentication.
