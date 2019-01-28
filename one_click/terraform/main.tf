provider "aws" {
    region = "us-west-2"
}

resource "random_string" "deployment_id" {
  length = 6
  special = false
}

resource aws_key_pair "one_click" {
    key_name = "one-click-key - ${random_string.deployment_id.result}"
    public_key = "${file("${var.path_to_public_key}")}"
}

resource "aws_instance" "flask_server" {
    ami = "ami-70e90210",
    instance_type = "t2.micro"
    key_name = "${aws_key_pair.one_click.key_name}"

    vpc_security_group_ids = ["${aws_security_group.allow_flask_and_ssh.id}"]

    tags {
        Name = "flask-server - ${random_string.deployment_id.result}"
    }
}

module "provision_project" {
    source = "./provision_project"

    host = "${aws_instance.flask_server.public_ip}"
    path_to_private_key = "${var.path_to_private_key}"
    base_directory = "${var.base_directory}"
    project_link_or_path = "${var.project_link_or_path}"
    image_version = "${var.image_version}"
    use_github = "${var.use_github}"
    use_local = "${var.use_local}"
    public_ip = "${aws_instance.flask_server.public_ip}"
}

resource "aws_security_group" "allow_flask_and_ssh" {
    name = "allow_flask_and_ssh - ${random_string.deployment_id.result}"

    ingress {
        protocol = "tcp"
        from_port = 80
        to_port = 80
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        protocol = "tcp"
        from_port = 22
        to_port = 22
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}
