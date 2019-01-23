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
    instance_type = "t2.medium"
    key_name = "${aws_key_pair.one_click.key_name}"

    vpc_security_group_ids = ["${aws_security_group.allow_flask_and_ssh.id}"]

    tags {
        Name = "flask-server - ${random_string.deployment_id.result}"
    }

    connection {
            type = "ssh"
            user = "ubuntu"
            private_key = "${file("${var.path_to_private_key}")}"
    }

    provisioner "file" {
        source = "${var.base_directory}/resources/app"
        destination = "/home/ubuntu/app/"
    }

    provisioner "remote-exec" {
        inline = [
            "mkdir ./app/app",
            "git clone ${var.github_clone_link} ./app/app",
            "mv app/uwsgi.ini ./app/app/",
            "sudo apt-get update && sudo apt-get install -y docker.io",
            "sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose",
            "sudo chmod +x /usr/local/bin/docker-compose",
            "cd ./app",
            "sudo docker-compose up -d"
        ]
    }
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

variable "base_directory" {}

variable "github_clone_link" {}

variable "path_to_public_key" {}

variable "path_to_private_key" {}

output "public_dns" {
    value = "${aws_instance.flask_server.public_dns}"
}
