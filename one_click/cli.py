from pathlib import Path

import click
import python_terraform as pt

from one_click import utils


DEPLOYMENT_DIR = Path.cwd()
BASE_DIR = Path(__file__).parent
TERRAFORM_DIR = str(BASE_DIR / "terraform")


def deploy(
    project_link_or_path,
    public_key_path,
    private_key_path,
    py,
    deployment_source="github",
):
    image_version = utils.py_version_to_image(py)
    github_local_switches = {}
    var = {
        "base_directory": str(BASE_DIR),
        "path_to_public_key": public_key_path,
        "path_to_private_key": private_key_path,
        "project_link_or_path": project_link_or_path,
        "image_version": image_version,
        **github_local_switches[deployment_source],
    }

    tfvars = utils.dict_to_tfvars(var)
    with open(DEPLOYMENT_DIR / "terraform.tfvars", "w") as f:
        f.write(tfvars)

    tf = pt.Terraform()
    tf.init(
        dir_or_plan=str(DEPLOYMENT_DIR),
        from_module=TERRAFORM_DIR,
        capture_output=False,
    )
    return_code, _, _ = tf.apply(var=var, capture_output=False)


@click.group()
def main():
    pass


def deployment_options(deployment_function):
    deployment_function = click.option(
        "--py",
        default="3.7",
        help='Python version. Options are 3.7, 3.6, 3.5, 2.7.',
    )(deployment_function)
    deployment_function = click.option(
        "--private_key_path", default="~/.ssh/id_rsa"
    )(deployment_function)
    deployment_function = click.option(
        "--public_key_path", default="~/.ssh/id_rsa.pub"
    )(deployment_function)
    deployment_function = main.command()(deployment_function)

    return deployment_function


@deployment_options
@click.argument("git_path")
def deploy_github(
    git_path, public_key_path=None, private_key_path=None, py=None
):
    deploy(
        git_path,
        public_key_path,
        private_key_path,
        py,
        deployment_source="github",
    )


@deployment_options
@click.argument("local_path")
def deploy_local(
    local_path, public_key_path=None, private_key_path=None, py=None
):
    deploy(
        local_path,
        public_key_path,
        private_key_path,
        py,
        deployment_source="local",
    )


@main.command()
def destroy():
    # Ensure that the proper backend files are in the deployment directory
    utils.pre_destroy_check(DEPLOYMENT_DIR)

    tf = pt.Terraform()
    tf.destroy(capture_output=False)
