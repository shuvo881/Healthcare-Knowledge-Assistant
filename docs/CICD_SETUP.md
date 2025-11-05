# CI/CD Setup Guide

This guide explains how to set up the GitHub Actions CI/CD pipeline for automatic Docker image builds and pushes to Docker Hub.

## Prerequisites

1. **Docker Hub Account** - Create one at https://hub.docker.com if you don't have it
2. **GitHub Repository** - Your code should be in a GitHub repository

## Setup Steps

### 1. Create Docker Hub Access Token

1. Log in to [Docker Hub](https://hub.docker.com)
2. Click on your username (top right) → **Account Settings**
3. Go to **Security** → **New Access Token**
4. Give it a name (e.g., `github-actions`)
5. Set permissions to **Read, Write, Delete**
6. Click **Generate**
7. **Copy the token** (you won't see it again!)

### 2. Add GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these two secrets:

   **Secret 1:**
   - Name: `DOCKERHUB_USERNAME`
   - Value: Your Docker Hub username (e.g., `johndoe`)

   **Secret 2:**
   - Name: `DOCKERHUB_TOKEN`
   - Value: The access token you copied from Docker Hub

### 3. Commit and Push the Workflow

The workflow file is already created at `.github/workflows/docker-build-push.yml`

```bash
git add .github/workflows/docker-build-push.yml
git commit -m "Add CI/CD pipeline for Docker builds"
git push origin main
```

## How It Works

### Triggers

The pipeline runs automatically when:
- ✅ You push to `main` or `master` branch
- ✅ You create a pull request to `main` or `master`
- ✅ You push a tag starting with `v` (e.g., `v1.0.0`)
- ✅ You manually trigger it from GitHub Actions tab

### Docker Image Tags

The pipeline creates multiple tags:

| Trigger | Example Tags |
|---------|-------------|
| Push to main | `latest`, `main`, `main-abc1234` |
| Push tag v1.2.3 | `v1.2.3`, `1.2.3`, `1.2`, `1` |
| Pull request #5 | `pr-5` |

### Multi-Platform Support

Images are built for:
- `linux/amd64` (Intel/AMD processors)
- `linux/arm64` (ARM processors, Apple Silicon)

## Usage

### Pull the Latest Image

```bash
docker pull <your-dockerhub-username>/healthcare-knowledge-assistant:latest
```

### Run the Container

```bash
docker run -p 8000:8000 \
  -e API_KEY=your-api-key \
  <your-dockerhub-username>/healthcare-knowledge-assistant:latest
```

### Use Specific Version

```bash
docker pull <your-dockerhub-username>/healthcare-knowledge-assistant:v1.0.0
```

## Manual Trigger

1. Go to your GitHub repository
2. Click **Actions** tab
3. Select **Build and Push Docker Image** workflow
4. Click **Run workflow** button
5. Select branch and click **Run workflow**

## Monitoring

- Check workflow status in the **Actions** tab of your GitHub repository
- View your images at `https://hub.docker.com/r/<your-username>/healthcare-knowledge-assistant`

## Troubleshooting

### Authentication Failed
- Verify `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets are correct
- Make sure the Docker Hub token has write permissions
- Token might be expired - generate a new one

### Build Failed
- Check the workflow logs in GitHub Actions
- Ensure Dockerfile is valid
- Make sure all dependencies are in `pyproject.toml` and `uv.lock`

### Image Not Found
- Wait for the workflow to complete (check Actions tab)
- Verify the image name matches your Docker Hub username
- Check if the workflow had permission to push

## Release Process

To create a new release:

```bash
# Tag your commit
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push the tag
git push origin v1.0.0
```

This will automatically build and push images with tags: `v1.0.0`, `1.0.0`, `1.0`, `1`, and `latest`.

