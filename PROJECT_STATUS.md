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

- Manual AWS EC2 deployment completed and documented
- AWS networking behind the EC2 deployment inspected manually
- Default VPC identified: 172.31.0.0/16
- EC2 subnet identified: 172.31.16.0/20 in eu-north-1a
- EC2 private IP identified: 172.31.21.20
- Public IP used during deployment: 16.171.54.38
- Main route table inspected
- Verified 172.31.0.0/16 -> local
- Verified 0.0.0.0/0 -> Internet Gateway
- Confirmed subnet uses the main route table implicitly
- Confirmed Internet Gateway is attached to the VPC
- Security Group inbound rules inspected
- SSH port 22 restricted to developer public IP /32
- FastAPI port 8000 restricted to developer public IP /32
- Security Group outbound allows all traffic to 0.0.0.0/0
- Understood VPC, subnet, routing, Internet Gateway, Security Group, private IP, and public IP roles
- Terraform CLI installed and verified
- AWS CLI v2 installed and verified
- AWS CLI authenticated with non-root IAM user sohel-admin
- Terraform working directory created under terraform/
- AWS provider configured for eu-north-1
- terraform init completed successfully
- Terraform AWS provider downloaded and locked
- terraform validate completed successfully
- Terraform successfully authenticated to AWS
- Existing default VPC read using a Terraform data source
- Default VPC CIDR 172.31.0.0/16 confirmed through Terraform
- First terraform plan completed with no infrastructure changes
- First terraform apply completed with 0 resources added, changed, or destroyed
- Terraform state files and .terraform/ excluded from Git
- Terraform configuration formatted with terraform fmt


## Working Environment

Repository:

/home/sohel/devops-portfolio

Development uses the native Linux filesystem instead of /mnt/c because Python virtual environments caused permission/filesystem problems on the Windows-mounted filesystem.

Docker Desktop runs on Windows and provides Docker Engine access to Ubuntu through WSL 2 integration.

## Current Architecture

Developer
   |
   v
GitHub
   |
   v
GitHub Actions
   |
   +--> pytest
   +--> Docker build
   +--> publish image
              |
              v
GitHub Container Registry
              |
              v
ghcr.io/sciencedevsoso/devops-portfolio:latest
              |
              v
Local Kubernetes / Minikube
              |
              v
Deployment
   |
   | desired replicas: 1
   v
Pod
   |
   v
FastAPI container
   |
   +--> readiness probe: /health
   +--> liveness probe: /health

Kubernetes Service
   |
   v
Pod :8000

## Current Phase

Local Kubernetes deployment is working successfully with Minikube.

The FastAPI container image published by GitHub Actions to GHCR is now deployed using Kubernetes manifests.

Implemented:

- Kubernetes Deployment
- one desired application replica
- GHCR container image
- container port 8000
- readiness probe using `/health`
- liveness probe using `/health`
- ClusterIP Service on port 8000
- local access using `kubectl port-forward`

Kubernetes self-healing was deliberately tested by deleting the running application Pod. The Deployment detected that the actual replica count no longer matched the desired state and automatically created a replacement Pod.

The replacement Pod reached `Ready 1/1` and the application `/health` endpoint was successfully verified through the Kubernetes Service.

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
- Kubernetes
- Minikube
- kubectl
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

Merge the local Kubernetes manifests milestone.

Then retire the standalone Terraform EC2 application deployment and begin moving the Kubernetes architecture toward AWS.

After the standalone EC2 deployment is removed, continue with:

- AWS Kubernetes / EKS fundamentals
- Kubernetes deployment on AWS
- Helm
- Prometheus
- Grafana
- application and infrastructure metrics
- logging and failure scenarios

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

## Terraform Security Group Milestone

Completed:
- First Terraform-managed AWS Security Group created
- Security Group created inside the existing default VPC
- Terraform-managed outbound rule allows all IPv4 traffic
- Terraform-managed inbound rule allows TCP port 8000
- Terraform state inspected with terraform state list and terraform state show
- Terraform idempotency verified: repeated terraform plan returned no changes
- AWS CLI expired-session authentication failure troubleshot
- AWS CLI authentication restored using aws login --remote through an Incognito browser session
- AWS identity verified with aws sts get-caller-identity

