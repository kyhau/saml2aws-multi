import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, mock_open, patch

import pytest
from click.testing import CliRunner

from saml2awsmulti.aws_login import (chained,
                                     create_profile_name_from_role_arn,
                                     create_profile_rolearn_dict, main_cli,
                                     pre_select_options, switch, whoami)


class TestCreateProfileNameFromRoleArn:
    def test_role_name_format(self):
        role_arn = "arn:aws:iam::123456789012:role/dev"
        account_alias = "aws-01"

        result = create_profile_name_from_role_arn(
            role_arn, account_alias, "RoleName"
        )
        assert result == "dev"

    def test_role_name_account_alias_format(self):
        role_arn = "arn:aws:iam::123456789012:role/dev"
        account_alias = "aws-01"

        result = create_profile_name_from_role_arn(
            role_arn, account_alias, "RoleName-AccountAlias"
        )
        assert result == "dev-aws-01"

    def test_role_with_slashes(self):
        role_arn = "arn:aws:iam::123456789012:role/team/subteam/dev"
        account_alias = "aws-01"

        result = create_profile_name_from_role_arn(
            role_arn, account_alias, "RoleName"
        )
        assert result == "team-subteam-dev"

    def test_role_name_account_alias_with_slashes(self):
        role_arn = "arn:aws:iam::123456789012:role/team/subteam/dev"
        account_alias = "aws-01"

        result = create_profile_name_from_role_arn(
            role_arn, account_alias, "RoleName-AccountAlias"
        )
        assert result == "team-subteam-dev-aws-01"


class TestCreateProfileRolearnDict:
    @patch('saml2awsmulti.aws_login.exists')
    @patch('saml2awsmulti.aws_login.write_csv')
    @patch('saml2awsmulti.aws_login.read_csv')
    def test_with_refresh_cached_roles(self, mock_read_csv, mock_write_csv, mock_exists):
        mock_exists.return_value = True
        mock_helper = Mock()
        mock_helper.run_saml2aws_list_roles.return_value = [
            ("arn:aws:iam::123456789012:role/dev", "aws-01"),
            ("arn:aws:iam::213456789012:role/test", "aws-02")
        ]

        result = create_profile_rolearn_dict(mock_helper, "RoleName", True, [])

        mock_helper.run_saml2aws_list_roles.assert_called_once()
        mock_write_csv.assert_called_once()
        assert len(result) == 2
        assert result["dev"] == "arn:aws:iam::123456789012:role/dev"
        assert result["test"] == "arn:aws:iam::213456789012:role/test"

    @patch('saml2awsmulti.aws_login.exists')
    @patch('saml2awsmulti.aws_login.read_csv')
    def test_with_cached_roles(self, mock_read_csv, mock_exists):
        mock_exists.return_value = True
        mock_read_csv.return_value = [
            ("arn:aws:iam::123456789012:role/dev", "aws-01"),
            ("arn:aws:iam::213456789012:role/test", "aws-02")
        ]
        mock_helper = Mock()

        result = create_profile_rolearn_dict(mock_helper, "RoleName", False, [])

        mock_read_csv.assert_called_once()
        mock_helper.run_saml2aws_list_roles.assert_not_called()
        assert len(result) == 2

    @patch('saml2awsmulti.aws_login.exists')
    @patch('saml2awsmulti.aws_login.read_csv')
    def test_with_keywords_filter(self, mock_read_csv, mock_exists):
        mock_exists.return_value = True
        mock_read_csv.return_value = [
            ("arn:aws:iam::123456789012:role/dev", "aws-01"),
            ("arn:aws:iam::213456789012:role/test", "aws-02"),
            ("arn:aws:iam::313456789012:role/prod", "aws-03")
        ]
        mock_helper = Mock()

        result = create_profile_rolearn_dict(mock_helper, "RoleName", False, ["dev", "test"])

        assert len(result) == 2
        assert "dev" in result
        assert "test" in result
        assert "prod" not in result


