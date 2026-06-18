# Deployment Discovery Report

**Target Project Verified:** `perceptive-bay-493811-c1` (Name: `prompt-wars`)
*(Note: `prompt-wars-project-3` does not exist or is inaccessible. We are using the verified `prompt-wars` project).*

## Discovery Results

### 1. Workload Identity Federation
- **Status:** MISSING
- **Findings:** `gcloud iam workload-identity-pools list` returned `0 items`.
- **Action Required:** We must create a WIF Pool and Provider to allow GitHub Actions to authenticate securely.

### 2. Artifact Registry
- **Status:** EXISTS
- **Findings:** Found two existing Docker repositories in `us-central1`:
  1. `cloud-run-source-deploy`
  2. `mcp-cloud-run-deployments`
- **Action Required:** We can reuse `mcp-cloud-run-deployments` or `cloud-run-source-deploy` to push our backend Docker images. No creation necessary.

### 3. Service Account
- **Status:** EXISTS (Default)
- **Findings:** Found `879775404804-compute@developer.gserviceaccount.com` (Default compute service account).
- **Action Required:** We can bind the GitHub WIF to this service account, or ideally create a dedicated least-privilege service account for the GitHub Actions deployment.

### 4. Cloud Run Service
- **Status:** MISSING
- **Findings:** Found `smart-election-assistant` and `smart-stadium`, but no service for `prompt-wars-project-3` or `ecosphere-ai`.
- **Action Required:** The Cloud Run service will automatically be created on the first successful deployment from GitHub Actions.

## Proposed Infrastructure Creation Plan

If approved, I will execute the following `gcloud` commands locally to provision the exact missing resources for GitHub Actions:

```bash
# 1. Create a dedicated Service Account
gcloud iam service-accounts create github-actions-deployer --display-name="GitHub Actions Deployer"

# 2. Grant it permissions to deploy Cloud Run & push to Artifact Registry
gcloud projects add-iam-policy-binding perceptive-bay-493811-c1 \
  --member="serviceAccount:github-actions-deployer@perceptive-bay-493811-c1.iam.gserviceaccount.com" \
  --role="roles/run.admin"
gcloud projects add-iam-policy-binding perceptive-bay-493811-c1 \
  --member="serviceAccount:github-actions-deployer@perceptive-bay-493811-c1.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"
gcloud projects add-iam-policy-binding perceptive-bay-493811-c1 \
  --member="serviceAccount:github-actions-deployer@perceptive-bay-493811-c1.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

# 3. Create WIF Pool & Provider for GitHub
gcloud iam workload-identity-pools create github-pool --location="global" --display-name="GitHub Actions Pool"
gcloud iam workload-identity-pools providers create-oidc github-provider \
  --workload-identity-pool="github-pool" --location="global" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
  --attribute-condition="assertion.repository == 'GovindaSaiKiran/prompt_wars_project_3'"

# 4. Bind the WIF Provider to the Service Account
gcloud iam service-accounts add-iam-policy-binding github-actions-deployer@perceptive-bay-493811-c1.iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/879775404804/locations/global/workloadIdentityPools/github-pool/attribute.repository/GovindaSaiKiran/prompt_wars_project_3"
```

This will give us the exact WIF Provider string:
`projects/879775404804/locations/global/workloadIdentityPools/github-pool/providers/github-provider`
