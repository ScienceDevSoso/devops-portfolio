output "default_vpc_cidr" {
  description = "CIDR block of the default VPC"
  value       = data.aws_vpc.default.cidr_block
}

output "ec2_instance_id" {
  description = "ID of the application EC2 instance"
  value       = aws_instance.app.id
}

output "ec2_public_ip" {
  description = "Public IPv4 address of the application EC2 instance"
  value       = aws_instance.app.public_ip
}

output "application_url" {
  description = "Public URL of the FastAPI application"
  value       = "http://${aws_instance.app.public_ip}:8000"
}
