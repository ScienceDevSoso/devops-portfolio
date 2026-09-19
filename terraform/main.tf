data "aws_vpc" "default" {
  default = true
}

resource "aws_security_group" "app" {
  name        = "devops-portfolio-app"
  description = "Security group for the DevOps portfolio application"
  vpc_id      = data.aws_vpc.default.id
}

resource "aws_vpc_security_group_egress_rule" "allow_all_outbound" {
  security_group_id = aws_security_group.app.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

resource "aws_vpc_security_group_ingress_rule" "allow_app_port" {
  security_group_id = aws_security_group.app.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 8000
  to_port           = 8000
  ip_protocol       = "tcp"
}

resource "aws_instance" "app" {
  ami                         = "ami-0aba19e56f3eaec05"
  instance_type               = "t3.micro"
  key_name                    = "devops-portfolio-ec2-key"
  subnet_id                   = "subnet-047c7f9d3d19817a4"
  vpc_security_group_ids      = [aws_security_group.app.id]
  associate_public_ip_address = true

  tags = {
    Name = "devops-portfolio-app"
  }
}

resource "aws_vpc_security_group_ingress_rule" "allow_ssh" {
  security_group_id = aws_security_group.app.id
  cidr_ipv4         = "147.235.195.181/32"
  from_port         = 22
  to_port           = 22
  ip_protocol       = "tcp"
}
