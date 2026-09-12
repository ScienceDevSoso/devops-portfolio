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
- GitHub-hosted Ubuntu runner used for CI
- CI checks out the repository automatically
- CI configures Python 3.14
- CI installs dependencies from requirements.txt
- CI runs python -m pytest automatically
- First GitHub Actions CI run completed successfully
- All 3 API tests passed in GitHub Actions
- GitHub Actions logs inspected using GitHub CLI
- actions/checkout updated from v4 to v7
- actions/setup-python updated from v5 to v7
- Node.js 20 GitHub Actions deprecation warning resolved
- CI configured to run on pull requests targeting main
- Temporary ci-pr-test branch created
- Pull Request #1 created to test the pull_request trigger
- GitHub Actions automatically triggered for Pull Request #1
- Pull request CI completed successfully
- Test pull request closed without merging
- Temporary test branch deleted
- Main branch protection enabled
- Direct pushes to main are blocked
- Changes to main must go through a Pull Request
- CI status check named test is required before merge
- Branch protection applies to repository administrators
- Branch protection verified by deliberately attempting and failing to push directly to main
- Docker image build added to GitHub Actions CI
- CI now builds devops-portfolio:ci after automated tests pass
- Pull Request #2 created for the Docker CI change
- Pull Request #2 CI completed successfully
- Docker image built successfully on the GitHub-hosted runner
- Pull Request #2 merged into protected main
- Temporary ci-docker-build branch deleted
- GitHub Actions CI split into separate test and docker-build jobs
- docker-build configured with needs: test
- Verified that docker-build runs only after the test job succeeds
- Pull Request #4 passed both CI jobs and was merged into main

## Working Environment

Repository:

/home/sohel/devops-portfolio

Development uses the native Linux filesystem instead of /mnt/c because Python virtual environments caused permission/filesystem problems on the Windows-mounted filesystem.

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
   | required CI check
   v
GitHub Actions CI
   |
   v
Ubuntu Runner
   |
   +--> Checkout repository
   |
   +--> Python 3.14
   |
   +--> Install dependencies
   |
   +--> Run pytest
   |       |
   |       v
   |   3 API tests
   |
   +--> Build Docker image
           |
           v
   devops-portfolio:ci

Local application runtime:

Client / Browser
   |
   | localhost:8001
   v
Docker Host
   |
   | 8001 -> 8000
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

Continuous Integration with GitHub Actions is working successfully.

The application is automatically validated:
- when code is pushed to main
- when a pull request targets main
- by running all automated API tests
- by building the Docker image

The main branch is protected.

Changes must be developed on a separate branch, submitted through a Pull Request, and pass the required CI test check before they can be merged.

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
- Use host port 8001 because host port 8000 is already occupied locally.
- Use GitHub Actions for Continuous Integration.
- Run CI on a fresh GitHub-hosted Ubuntu runner rather than relying on the local machine.
- Explicitly configure Python 3.14 in CI.
- Use actions/checkout@v7 and actions/setup-python@v7.
- Treat CI configuration as version-controlled code.
- Run CI on both pushes to main and pull requests targeting main.
- Require Pull Requests before changes can enter main.
- Require the CI test status check before Pull Requests can be merged.
- Apply branch protection rules to repository administrators.
- Build the Docker image in CI so a successful test suite alone is not considered sufficient validation.
- Validate important GitHub and CI behavior deliberately before relying on it.

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

Investigation:

docker ps

Solution:

Mapped:

8001 -> 8000

### GitHub Actions Node.js 20 deprecation warning

The first CI run succeeded but reported that:

actions/checkout@v4
actions/setup-python@v5

targeted the deprecated Node.js 20 runtime.

Solution:

Updated to:

actions/checkout@v7
actions/setup-python@v7

The CI workflow passed again and the Node.js warning disappeared.

### Dependency deprecation warnings during pytest

Local pytest and GitHub Actions both report two warnings from FastAPI/Starlette/AnyIO dependencies.

The warnings come from installed packages rather than application code.

Current decision:

Do not change dependencies blindly because all tests pass. Revisit when dependency upgrades are intentionally introduced.

### Protected main branch rejected a direct push

A deliberate empty test commit was created locally on main and pushed to GitHub.

GitHub rejected the push with:

GH006: Protected branch update failed

and reported:

Changes must be made through a pull request.

This confirmed that branch protection was working correctly.

The local test commit was removed by resetting local main to origin/main.

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

## Next Task

Separate Docker build validation into its own GitHub Actions job and make it depend on the test job succeeding.

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
