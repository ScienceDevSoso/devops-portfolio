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
- Updated CI workflow successfully verified

## Working Environment

Repository:

/home/sohel/devops-portfolio

Development uses the native Linux filesystem instead of /mnt/c because Python virtual environments caused permission/filesystem problems on the Windows-mounted filesystem.

## Current Architecture

Developer
   |
   | git push
   v
GitHub
   |
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
            |
            v
       3 API tests

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

Basic Continuous Integration with GitHub Actions is working successfully.

The application can now be tested locally and automatically tested by GitHub Actions after a push to main.

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

## Current Technologies

- Linux
- Ubuntu
- WSL 2
- Git
- GitHub
- GitHub CLI
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

## Next Task

Extend the GitHub Actions workflow so CI also runs on pull requests targeting main.

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
