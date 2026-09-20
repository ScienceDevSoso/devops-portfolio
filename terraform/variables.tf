variable "aws_region" {
  description = "AWS region for the EKS cluster"
  type        = string
  default     = "eu-north-1"
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "devops-portfolio-eks"
}

variable "kubernetes_version" {
  description = "Kubernetes version used by EKS"
  type        = string
  default     = "1.36"
}

variable "node_instance_type" {
  description = "EC2 instance type used by the EKS managed node group"
  type        = string
  default     = "t3.small"
}

variable "developer_api_cidr" {
  description = "CIDR allowed to access the public Kubernetes API endpoint"
  type        = string
}