class TestPreSelectOptions:
    @patch('saml2awsmulti.aws_login.read_lines_from_file')
    def test_with_last_selected(self, mock_read_lines):
        mock_read_lines.return_value = ["dev", "test"]
        profile_rolearn_dict = {
            "dev": "arn:aws:iam::123456789012:role/dev",
            "test": "arn:aws:iam::213456789012:role/test",
            "prod": "arn:aws:iam::313456789012:role/prod"
        }

        result = pre_select_options(profile_rolearn_dict, [])

        assert result == ["dev", "test"]

    @patch('saml2awsmulti.aws_login.read_lines_from_file')
    def test_with_keywords(self, mock_read_lines):
        mock_read_lines.return_value = []
        profile_rolearn_dict = {
            "dev": "arn:aws:iam::123456789012:role/dev",
            "test": "arn:aws:iam::213456789012:role/test",
            "prod": "arn:aws:iam::313456789012:role/prod"
        }

        result = pre_select_options(profile_rolearn_dict, ["dev"])

        assert result == ["dev"]

    @patch('saml2awsmulti.aws_login.read_lines_from_file')
    def test_invalid_last_selected_filtered(self, mock_read_lines):
        mock_read_lines.return_value = ["dev", "invalid", "test"]
        profile_rolearn_dict = {
            "dev": "arn:aws:iam::123456789012:role/dev",
            "test": "arn:aws:iam::213456789012:role/test"
        }

        result = pre_select_options(profile_rolearn_dict, [])

        assert result == ["dev", "test"]


class TestMainCli:
    @patch('saml2awsmulti.aws_login.Saml2AwsHelper')
    @patch('saml2awsmulti.aws_login.create_profile_rolearn_dict')
    @patch('saml2awsmulti.aws_login.pre_select_options')
    @patch('saml2awsmulti.aws_login.prompt_roles_selection')
    def test_main_cli_success(self, mock_prompt, mock_pre_select, mock_create_dict, mock_helper_class):
        runner = CliRunner()
        mock_helper = Mock()
        mock_helper_class.return_value = mock_helper
        mock_create_dict.return_value = {"dev": "arn:aws:iam::123456789012:role/dev"}
        mock_pre_select.return_value = ["dev"]
        mock_prompt.return_value = ["dev"]

        with patch('builtins.open', mock_open()) as mock_file:
            result = runner.invoke(main_cli, [])

        assert result.exit_code == 0
        mock_helper.run_saml2aws_login.assert_called_once()

    @patch('saml2awsmulti.aws_login.Saml2AwsHelper')
    def test_main_cli_file_not_found_saml2aws_config(self, mock_helper_class, caplog):
        runner = CliRunner()
        mock_helper_class.side_effect = FileNotFoundError("saml2aws config not found")

        with caplog.at_level("ERROR"):
            result = runner.invoke(main_cli, [])

        assert result.exit_code == 0  # Click handles exceptions gracefully
        assert "saml2aws config not found" in caplog.text

    @patch('saml2awsmulti.aws_login.Saml2AwsHelper')
    @patch('saml2awsmulti.aws_login.create_profile_rolearn_dict')
    @patch('saml2awsmulti.aws_login.pre_select_options')
    @patch('saml2awsmulti.aws_login.prompt_roles_selection')
    def test_main_cli_nothing_selected(self, mock_prompt, mock_pre_select, mock_create_dict, mock_helper_class, caplog):
        runner = CliRunner()
        mock_helper = Mock()
        mock_helper_class.return_value = mock_helper
        mock_create_dict.return_value = {"dev": "arn:aws:iam::123456789012:role/dev"}
        mock_pre_select.return_value = []
        mock_prompt.return_value = []

        with caplog.at_level("INFO"):
            result = runner.invoke(main_cli, [])

        assert result.exit_code == 0
        assert "Nothing selected. Aborted." in caplog.text
        mock_helper.run_saml2aws_login.assert_not_called()


