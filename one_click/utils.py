from typing import Dict, Optional
from pathlib import Path

import click

BASE_DIR = str(Path(__file__).parent)


def dict_to_tfvars(vars: Dict[str, str]) -> str:
    """
    Convert a dictionary of strings to a string suitable for a tfvars file
    (or a bash enviornment variable file for that matter)
    """
    return "\n".join(f"{key} = \"{val}\"" for key, val in vars.items())


def py_version_to_image(py_version: str) -> Optional[str]:
    if py_version not in {"3.7", "3.6", "3.5", "2.7"}:
        raise click.BadParameter(
            'Invalid version of Python',
            param=py_version,
            param_hint=["3.7", "3.6", "3.5", "2.7"],
        )
    return f"tiangolo/uwsgi-nginx-flask:python{py_version}"


def build_and_validate_tfvars(
    project_link_or_path,
    public_key_path,
    private_key_path,
    py,
    instance_type,
    deployment_source="github",
):
    # Drop trailing slash from local path so it doesn't interfere with rsync
    if (deployment_source == "local") and (project_link_or_path[-1] == "/"):
        project_link_or_path = project_link_or_path[:-1]

    github_local_switches = {
        "github": {"use_github": 1, "use_local": 0},
        "local": {"use_github": 0, "use_local": 1},
    }

    image_tag = py_version_to_image(py)

    var = {
        "base_directory": str(BASE_DIR),
        "path_to_public_key": public_key_path,
        "path_to_private_key": private_key_path,
        "project_link_or_path": project_link_or_path,
        "image_version": image_tag,
        "instance_type": instance_type,
        **github_local_switches[deployment_source],
    }

    return dict_to_tfvars(var)


def pre_destroy_check(deployment_directory):
    required_state_files = (
        ".terraform",
        "terraform.tfstate",
        "terraform.tfvars",
    )
    has_all_required_files = all(
        map(
            lambda path: any(deployment_directory.glob(path)),
            required_state_files,
        )
    )
    if not has_all_required_files:
        raise click.UsageError(
            f"""
            Deployment directory is missing some or all of the required state
            files: {required_state_files}. Make sure that you actually have a
            project deployed and that you are in its correct directory."""
        )
