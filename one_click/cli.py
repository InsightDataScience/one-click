from pathlib import Path

import click
import python_terraform as pt


BACKEND_DIR = str(Path.cwd())
BASE_DIR = Path(__file__).parent
TERRAFORM_DIR = str(BASE_DIR / "terraform")


@click.command()
@click.option("--public_key_path", default="~/.ssh/id_rsa.pub")
@click.option("--private_key_path", default="~/.ssh/id_rsa")
@click.argument("git_path")
def main(git_path, public_key_path=None, private_key_path=None):
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
    tf.apply(var=var, capture_output=False)
