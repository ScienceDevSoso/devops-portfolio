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
- FastAPI installed
- Uvicorn installed
- requirements.txt created
- Initial FastAPI application created
- Root / endpoint created and tested
- /health endpoint created and tested
- /health returns HTTP 200 OK
- /version endpoint created and tested
- /version returns application version 1.0.0
- pytest and httpx installed
- Automated tests created for /, /health, and /version
- All 3 API tests passing successfully
- Docker Desktop configured with WSL 2 integration
- Docker CLI and Docker Engine verified successfully
- Dockerfile created for the FastAPI application
- .dockerignore created
- Docker image devops-portfolio:1.0 built successfully
- FastAPI application successfully started inside a Docker container
- Docker port mapping tested using host port 8001 to container port 8000
- /health and /version endpoints successfully tested through the container
- Docker container logs inspected
- Docker container lifecycle practiced: run, stop, start, inspect, and remove

## Working Environment

Repository:

/home/sohel/devops-portfolio

We use the native Linux filesystem instead of /mnt/c because Python virtual environments caused permission/filesystem problems on the Windows-mounted filesystem.

## Current Architecture

Client / Browser
   |
   | localhost:8001
   v
Docker Host
   |
   | port mapping 8001 -> 8000
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
   |
   +--> /health
   |
   +--> /version

## Current Phase

Docker containerization and local validation completed. Preparing to introduce GitHub Actions CI for automated testing.

## Important Technical Decisions

- Use the native Linux filesystem for development.
- Keep Python dependencies isolated inside .venv.
- Do not commit .venv, __pycache__, or .pyc files.
- Use GitHub CLI for GitHub authentication from Ubuntu.
- Add health checks before introducing Docker and Kubernetes.
- Use python:3.14-slim as the Docker base image to match the tested Python runtime while keeping the image relatively small.
- Install Python dependencies inside the Docker image from requirements.txt instead of copying the local .venv.
- Use .dockerignore to exclude .venv, __pycache__, and .git from the Docker build context.
- Run Uvicorn on 0.0.0.0 inside the container so the application is reachable through Docker port mapping.
- Use host port 8001 mapped to container port 8000 because host port 8000 is already used by another local Docker container.

## Problems Encountered

### pytest could not import the app module

Running `pytest` directly caused:

ModuleNotFoundError: No module named 'app'

Solution:

Run the test suite through the active Python interpreter:

python -m pytest

This successfully used the project virtual environment and discovered all tests.

### Python virtual environment failed under /mnt/c

The virtual environment could not be created correctly because the project was stored on the Windows-mounted filesystem.

Solution:

Moved the working repository to:

/home/sohel/devops-portfolio

### GitHub password authentication failed

GitHub does not support normal account-password authentication for Git operations over HTTPS.

Solution:

Installed and configured GitHub CLI.

### Docker socket permission denied in WSL 2

The Docker CLI was available, but `docker version` failed with:

permission denied while trying to connect to the docker API at unix:///var/run/docker.sock

Cause:

The current Linux user was not a member of the docker group.

Solution:

Added the current user to the docker group and started a fresh Ubuntu session so the new group membership became active.

### Docker host port 8000 was already allocated

Starting the FastAPI container with host port 8000 failed with:

Bind for 0.0.0.0:8000 failed: port is already allocated

Cause:

Host port 8000 was already being used by another local Docker container.

Investigation:

Used `docker ps` to identify that another running container was already publishing host port 8000.

Solution:

Kept Uvicorn listening on port 8000 inside the container and mapped a different host port:

8001 -> 8000

## Current Technologies

- Linux / Ubuntu / WSL 2
- Git
- GitHub
- GitHub CLI
- Python 3
- Python virtual environments
- pip
- FastAPI
- Uvicorn
- pytest
- httpx
- Docker
- Docker Desktop
- Docker Desktop WSL 2 integration

## Next Task

Introduce GitHub Actions and create the first CI workflow to automatically run the FastAPI test suite on repository changes.

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
