variable "aws_region" {
  description = "AWS region where resources are created"
  type        = string
  default     = "eu-north-1"
}

variable "ami_id" {
  description = "AMI ID used for the EC2 instance"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "subnet_id" {
  description = "Subnet where the EC2 instance is launched"
  type        = string
}

variable "key_name" {
  description = "Existing EC2 SSH key pair name"
  type        = string
}

variable "developer_ssh_cidr" {
  description = "CIDR allowed to SSH into the EC2 instance"
  type        = string
}
