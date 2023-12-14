output "vpc_id" {
  description = "ID of the main VPC"
  value = aws_vpc.this.id
}
output "subnet_ids" {
  description = "Created subnets"
  value = [ for subnet in aws_subnet.this : subnet.id ]
}