resource "null_resource" "remote_exec_from_github" {
    count = "${var.use_github}"

    connection {
        host = "${var.host}"
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
            "git clone ${var.project_link_or_path} ./app/app",
            "mv app/uwsgi.ini ./app/app/",
            "sudo apt-get update && sudo apt-get install -y docker.io",
            "sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose",
            "sudo chmod +x /usr/local/bin/docker-compose",
            "sudo usermod -aG docker",
            "cd ./app",
            "docker-compose build --build-arg IMAGE=${var.image_version} app",
            "docker-compose up -d"
        ]
    }
}

resource "null_resource" "remote_exec_from_local" {
    count = "${var.use_local}"

    connection {
        host = "${var.host}"
        type = "ssh"
        user = "ubuntu"
        private_key = "${file("${var.path_to_private_key}")}"
    }

    provisioner "file" {
        source = "${var.base_directory}/resources/app"
        destination = "/home/ubuntu/app/"
    }

    provisioner "local-exec" {
        command = "rsync -avz --progress -e \"ssh -o StrictHostKeyChecking=no\" ${var.project_link_or_path}/ ubuntu@${var.public_ip}:/home/ubuntu/app/app"
    }

    provisioner "remote-exec" {
        inline = [
            "mv app/uwsgi.ini ./app/app/",
            "sudo apt-get update && sudo apt-get install -y docker.io",
            "sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose",
            "sudo chmod +x /usr/local/bin/docker-compose",
            "sudo usermod -aG docker",
            "cd ./app",
            "sudo docker-compose build --build-arg IMAGE=${var.image_version} app",
            "sudo docker-compose up -d"
        ]
    }
}