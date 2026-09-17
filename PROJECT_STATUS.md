# DevOps Project Status

## Goal

Build a real end-to-end DevOps portfolio project that demonstrates practical Junior DevOps skills.

## Completed

- Git installed and configured
- GitHub repository created
- Main branch configured
- README.md created
- PROJECT_STATUS.md created
- WSL 2 and Ubuntu installed
- Windows Terminal configured
- Repository cloned into /home/sohel/devops-portfolio
- GitHub CLI authentication configured
- Python virtual environment created
- .gitignore configured
- FastAPI and Uvicorn installed
- requirements.txt created
- Initial FastAPI application created
- / endpoint created and tested
- /health endpoint created and tested
- /version endpoint created and tested
- pytest and httpx installed
- Automated tests created for /, /health, and /version
- All 3 API tests passing locally
- Docker Desktop configured with WSL 2 integration
- Docker CLI and Docker Engine verified
- Dockerfile created
- .dockerignore created
- Docker image devops-portfolio:1.0 built successfully
- FastAPI application started successfully inside Docker
- Host port 8001 mapped to container port 8000
- /health and /version tested through Docker
- Docker logs inspected
- Docker container lifecycle practiced: run, stop, start, inspect, and remove
- GitHub Actions CI workflow created
- CI configured to trigger on pushes to main
- CI configured to trigger on Pull Requests targeting main
- GitHub-hosted Ubuntu runners used for CI
- CI configures Python 3.14
- CI installs dependencies from requirements.txt
- CI runs python -m pytest automatically
- All 3 API tests passing in GitHub Actions
- actions/checkout updated to v7
- actions/setup-python updated to v7
- Node.js 20 GitHub Actions deprecation warning resolved
- Main branch protection enabled
- Direct pushes to main blocked
- Pull Requests required before changes can enter main
- Branch protection applies to repository administrators
- GitHub Actions CI split into separate test and docker-build jobs
- docker-build configured with needs: test
- Verified that docker-build is skipped when the test job fails
- Deliberately introduced a failing pytest assertion to test CI behavior
- Verified failed test job prevents docker-build from running
- Restored the test and verified both CI jobs passed again
- test and docker-build configured as required branch protection checks
- Deliberately broke Dockerfile to test Docker build failure behavior
- Verified test passed while docker-build failed
- Verified failed docker-build caused Pull Request mergeStateStatus to become BLOCKED
- Restored Dockerfile and verified Pull Request mergeStateStatus became CLEAN
- Temporary CI failure test branches and Pull Requests cleaned up without merging broken code
- GitHub Container Registry publishing added to GitHub Actions
- publish-image job added after docker-build
- publish-image configured to run only on pushes to main
- Pull Request runs verified to skip publish-image
- GitHub Actions authenticated to GHCR using GITHUB_TOKEN
- packages: write permission configured for image publishing
- Docker image published to GitHub Container Registry
- Published image: ghcr.io/sciencedevsoso/devops-portfolio:latest
- Docker image successfully pulled from GHCR into local WSL environment
- GHCR image digest verified during pull
- Container successfully started from the GHCR image
- GHCR-published latest image verified through the /health endpoint
- Temporary GHCR test container stopped and removed
- Docker image tagging improved to include the Git commit SHA
- GitHub Actions now builds the registry image with both latest and commit-SHA tags
- GitHub Actions pushes both latest and commit-SHA image tags to GHCR
- SHA-tagging workflow validated through Pull Request CI
- SHA-tagging workflow merged into protected main
- Main branch CI successfully published the SHA-tagged image
- Exact commit-SHA image successfully pulled from GHCR
- Container successfully started from the exact commit-SHA image
- /health successfully verified from the SHA-tagged container

## Working Environment

Repository:

/home/sohel/devops-portfolio

Development uses the native Linux filesystem instead of /mnt/c because Python virtual environments caused permission/filesystem problems on the Windows-mounted filesystem.

Docker Desktop runs on Windows and provides Docker Engine access to Ubuntu through WSL 2 integration.

