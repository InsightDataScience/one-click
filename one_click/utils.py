from typing import Dict


def dict2tfvars(vars: Dict[str, str]) -> str:
    """
    Convert a dictionary of strings to a string suitable for a tfvars file
    (or a bash enviornment variable file for that matter)
    """
    return "\n".join(f"{key} = \"{val}\"" for key, val in vars.items())
