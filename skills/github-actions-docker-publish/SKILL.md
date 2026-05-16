---
name: github-actions-docker-publish
description: "Build and publish Docker images via GitHub Actions to GHCR or other registries — multi-arch with buildx, dynamic tagging from git context, SBOM and provenance attestations, layer caching. Trigger when the user wants to push Docker images from CI, set up a container build workflow, configure GHCR, or automate image versioning. Sourced from github.com/skills/publish-docker-images."
---

# Publishing Docker Images from GitHub Actions

Build container images on every push and publish them to GitHub Container Registry (GHCR) with sensible tagging, multi-arch support, and supply-chain attestations.

## The Minimum Viable Workflow

`.github/workflows/docker.yml`:
```yaml
name: Build and Publish Docker Image

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      attestations: write
      id-token: write
    steps:
      - uses: actions/checkout@v4

      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix=,format=short

      - id: push
        uses: docker/build-push-action@v6
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - uses: actions/attest-build-provenance@v2
        if: github.event_name != 'pull_request'
        with:
          subject-name: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          subject-digest: ${{ steps.push.outputs.digest }}
          push-to-registry: true
```

## Permissions Breakdown

| Permission | Why |
|---|---|
| `contents: read` | Checkout the repo |
| `packages: write` | Push to GHCR |
| `attestations: write` | Generate Sigstore-based attestation |
| `id-token: write` | OIDC token for the attestation signer |

Without `packages: write`, the push fails with a 403. Without the attestation perms, `attest-build-provenance` silently skips.

## Tagging Strategy

`docker/metadata-action` auto-generates tags from git context:

| Event | Result |
|---|---|
| Push to `main` | `:main`, `:<short-sha>` |
| Push tag `v1.2.3` | `:1.2.3`, `:1.2`, `:<short-sha>` |
| PR #42 | `:pr-42`, `:<short-sha>` (build only, no push) |

The `{{major}}.{{minor}}` floating tag means a `v1.2.3` release auto-updates the `:1.2` tag. Consumers pinning to `:1.2` get patch releases automatically.

**Add a `:latest` tag** only if you want the default pull to track main:
```yaml
type=raw,value=latest,enable={{is_default_branch}}
```

## Multi-Architecture Builds

```yaml
- uses: docker/setup-qemu-action@v3
- uses: docker/setup-buildx-action@v3

- uses: docker/build-push-action@v6
  with:
    context: .
    platforms: linux/amd64,linux/arm64
    push: true
    tags: ${{ steps.meta.outputs.tags }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

Adds ARM64 builds for Apple Silicon and Graviton. **Cost**: roughly 2x build time. Use a [larger runner](https://docs.github.com/en/actions/using-github-hosted-runners/about-larger-runners) or `runs-on: ubuntu-24.04-arm` for native ARM.

For separate native runners (faster):
```yaml
jobs:
  build:
    strategy:
      matrix:
        platform:
          - { runner: ubuntu-latest, arch: linux/amd64 }
          - { runner: ubuntu-24.04-arm, arch: linux/arm64 }
    runs-on: ${{ matrix.platform.runner }}
    # build single-arch image, push by digest
  merge:
    needs: build
    runs-on: ubuntu-latest
    # use docker buildx imagetools create to merge digests into a manifest list
```

## Caching

GHA cache backend (`type=gha`) gives ~10-min cache hits on subsequent builds. The first build is full speed, the second is cache-warm.

Alternatives:
- `type=registry,ref=ghcr.io/org/cache:main` — store cache as a separate image, survives across branches.
- `type=local,dest=/tmp/.buildx-cache` — file-based, must combine with `actions/cache@v4`.

`mode=max` caches every intermediate layer. `mode=min` caches only the final image — smaller cache but worse hit rate.

## Build Attestations (Supply Chain)

`actions/attest-build-provenance` creates a signed SLSA provenance attestation. Anyone can verify the image was built by this exact workflow at this exact commit:

```bash
gh attestation verify oci://ghcr.io/owner/repo:tag --owner owner
```

For SBOM (Software Bill of Materials):
```yaml
- uses: actions/attest-sbom@v2
  with:
    subject-name: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
    subject-digest: ${{ steps.push.outputs.digest }}
    sbom-path: 'sbom.spdx.json'
    push-to-registry: true
```

## Pull-Request Builds Without Push

The example above sets `push: ${{ github.event_name != 'pull_request' }}`. PR builds verify the Dockerfile compiles but don't pollute the registry with pr-* tags from forks (which would also fail auth).

For PR comments showing the image SHA, use `peter-evans/create-or-update-comment` to post `steps.push.outputs.digest`.

## Container Visibility on GHCR

After the first push, the package is **private** by default. To make it public:
- Go to `https://github.com/users/<owner>/packages/container/<name>/settings`
- "Change visibility" → Public
- Link it to the repo for inherited permissions

Or via API on first push:
```yaml
- run: gh api -X PATCH /user/packages/container/${{ env.IMAGE_NAME }}/visibility -f visibility=public
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Dockerfile Best Practices for CI

Multi-stage builds keep the runtime image small:
```dockerfile
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-slim AS runtime
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
USER node
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

`USER node` instead of root — avoids running as root in the container.

`.dockerignore`:
```
.git
node_modules
.env
.env.*
*.log
coverage/
```

## Anti-Patterns

- ❌ Tagging only `:latest` — no way to roll back to a specific version.
- ❌ Hardcoding `:v1.2.3` in `docker push` instead of using `docker/metadata-action` — drifts from git tags.
- ❌ Pushing on PR builds from forks — auth fails and exposes the GHCR namespace.
- ❌ Building with `docker buildx --push` directly when `build-push-action` would also generate attestations.
- ❌ Skipping `cache-from`/`cache-to` and waiting 10 min for the same `npm ci` every time.
- ❌ Running as root in the container — security risk.
- ❌ Pinning all base images to `:latest` — non-reproducible builds.

## Quick Checklist

- [ ] Workflow has `permissions.packages: write` and `attestations: write`
- [ ] `docker/login-action` uses `GITHUB_TOKEN`, not a hardcoded PAT
- [ ] `docker/metadata-action` generates tags from git context
- [ ] `cache-from`/`cache-to: type=gha,mode=max` set
- [ ] `actions/attest-build-provenance` step pushes attestation to registry
- [ ] PR builds don't push (`push: ${{ github.event_name != 'pull_request' }}`)
- [ ] Dockerfile uses a `USER` other than root in the final stage
- [ ] `.dockerignore` excludes `.git`, `node_modules`, secrets

## References

- Source course: https://github.com/skills/publish-docker-images
- docker/build-push-action: https://github.com/docker/build-push-action
- docker/metadata-action: https://github.com/docker/metadata-action
- Attestations: https://docs.github.com/en/actions/security-guides/using-artifact-attestations
- GHCR docs: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry
