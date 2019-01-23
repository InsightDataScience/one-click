from pathlib import Path

import click
import python_terraform as pt


BASE_DIR = Path(__file__).parent
TERRAFORM_DIR = BASE_DIR / 'terraform'


@click.command()
@click.option('--public_key_path', default='~/.ssh/id_rsa.pub')
@click.option('--private_key_path', default='~/.ssh/id_rsa')
@click.argument('git_path')
def main(git_path, public_key_path=None, private_key_path=None):
    var = {
        'path_to_public_key': public_key_path,
        'path_to_private_key': private_key_path,
        'github_clone_link': git_path,
    }

    tf = pt.Terraform(working_dir=TERRAFORM_DIR)
    tf.apply(var=var, capture_output=False)
