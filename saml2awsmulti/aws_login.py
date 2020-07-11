"""
A helper script using saml2aws to login and retrieve AWS temporary credentials for multiple roles in different accounts.
"""
import click
from collections import OrderedDict
import logging
from os.path import exists, join
from pathlib import Path

from saml2awsmulti.file_io import (
    get_aws_profiles,
    read_csv,
    read_lines_from_file,
    write_aws_profiles,
    write_csv,
)
from saml2awsmulti.saml2aws_helper import Saml2AwsHelper
from saml2awsmulti.selector import (
    prompt_profile_selection,
    prompt_roles_selection,
)

logging.basicConfig(format="%(message)s")
logging.getLogger().setLevel(logging.INFO)

AWS_CRED_FILE = join(str(Path.home()), ".aws", "credentials")
SAML2AWS_CONFIG_FILE = join(str(Path.home()), ".saml2aws")
USER_DATA_HOME = join(str(Path.home()), ".saml2aws-multi")
ALL_ROLES_FILE = join(USER_DATA_HOME, "aws_login_roles.csv")    # role_arn, account_alias
LAST_SELECTED_FILE = join(USER_DATA_HOME, "aws_login_last_selected.txt")    # aws_profile_name

DEFAULT_PROFILE_NAME_FORMAT = "RoleName"
PROFILE_NAME_FORMATS = ["RoleName", "RoleName-AccountAlias"]


def create_profile_name_from_role_arn(role_arn, account_alias, profile_name_format):
    """Create a profile name for a give role ARN and account alias."""
    profile_name = role_arn.split("role/")[-1].replace("/", "-")
    if profile_name_format == "RoleName-AccountAlias":
        return f"{profile_name}-{account_alias}"
    return profile_name


def create_profile_rolearn_dict(saml2aws_helper, profile_name_format, refresh_cached_roles):
    if refresh_cached_roles or not exists(ALL_ROLES_FILE):
        rolearn_alias_list = saml2aws_helper.run_saml2aws_list_roles()
        write_csv(ALL_ROLES_FILE, rolearn_alias_list)
    else:
        rolearn_alias_list = read_csv(ALL_ROLES_FILE)
    
    profile_rolearn_dict = OrderedDict()
    for role_arn, account_alias in rolearn_alias_list:
        profile_name = create_profile_name_from_role_arn(role_arn, account_alias, profile_name_format)
        profile_rolearn_dict[profile_name] = role_arn
    return profile_rolearn_dict


def pre_select_options(profile_rolearn_dict, keyword):
    pre_select_profiles = read_lines_from_file(LAST_SELECTED_FILE)
    for profile_name, role_arn in profile_rolearn_dict.items():
        for k in keyword:
            if k in role_arn:
                pre_select_profiles.append(profile_name)
                break
    return pre_select_profiles


@click.group(invoke_without_command=True, help="Get credentials for multiple accounts with saml2aws")
@click.option("--keyword", "-k", multiple=True, help="Pre-select roles with the given keyword(s)")
@click.option("--profile-name-format", "-f", default=DEFAULT_PROFILE_NAME_FORMAT, show_default=True,
              help="Profile name format", type=click.Choice(PROFILE_NAME_FORMATS, case_sensitive=False))
@click.option("--refresh-cached-roles", "-r", is_flag=True, show_default=True)
@click.option("--session-duration", "-t", help="Session duration in seconds")
@click.option("--debug", "-d", is_flag=True, show_default=True)
def main_cli(keyword, profile_name_format, refresh_cached_roles, session_duration, debug):
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        saml2aws_helper = Saml2AwsHelper(SAML2AWS_CONFIG_FILE, session_duration)

        profile_rolearn_dict = create_profile_rolearn_dict(saml2aws_helper, profile_name_format, refresh_cached_roles)
        pre_select_profiles = pre_select_options(profile_rolearn_dict, keyword)

        answers = prompt_roles_selection(profile_rolearn_dict.keys(), pre_select_profiles)
        if answers.get("roles"):
            for profile in answers["roles"]:
                saml2aws_helper.run_saml2aws_login(profile_rolearn_dict[profile], profile)
    
            # Dump the last selected options
            with open(LAST_SELECTED_FILE, "w") as f:
                f.write("\n".join(answers["roles"]))
        else:
            logging.info("Nothing selected. Aborted.")
    except FileNotFoundError as e:
        if e.filename == SAML2AWS_CONFIG_FILE:
            logging.error(f"{e}. See https://github.com/Versent/saml2aws to create one.")
        else:
            logging.error(f"Error: {e} Aborted.")
    except Exception as e:
        import traceback
        traceback.print_exc()


@main_cli.command(help="Switch default profile")
def switch():
    config = get_aws_profiles(AWS_CRED_FILE)
    options = [profile for profile in config.sections() if profile != "default"]
    if options:
        answer = prompt_profile_selection(options)
        profile = answer.get("profile")
        if profile is not None:
            config["default"] = config[profile]
            write_aws_profiles(AWS_CRED_FILE, config)
            logging.info(f"Set the default profile to {profile}")
        else:
            logging.info("Nothing selected. Aborted.")
    else:
        logging.info("No non default aws profile found. Aborted.")


if __name__ == "__main__":
    main_cli()
