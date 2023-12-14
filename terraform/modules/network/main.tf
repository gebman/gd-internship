resource "aws_vpc" "this" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "tf_task_mlabeckiVPC"
  }
}

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id

    tags = {
    Name = "tf_task_mlabeckiIGW"
  }
}

resource "aws_default_route_table" "this" {
  default_route_table_id = aws_vpc.this.default_route_table_id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.this.id
  }
  route {
    cidr_block = aws_vpc.this.cidr_block
    gateway_id = "local"
  }
}

resource "aws_default_security_group" "this" {
  vpc_id = aws_vpc.this.id
  ingress {
    protocol = "tcp"
    from_port = 80
    to_port = 80
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "tf_task_mlabeckiSG"
  }
}
resource "aws_subnet" "this" {
  vpc_id = aws_vpc.this.id
  for_each = var.subnet_list
  cidr_block = each.value.ip
  availability_zone = each.value.az
  tags = {
    Name = each.key
  }
}