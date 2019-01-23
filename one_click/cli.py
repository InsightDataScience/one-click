from pathlib import Path

import click
import python_terraform as pt

from one_click import utils


BACKEND_DIR = str(Path.cwd())
BASE_DIR = Path(__file__).parent
TERRAFORM_DIR = str(BASE_DIR / "terraform")


@click.group()
def main():
    pass


@main.command()
@click.option("--public_key_path", default="~/.ssh/id_rsa.pub")
@click.option("--private_key_path", default="~/.ssh/id_rsa")
@click.argument("git_path")
def deploy(git_path, public_key_path=None, private_key_path=None):
    var = {
        "base_directory": str(BASE_DIR),
        "path_to_public_key": public_key_path,
        "path_to_private_key": private_key_path,
        "github_clone_link": git_path,
    }

    tf = pt.Terraform()
    tf.init(
        dir_or_plan=BACKEND_DIR,
        from_module=TERRAFORM_DIR,
        capture_output=False,
    )
    return_code, _, _ = tf.apply(var=var, capture_output=False)

    if not return_code:
        tfvars = utils.dict2tfvars(var)
        with open(Path.cwd() / "terraform.tfvars", "w") as f:
            f.write(tfvars)


@main.command()
def destroy():
    tf = pt.Terraform()
    tf.destroy(capture_output=False)
