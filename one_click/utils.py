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
