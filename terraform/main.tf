provider "aws" {
  region = var.region
  default_tags {
    tags = {
      Owner   = "mlabecki"
      Project = "2023_internship_warsaw_mlabecki"
    }
  }
}
data "aws_ami" "al2023" {
  most_recent = true
  filter {
    name = "name"
    values = ["al2023-ami-*-x86_64"]
  }
  filter {
    name = "architecture"
    values = ["x86_64"]
  }

  owners = ["amazon"]
}
module "network" {
  source = "./modules/network"
  subnet_list = {
    tf_task_mlabeckiSUBNET1 = {
      ip = "10.0.1.0/24"
      az = "${var.region}a"
    }
    tf_task_mlabeckiSUBNET2 = {
      ip = "10.0.2.0/24"
      az = "${var.region}b"
    }
  }
}
module "compute" {
  count = 3
  source = "./modules/compute"
  current_count = count.index

  subnet_ids = module.network.subnet_ids
  ami_id = data.aws_ami.al2023.id
}
resource "aws_lb" "this" {
  name = "tf-lb-mlabecki"
  internal = false
  load_balancer_type = "application"
  subnets = module.network.subnet_ids
    tags = {
    Name = "tf_task_mlabeckiLB"
  }
}
resource "aws_lb_target_group" "this" {
  name = "tf-task-mlabecki-group"
  port = 80
  protocol = "HTTP"
  vpc_id = module.network.vpc_id
}
resource "aws_lb_target_group_attachment" "this" {
  for_each = {for i, val in module.compute[*].instance_id: i => val}
  target_group_arn = aws_lb_target_group.this.arn
  target_id = each.value
}
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.this.arn
  port = "80"
  protocol = "HTTP"
  default_action {
    type = "forward"
    target_group_arn = aws_lb_target_group.this.arn
  }
}

