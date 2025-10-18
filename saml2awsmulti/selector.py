from InquirerPy import inquirer
from InquirerPy.base.control import Choice

# To use custom styles, see:
# https://inquirerpy.readthedocs.io/en/latest/pages/style.html?highlight=style#customising-style


def prompt_profile_selection(options):
    if not options:
        raise ValueError("No profiles retrieved for selection.")

    return inquirer.select(
        message="Please choose the profile",
        choices=options,
        default=None,
    ).execute()


def prompt_roles_selection(options, last_selected_options):
    if not options:
        raise ValueError("No roles retrieved for selection.")

    choices = [Choice(role, enabled=role in last_selected_options) for role in options]

    return inquirer.checkbox(
        message="Please choose the role",
        choices=choices,
        cycle=True,
        transformer=lambda result: f"{len(result)} role(s) selected",
    ).execute()
