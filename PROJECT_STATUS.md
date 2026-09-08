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

## Working Environment

Repository:

/home/sohel/devops-portfolio

We use the native Linux filesystem instead of /mnt/c because Python virtual environments caused permission/filesystem problems on the Windows-mounted filesystem.

## Current Architecture

Browser
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
Build and validate the first version of the application before containerizing it.

## Important Technical Decisions
- Use the native Linux filesystem for development.
- Keep Python dependencies isolated inside .venv.
- Do not commit .venv, __pycache__, or .pyc files.
- Use GitHub CLI for GitHub authentication from Ubuntu.
- Add health checks before introducing Docker and Kubernetes.

## Problems Encountered

### Python virtual environment failed under /mnt/c
The virtual environment could not be created correctly because the project was stored on the Windows-mounted filesystem.

Solution:
Moved the working repository to:

/home/sohel/devops-portfolio

### GitHub password authentication failed
GitHub does not support normal account-password authentication for Git operations over HTTPS.

Solution:
Installed and configured GitHub CLI.

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

## Next Task
Create automated tests for the FastAPI endpoints.
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
