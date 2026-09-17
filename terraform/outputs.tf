output "default_vpc_cidr" {
  value = data.aws_vpc.default.cidr_block
}
