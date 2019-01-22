provider "aws" {
    region = "us-west-2"
    access_key = "${var.aws_access_key}"
    secret_key = "${var.aws_secret_key}"
}

resource aws_key_pair "one_click" {
    key_name = "one-click-key"
    public_key = "${file("${var.path_to_public_key}")}"
}

resource "aws_instance" "flask_server" {
    ami = "ami-70e90210",
    instance_type = "t2.medium"
    key_name = "${aws_key_pair.one_click.key_name}"

    vpc_security_group_ids = ["${aws_security_group.allow_flask_and_ssh.id}"]

    tags {
        Name = "flask-server"
    }

    connection {
            type = "ssh"
            user = "ubuntu"
            private_key = "${file("${var.path_to_private_key}")}"
    }

    provisioner "file" {
        source = "../resources/app"
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
    name = "allow_flask_and_ssh"

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

variable "aws_access_key" {
	description = "AWS access key (e.g. ABCDE1F2G3HIJKLMNOP )"	
}

variable "aws_secret_key" {
	description = "AWS secret key (e.g. 1abc2d34e/f5ghJKlmnopqSr678stUV/WXYZa12 )"	
}

variable "github_clone_link" {}

variable "path_to_public_key" {}

variable "path_to_private_key" {}

output "public_dns" {
    value = "${aws_instance.flask_server.public_dns}"
}
