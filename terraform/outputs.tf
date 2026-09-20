output "default_vpc_cidr" {
  description = "CIDR block of the default VPC"
  value       = data.aws_vpc.default.cidr_block
}