## Current Architecture

Developer
   |
   | feature branch
   v
GitHub
   |
   | Pull Request
   v
Branch Protection
   |
   | required checks:
   | test
   | docker-build
   v
GitHub Actions
   |
   +--> test job
   |      |
   |      +--> Checkout repository
   |      +--> Python 3.14
   |      +--> Install dependencies
   |      +--> pytest
   |
   +--> docker-build job
   |      |
   |      | needs: test
   |      +--> Checkout repository
   |      +--> docker build
   |
   +--> publish-image job
          |
          | needs: docker-build
          | runs only on push to main
          +--> Checkout repository
          +--> Login to GHCR
          +--> Build registry image
          +--> Push image
                  |
                  v
       GitHub Container Registry
                  |
                  v
ghcr.io/sciencedevsoso/devops-portfolio:latest
ghcr.io/sciencedevsoso/devops-portfolio:<git-commit-sha>

Local application runtime:

Client / Browser
   |
   v
Docker Host
   |
   v
Docker Container
   |
   v
Uvicorn
   |
   v
FastAPI
   |
   +--> /
   +--> /health
   +--> /version

## Current Phase

Continuous Integration and initial container image publishing are working successfully.

Pull Requests are automatically validated with:

- pytest
- Docker image build

Both test and docker-build are required before changes can merge into main.

After approved code is merged into main:

- GitHub Actions runs the tests again
- Docker image build is validated
- publish-image runs
- GitHub Actions logs in to GHCR
- the application image is built
- the image is pushed to GitHub Container Registry

Published images use two tags:

ghcr.io/sciencedevsoso/devops-portfolio:latest
ghcr.io/sciencedevsoso/devops-portfolio:<git-commit-sha>

The latest image and an exact commit-SHA image have both been successfully pulled from GHCR and run locally. The /health endpoint was verified from the published containers.

The commit-SHA tag provides traceability between source code and the Docker image and allows a known-good image version to be selected for rollback.

## Important Technical Decisions

- Use the native Linux filesystem for development.
- Keep Python dependencies isolated inside .venv.
- Do not commit .venv, __pycache__, or .pyc files.
- Use GitHub CLI for GitHub authentication and GitHub Actions inspection.
- Run tests with python -m pytest so pytest uses the intended Python environment.
- Add health checks before introducing Docker and Kubernetes.
- Use python:3.14-slim as the Docker base image.
- Install dependencies inside the Docker image from requirements.txt.
- Exclude .venv, __pycache__, and .git from Docker build context.
- Run Uvicorn on 0.0.0.0 inside the container.
- Use GitHub Actions for Continuous Integration.
- Run CI on fresh GitHub-hosted Ubuntu runners.
- Explicitly configure Python 3.14 in CI.
- Use actions/checkout@v7 and actions/setup-python@v7.
- Treat CI configuration as version-controlled code.
- Run CI on pushes to main and Pull Requests targeting main.
- Require Pull Requests before changes can enter main.
- Require both test and docker-build CI checks before Pull Requests can merge.
- Use needs: test so Docker validation only runs after tests pass.
- Build the Docker image in CI so passing Python tests alone is not enough.
- Deliberately test failure scenarios before relying on CI protection.
- Do not publish Docker images from unmerged Pull Requests.
- Publish Docker images only after code reaches main.
- Use GitHub Container Registry before introducing AWS ECR so container registry concepts are understood first.
- Use GITHUB_TOKEN instead of storing a personal GitHub password in CI.
- Give publish-image only the permissions it needs: contents: read and packages: write.
- Keep the latest image tag for convenience.
- Also tag every published image with github.sha so the image can be traced to the exact Git commit.
- Prefer commit-SHA tags when an exact deployment or rollback version must be identified.

## Problems Encountered

### pytest could not import the app module

Running:

pytest

caused:

ModuleNotFoundError: No module named 'app'

Solution:

python -m pytest

This runs pytest through the intended Python interpreter.

### Python virtual environment failed under /mnt/c

