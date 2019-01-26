from typing import Dict, Optional

import click


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


def pre_destroy_check(deployment_directory):
    required_state_files = (
        ".terraform",
        "main.tf",
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
