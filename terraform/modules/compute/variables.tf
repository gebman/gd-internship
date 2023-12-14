variable "subnet_ids" {
  type = list(string)
}
variable "ami_id" {
  type = string
}
variable "current_count" {
  default = 1
  type = number
}