The project was originally stored on the Windows-mounted filesystem.

Solution:

Moved the repository to:

/home/sohel/devops-portfolio

### GitHub password authentication failed

GitHub does not support normal account-password authentication for Git operations over HTTPS.

Solution:

Installed and configured GitHub CLI authentication.

### Docker socket permission denied

docker version failed with a permission error for:

/var/run/docker.sock

Cause:

The Linux user was not in the docker group.

Solution:

Added the user to the docker group and started a fresh Ubuntu session.

### Docker host port 8000 was already allocated

Docker could not publish host port 8000 because another local container was already using it.

Solution:

Used another host port while keeping container port 8000.

### GitHub Actions Node.js 20 deprecation warning

Older GitHub Actions versions used the deprecated Node.js 20 runtime.

Solution:

Updated to:

actions/checkout@v7
actions/setup-python@v7

### Dependency deprecation warnings during pytest

Local pytest and GitHub Actions report warnings from FastAPI/Starlette/AnyIO dependencies.

Current decision:

Do not change dependencies blindly because all tests pass. Revisit dependency upgrades intentionally later.

### Protected main branch rejected a direct push

A deliberate test push to main was rejected.

This confirmed that branch protection was working.

### Test failure CI experiment

A pytest assertion was deliberately changed to expect HTTP 500 instead of HTTP 200.

Result:

test failed
docker-build was skipped

The test was restored and both jobs passed.

### Docker build failure experiment

Dockerfile was deliberately changed to COPY a file that did not exist.

Result:

test passed
docker-build failed
Pull Request mergeStateStatus became BLOCKED

After restoring Dockerfile:

test passed
docker-build passed
Pull Request mergeStateStatus became CLEAN

This confirmed that docker-build is an effective required merge gate.

### Docker command disappeared from WSL

Ubuntu temporarily reported:

The command 'docker' could not be found in this WSL 2 distro.

Docker Desktop WSL integration was already enabled.

Solution:

Ran:

wsl --shutdown

from Windows, restarted Ubuntu while Docker Desktop was running, and verified Docker access again with:

docker version

## Current Technologies

- Linux
- Ubuntu
- WSL 2
- Git
- GitHub
- GitHub CLI
- GitHub Branch Protection
- Python 3.14
- Python virtual environments
- pip
- FastAPI
- Uvicorn
- pytest
- httpx
- Docker
- Docker Desktop
- Docker Desktop WSL 2 integration
- GitHub Actions
- YAML
- Continuous Integration
- Pull Requests
- GitHub Container Registry
- Docker image registries
- AWS
- Amazon EC2
- AWS IAM
- Security Groups
- Amazon EBS
- SSH

## Next Task

The first manual AWS deployment is complete.

The FastAPI application is now running on an AWS EC2 instance using the exact Docker image previously published to GHCR with a Git commit SHA tag.

The manual deployment included:

- AWS EC2 instance running Ubuntu 26.04 LTS
- t3.micro instance type
- SSH key-pair authentication
- SSH access restricted by Security Group
- public and private IP addressing
- encrypted EBS root storage
- Docker Engine installed manually on EC2
- ubuntu user added to the docker group
- SHA-tagged application image pulled from GHCR
- FastAPI container started with port 8000 exposed
- Security Group configured to allow application traffic on port 8000 from the developer IP
- /health endpoint verified externally
- /version endpoint verified externally

Next, inspect and understand the AWS networking that supports this deployment, especially the VPC, subnet, routing, public/private IP addresses, and Security Group behavior.

After the manual AWS infrastructure and networking are understood, begin reproducing the infrastructure with Terraform.

## Future Architecture

Developer
   |
   v
GitHub
   |
   v
GitHub Actions CI/CD
   |
   v
Tests + Docker Build
   |
   v
Container Registry
   |
   v
AWS Infrastructure
   |
   v
Kubernetes
   |
   v
Helm
   |
   +--> Application
   |
   +--> Prometheus
   |
   +--> Grafana
   |
   +--> Logging / Observability