class TestChainedCommand:
    @patch('saml2awsmulti.aws_login.get_aws_profiles')
    def test_chained_with_profiles(self, mock_get_profiles, caplog):
        runner = CliRunner()
        mock_config = Mock()
        mock_config.sections.return_value = ["profile dev", "profile test"]
        mock_config.__getitem__ = Mock(return_value={
            "source_profile": "base",
            "role_arn": "arn:aws:iam::123456789012:role/dev"
        })
        mock_get_profiles.return_value = mock_config

        with caplog.at_level("INFO"):
            result = runner.invoke(chained, [])

        assert result.exit_code == 0
        assert "Found 2 chained role profiles" in caplog.text

    @patch('saml2awsmulti.aws_login.get_aws_profiles')
    def test_chained_with_from_profile(self, mock_get_profiles):
        runner = CliRunner()
        mock_config = Mock()
        mock_config.sections.return_value = ["profile dev"]
        mock_config.__getitem__ = Mock(return_value={
            "source_profile": "base",
            "role_arn": "arn:aws:iam::123456789012:role/dev"
        })
        mock_get_profiles.return_value = mock_config

        result = runner.invoke(chained, ["--from-profile", "base"])

        assert result.exit_code == 0


class TestSwitchCommand:
    @patch('saml2awsmulti.aws_login.get_aws_profiles')
    @patch('saml2awsmulti.aws_login.write_aws_profiles')
    @patch('saml2awsmulti.aws_login.prompt_profile_selection')
    def test_switch_success(self, mock_prompt, mock_write, mock_get_profiles, caplog):
        runner = CliRunner()
        mock_config = Mock()
        mock_config.sections.return_value = ["default", "dev", "test"]
        mock_config.__getitem__ = Mock(return_value={"aws_access_key_id": "test"})
        mock_config.__setitem__ = Mock()  # Enable item assignment
        mock_get_profiles.return_value = mock_config
        mock_prompt.return_value = "dev"

        with caplog.at_level("INFO"):
            result = runner.invoke(switch, [])

        assert result.exit_code == 0
        assert "Set the default profile to dev" in caplog.text
        mock_write.assert_called_once()

    @patch('saml2awsmulti.aws_login.get_aws_profiles')
    def test_switch_no_profiles(self, mock_get_profiles, caplog):
        runner = CliRunner()
        mock_config = Mock()
        mock_config.sections.return_value = ["default"]
        mock_get_profiles.return_value = mock_config

        with caplog.at_level("INFO"):
            result = runner.invoke(switch, [])

        assert result.exit_code == 0
        assert "No non default aws profile found" in caplog.text


class TestWhoamiCommand:
    @patch('saml2awsmulti.aws_login.Session')
    def test_whoami_success(self, mock_session):
        runner = CliRunner()
        mock_client = Mock()
        mock_client.get_caller_identity.return_value = {
            "UserId": "test-user",
            "Account": "123456789012",
            "Arn": "arn:aws:iam::123456789012:user/test-user",
            "ResponseMetadata": {"RequestId": "test"}
        }
        mock_session.return_value.client.return_value = mock_client

        result = runner.invoke(whoami, [])

        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["UserId"] == "test-user"
        assert output["Account"] == "123456789012"
        assert "ResponseMetadata" not in output

    @patch('saml2awsmulti.aws_login.Session')
    def test_whoami_with_profile(self, mock_session):
        runner = CliRunner()
        mock_client = Mock()
        mock_client.get_caller_identity.return_value = {
            "UserId": "test-user",
            "Account": "123456789012",
            "Arn": "arn:aws:iam::123456789012:user/test-user"
        }
        mock_session.return_value.client.return_value = mock_client

        result = runner.invoke(whoami, ["--profile", "dev"])

        assert result.exit_code == 0
        mock_session.assert_called_once_with(profile_name="dev")

    @patch('saml2awsmulti.aws_login.Session')
    def test_whoami_error(self, mock_session, caplog):
        runner = CliRunner()
        mock_session.side_effect = Exception("AWS credentials not found")

        with caplog.at_level("ERROR"):
            result = runner.invoke(whoami, [])

        assert result.exit_code == 0
        assert "AWS credentials not found" in caplog.text