Technologies added:
- Terraform
- Terraform state
- AWS CLI v2
- AWS VPC
- Terraform-managed Security Groups

Current Terraform architecture:

Existing Default VPC
        |
        | data.aws_vpc.default
        v
Terraform
        |
        v
devops-portfolio-app Security Group
        |
        +--> Ingress: TCP 8000 from 0.0.0.0/0
        |
        +--> Egress: all traffic to 0.0.0.0/0

Next task:
Begin defining the compute resource that will use this Security Group, while continuing to review every terraform plan before applying infrastructure changes.




## Terraform EC2 Deployment Milestone

Completed:
- Existing manual EC2 configuration inspected before recreating compute with Terraform
- Existing Ubuntu 26.04 AMI inspected and reused for the learning deployment
- Existing subnet inspected: subnet-047c7f9d3d19817a4 in eu-north-1a
- Subnet confirmed to belong to the default VPC and assign public IPv4 addresses
- Terraform-managed EC2 instance created
- EC2 instance type configured as t3.micro
- Existing EC2 key pair devops-portfolio-ec2-key reused for SSH access
- Terraform-managed Security Group attached to the EC2 instance
- Public IPv4 assignment explicitly enabled in Terraform
- SSH ingress rule added for TCP port 22
- SSH restricted to the current developer public IPv4 address using a /32 CIDR
- Terraform plan reviewed before EC2 creation
- Terraform created EC2 instance i-0a3070af7b8b806c7 successfully
- Terraform state inspected for the new EC2 resource
- EC2 system and instance health checks verified as OK
- SSH access to the Terraform-created EC2 instance verified successfully
- Docker installed manually on the fresh Ubuntu EC2 instance
- Docker daemon verified as active
- Docker socket permission problem diagnosed
- ubuntu user added to the docker group
- Docker client and server verified without sudo
- Application image pulled from GitHub Container Registry
- ghcr.io/sciencedevsoso/devops-portfolio:latest started successfully on EC2
- Docker port 8000 mapped to container port 8000
- FastAPI /health verified successfully from inside the EC2 instance
- FastAPI /health verified successfully externally through the EC2 public IP
- Terraform idempotency verified after EC2 creation with no infrastructure changes required

Problems encountered:
- The terraform-ec2-instance branch was created from a stale local main branch after PR #15 had already merged remotely
- The EC2 resource initially referenced aws_security_group.app before the branch contained that resource
- The EC2 work was stashed, the branch rebased onto origin/main, and the work restored
- git stash pop produced a main.tf merge conflict because both main and the stash modified the same Terraform file
- The conflict was resolved manually by preserving both the existing Security Group resources and the new EC2 resource
- The old developer public IP had changed, so the existing SSH /32 CIDR could not be reused
- The current public IPv4 address was checked before creating the Terraform SSH rule
- Docker initially returned permission denied for /var/run/docker.sock
- The ubuntu user was added to the docker group and a new SSH session activated the new group membership

Current Terraform-managed AWS architecture:

Existing Default VPC
        |
        v
Existing Subnet
subnet-047c7f9d3d19817a4
        |
        v
Terraform-managed EC2
devops-portfolio-app
        |
        +--> Terraform-managed Security Group
        |       |
        |       +--> TCP 22 from developer /32
        |       +--> TCP 8000
        |       +--> outbound traffic
        |
        +--> Ubuntu 26.04
                |
                v
              Docker
                |
                v
ghcr.io/sciencedevsoso/devops-portfolio:latest
                |
                v
             FastAPI
                |
                +--> /health

Next task:
Commit and merge the Terraform EC2 milestone, then decide how to make server provisioning reproducible instead of manually installing Docker after every new EC2 instance.


## Terraform Reproducible EC2 Provisioning Milestone

