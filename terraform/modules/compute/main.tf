resource "aws_instance" "this" {
  instance_type = "t3.micro"
  subnet_id = "${var.subnet_ids[ var.current_count % length(var.subnet_ids) ]}"
  ami = var.ami_id
  user_data = "${file("instance-user-data.sh")}"
  tags = {
    Name = "tf_web_instance_mlabecki"
  }
  associate_public_ip_address = true
}