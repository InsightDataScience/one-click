output "public_dns" {
    value = "${aws_instance.flask_server.public_dns}"
}