Completed:
- Added `terraform/user_data.sh` for automatic EC2 bootstrap provisioning
- EC2 `user_data` configured with `file("${path.module}/user_data.sh")`
- `user_data_replace_on_change = true` configured so bootstrap changes cause a fresh EC2 launch
- Docker installation automated during the initial EC2 boot
- Docker service automatically enabled and started
- GHCR application image automatically pulled
- FastAPI container automatically started on port 8000
- Docker restart policy configured as `unless-stopped`
- Terraform plan correctly identified that adding `user_data` required replacing the Terraform-managed EC2 instance
- Reviewed the saved Terraform plan before applying the destructive replacement
- Previous Terraform EC2 instance `i-0a3070af7b8b806c7` replaced intentionally
- New Terraform EC2 instance created: `i-00c82256c055c7dc1`
- New EC2 public IP after replacement: `13.60.8.100`
- `/health` succeeded immediately from outside EC2 without manual server provisioning
- Confirmed that Terraform can now reproduce the EC2 + Docker + FastAPI runtime from a fresh instance
- Added Terraform input variables for AWS region, AMI, instance type, subnet, EC2 key pair, and developer SSH CIDR
- Replaced hardcoded resource values with `var.<name>` references
- Added local `terraform.tfvars` for environment-specific values
- Added `terraform.tfvars.example` for repository documentation
- Added `terraform/terraform.tfvars` to `.gitignore`
- Added outputs for EC2 instance ID, EC2 public IP, application URL, and default VPC CIDR
- Variable/output refactor validated with `terraform fmt`, `terraform validate`, and `terraform plan`
- Refactor produced no real infrastructure changes
- Application health verified again after the refactor

Important technical decisions:
- Use EC2 `user_data` only as a simple bootstrap mechanism at this stage, not as a long-term deployment platform
- Treat infrastructure provisioning and application deployment as related but separate concerns
- Use `user_data_replace_on_change = true` because initial-boot bootstrap scripts should run against a fresh instance when their configuration changes
- Keep environment-specific Terraform values separate from resource definitions
- Do not treat `.tfvars` files as secret-management systems
- Keep the real local `terraform.tfvars` out of Git and commit only an example file
- Expose infrastructure information through Terraform outputs instead of repeatedly inspecting raw Terraform state
- Continue reviewing destructive Terraform plans before applying them

Problems encountered:
- `terraform plan` failed because the AWS CLI login session had expired
- `aws sso login` failed because the AWS CLI configuration was not IAM Identity Center/SSO based
- Authentication was restored with the AWS CLI login flow and verified with `aws sts get-caller-identity`
- This reinforced the distinction between AWS CLI login credentials and `aws sso login`

Current deployment flow:

Terraform
   |
   v
AWS EC2
   |
   | first boot
   v
cloud-init / user_data
   |
   +--> apt update
   +--> install Docker
   +--> enable/start Docker
   +--> pull GHCR image
   +--> start container
              |
              v
           FastAPI
              |
              +--> /health


## Local Kubernetes / Minikube Milestone

Completed:
- Minikube installed in Ubuntu/WSL
- Minikube configured to use the Docker driver
- Local single-node Kubernetes cluster created
- Kubernetes node verified as `Ready`
- `kubectl` successfully connected to the Minikube cluster
- `k8s/deployment.yaml` created
- FastAPI deployed from `ghcr.io/sciencedevsoso/devops-portfolio:latest`
- Kubernetes Deployment configured with one replica
- readiness probe configured against `/health`
- liveness probe configured against `/health`
- `k8s/service.yaml` created
- ClusterIP Service configured on port 8000
- Kubernetes rolling update observed after adding health probes
- application Pod reached `Ready 1/1`
- deliberate Pod deletion used to test Kubernetes self-healing
- Deployment automatically created a replacement Pod
- replacement Pod reached Running and Ready state
- `kubectl port-forward` used to access the ClusterIP Service locally
- `/health` successfully returned `{"status":"healthy"}` through the Kubernetes Service

Problems encountered:
- Minikube initially failed with `PROVIDER_DOCKER_VERSION_EXIT_1`
- `docker` was unavailable inside the WSL Ubuntu distro
- Docker Desktop WSL integration was re-enabled
- Docker client and Docker Desktop engine were verified with `docker version`
- Minikube then started successfully using the Docker driver

Key lessons:
- Pods are disposable runtime units
- Deployments maintain desired application state
- deleting a Pod does not delete the application when a Deployment manages it
- Services provide stable networking in front of disposable Pods
- ClusterIP Services are internal to the cluster
- `kubectl port-forward` provides temporary local access for development/testing
- readiness probes control whether a Pod should receive traffic
- liveness probes help Kubernetes detect unhealthy application containers
