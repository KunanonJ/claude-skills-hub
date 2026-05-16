---
name: github-actions-azure-deploy
description: "Deploy applications to Microsoft Azure from GitHub Actions using OIDC federated credentials (no long-lived secrets), with staging/production environments, slot swaps, and Bicep/ARM. Trigger when the user wants to deploy to Azure App Service, Container Apps, AKS, or Functions from GHA, set up `azure/login@v2` with OIDC, or build a Continuous Delivery pipeline. Sourced from github.com/skills/deploy-to-azure."
---

# Deploy to Azure from GitHub Actions

Continuous Delivery to Azure with no static service-principal secrets in your repo. OIDC federated credentials let GitHub Actions assume an Azure role at runtime — short-lived, audited, revocable.

## One-Time Azure Setup (OIDC)

```bash
# 1. Create an Azure AD application + service principal
az ad sp create-for-rbac --name "gh-deploy-$REPO" --json-auth=false

# 2. Note the appId (clientId), tenantId, and your subscriptionId

# 3. Federate it to your GitHub repo
az ad app federated-credential create --id <appId> --parameters '{
  "name": "main-branch",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:OWNER/REPO:ref:refs/heads/main",
  "audiences": ["api://AzureADTokenExchange"]
}'

# 4. Grant the SP a role on the target resource group
az role assignment create \
  --assignee <appId> \
  --role "Contributor" \
  --scope /subscriptions/<subId>/resourceGroups/<rg>
```

Subject patterns for different triggers:
- `repo:OWNER/REPO:ref:refs/heads/main` — push to main only
- `repo:OWNER/REPO:environment:production` — deployments to "production" environment
- `repo:OWNER/REPO:pull_request` — PR builds
- `repo:OWNER/REPO:ref:refs/tags/v*` — tag pushes

Store in repo: `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID` as **variables** (not secrets — they're identifiers, not credentials).

## The Workflow

```yaml
name: Deploy to Azure

on:
  push:
    branches: [main]
  pull_request:
    types: [labeled]

permissions:
  id-token: write       # required for OIDC
  contents: read

env:
  AZURE_WEBAPP_NAME: my-app
  AZURE_RESOURCE_GROUP: my-rg

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "20", cache: npm }
      - run: npm ci && npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: webapp
          path: dist/

  deploy-staging:
    needs: build
    if: github.event_name == 'pull_request' && contains(github.event.pull_request.labels.*.name, 'deploy-staging')
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: ${{ steps.deploy.outputs.webapp-url }}
    steps:
      - uses: actions/download-artifact@v4
        with: { name: webapp, path: dist/ }

      - uses: azure/login@v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}

      - id: deploy
        uses: azure/webapps-deploy@v3
        with:
          app-name: ${{ env.AZURE_WEBAPP_NAME }}
          slot-name: staging
          package: dist/

  deploy-production:
    needs: build
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://${{ env.AZURE_WEBAPP_NAME }}.azurewebsites.net
    steps:
      - uses: actions/download-artifact@v4
        with: { name: webapp, path: dist/ }

      - uses: azure/login@v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}

      - uses: azure/webapps-deploy@v3
        with:
          app-name: ${{ env.AZURE_WEBAPP_NAME }}
          slot-name: staging       # deploy to staging slot first
          package: dist/

      - name: Swap staging into production
        run: |
          az webapp deployment slot swap \
            --resource-group ${{ env.AZURE_RESOURCE_GROUP }} \
            --name ${{ env.AZURE_WEBAPP_NAME }} \
            --slot staging \
            --target-slot production
```

## Two-Slot Production Pattern

Staging deploy → smoke test → slot swap. The swap is a hostname switch, not a re-deploy — production gets the already-warmed staging instance.

Gotchas:
- App settings marked "Deployment slot setting" stay with the slot during swap. Use this for slot-specific config (e.g., different App Insights instances).
- Connection strings without the slot-setting flag swap with the code.
- Pre-swap warmup: Azure makes warmup requests against the staging slot before swap. If `/health` returns 200 it proceeds.

## Container Apps / AKS Variants

For Container Apps:
```yaml
- uses: azure/container-apps-deploy-action@v2
  with:
    appSourcePath: ${{ github.workspace }}
    acrName: myregistry
    containerAppName: my-app
    resourceGroup: ${{ env.AZURE_RESOURCE_GROUP }}
```

For AKS:
```yaml
- uses: azure/aks-set-context@v4
  with:
    resource-group: ${{ env.AZURE_RESOURCE_GROUP }}
    cluster-name: my-aks
- run: kubectl apply -f k8s/
```

## Infrastructure as Code

Provision the infra in the same workflow with Bicep:

```yaml
- uses: azure/login@v2
  with: { client-id: ..., tenant-id: ..., subscription-id: ... }

- uses: azure/arm-deploy@v2
  with:
    scope: resourcegroup
    resourceGroupName: ${{ env.AZURE_RESOURCE_GROUP }}
    template: ./infra/main.bicep
    parameters: environment=production
    failOnStdErr: false
```

Required role for ARM/Bicep deployment: at least `Contributor` on the resource group.

## Environment Protection Rules

In repo Settings → Environments → `production`:
- Required reviewers (2 from a team)
- Wait timer (5 min before deploy)
- Branch protection (only deploy from `main`)

Combined with the OIDC subject restriction (`repo:OWNER/REPO:environment:production`), this means: deploys only fire from main, only after human approval, and only the specific env can request a token.

## Tearing Down (Ephemeral Environments)

For PR preview environments:
```yaml
jobs:
  destroy:
    if: github.event.action == 'closed'
    runs-on: ubuntu-latest
    steps:
      - uses: azure/login@v2
        with: { client-id: ..., tenant-id: ..., subscription-id: ... }
      - run: |
          az group delete --name pr-${{ github.event.pull_request.number }} --yes --no-wait
```

## Anti-Patterns

- ❌ Storing `AZURE_CREDENTIALS` JSON blob as a secret — use OIDC.
- ❌ Service principal with `Owner` role — over-permissioned. `Contributor` on the RG is plenty for most cases.
- ❌ Federated credential subject `repo:OWNER/REPO:*` — too permissive. Scope by branch, tag, or environment.
- ❌ Deploying to production directly from `push` without slot swap — no smoke-test window.
- ❌ Slot swap without a `/health` endpoint that actually checks dependencies.
- ❌ Putting connection strings as plain env vars on the webapp instead of using Key Vault references.

## Quick Checklist

- [ ] AAD app registered with federated credential matching workflow trigger
- [ ] Workflow has `permissions.id-token: write`
- [ ] Uses `azure/login@v2` with `client-id` / `tenant-id` / `subscription-id` (no `creds:`)
- [ ] Production deploy gated by `environment: production` with required reviewers
- [ ] Slot swap pattern for App Service deploys
- [ ] Health check endpoint that fails on dependency outage
- [ ] PR ephemeral envs cleaned up on PR close

## References

- Source course: https://github.com/skills/deploy-to-azure
- azure/login OIDC guide: https://github.com/Azure/login#configure-deployment-credentials
- Federated identity: https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation-create-trust
- Slot swap: https://learn.microsoft.com/en-us/azure/app-service/deploy-staging-slots
