from unittest.mock import Mock, patch

import pytest

from saml2awsmulti.saml2aws_helper import Saml2AwsHelper


class TestSaml2AwsHelper:
    def test_init(self):
        helper = Saml2AwsHelper("config_file", "3600", True)
        assert helper._configfile == "config_file"
        assert helper._session_duration == "3600"
        assert helper._browser_autofill is True
        assert helper._uname is None
        assert helper._upass is None

    @patch("saml2awsmulti.saml2aws_helper.load_saml2aws_config")
    @patch("builtins.input")
    @patch("getpass.getpass")
    def test_get_credentials_from_config(self, mock_getpass, mock_input, mock_load_config):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "<test_password>"

        helper = Saml2AwsHelper("config_file", None, False)
        username, password = helper.get_credentials()

        assert username == "testuser"
        assert password == "<test_password>"
        mock_input.assert_not_called()
        mock_getpass.assert_called_once()

    @patch("saml2awsmulti.saml2aws_helper.load_saml2aws_config")
    @patch("builtins.input")
    @patch("getpass.getpass")
    def test_get_credentials_no_config_username(self, mock_getpass, mock_input, mock_load_config):
        mock_load_config.return_value = {}
        mock_input.return_value = "testuser"
        mock_getpass.return_value = "testpass"

        helper = Saml2AwsHelper("config_file", None, False)
        username, password = helper.get_credentials()

        assert username == "testuser"
        assert password == "testpass"
        mock_input.assert_called_once_with("Username: ")
        mock_getpass.assert_called_once()

    @patch("saml2awsmulti.saml2aws_helper.load_saml2aws_config")
    @patch("getpass.getpass")
    def test_get_credentials_cached(self, mock_getpass, mock_load_config):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "testpass"

        helper = Saml2AwsHelper("config_file", None, False)
        # First call
        username1, password1 = helper.get_credentials()
        # Second call should use cached values
        username2, password2 = helper.get_credentials()

        assert username1 == username2 == "testuser"
        assert password1 == password2 == "testpass"
        # Should only call getpass once
        mock_getpass.assert_called_once()

    @patch("saml2awsmulti.saml2aws_helper.load_saml2aws_config")
    @patch("getpass.getpass")
    @patch("subprocess.Popen")
    def test_run_saml2aws_list_roles_success(self, mock_popen, mock_getpass, mock_load_config):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "testpass"

        # Mock subprocess output
        mock_process = Mock()
        mock_process.communicate.return_value = (
            b"Account: aws-01 (123456789012)\narn:aws:iam::123456789012:role/dev\n"
            b"Account: aws-02 (213456789012)\narn:aws:iam::213456789012:role/test\n",
            None,
        )
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        helper = Saml2AwsHelper("config_file", None, False)
        result = helper.run_saml2aws_list_roles()

        expected = [
            ("arn:aws:iam::123456789012:role/dev", "aws-01"),
            ("arn:aws:iam::213456789012:role/test", "aws-02"),
        ]
        assert result == expected
        mock_popen.assert_called_once()
        # Password must be sent via stdin, not in the command
        mock_process.communicate.assert_called_once_with(input=b"testpass\n")
        cmd_args = mock_popen.call_args[0][0]
        assert "--stdin-password" in cmd_args
        assert not any("password" in arg.lower() and "stdin" not in arg for arg in cmd_args)

    @patch("saml2awsmulti.saml2aws_helper.load_saml2aws_config")
    @patch("getpass.getpass")
    @patch("subprocess.Popen")
    def test_run_saml2aws_list_roles_no_account_alias(
        self, mock_popen, mock_getpass, mock_load_config
    ):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "testpass"

        # Mock subprocess output with no account alias
        mock_process = Mock()
        mock_process.communicate.return_value = (
            b"Account: 123456789012\narn:aws:iam::123456789012:role/dev\n",
            None,
        )
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        helper = Saml2AwsHelper("config_file", None, False)
        result = helper.run_saml2aws_list_roles()

        expected = [("arn:aws:iam::123456789012:role/dev", "None")]
        assert result == expected

    @patch("saml2awsmulti.saml2aws_helper.load_saml2aws_config")
    @patch("getpass.getpass")
    @patch("subprocess.Popen")
    def test_run_saml2aws_list_roles_no_roles(self, mock_popen, mock_getpass, mock_load_config):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "testpass"

        # Mock subprocess output with no roles
        mock_process = Mock()
        mock_process.communicate.return_value = (b"Account: aws-01 (123456789012)\n", None)
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        helper = Saml2AwsHelper("config_file", None, False)

        with pytest.raises(ValueError, match="Failed to retrieve roles with saml2aws"):
            helper.run_saml2aws_list_roles()

    @patch("saml2awsmulti.saml2aws_helper.load_saml2aws_config")
    @patch("getpass.getpass")
    @patch("subprocess.Popen")
    def test_run_saml2aws_list_roles_parse_error(self, mock_popen, mock_getpass, mock_load_config):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "testpass"

        # Mock subprocess output with malformed account line
        mock_process = Mock()
        mock_process.communicate.return_value = (
            b"Account: malformed line\narn:aws:iam::123456789012:role/dev\n",
            None,
        )
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        helper = Saml2AwsHelper("config_file", None, False)

        with pytest.raises(KeyError):
            helper.run_saml2aws_list_roles()

    @patch("saml2awsmulti.saml2aws_helper.load_saml2aws_config")
    @patch("getpass.getpass")
    @patch("subprocess.Popen")
    def test_run_saml2aws_list_roles_account_parse_exception(
        self, mock_popen, mock_getpass, mock_load_config, caplog
    ):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "testpass"

        # A malformed account line with too many parts triggers the except block
        # (ValueError: too many values to unpack). A subsequent valid account and
        # ARN line allow normal completion.
        mock_process = Mock()
        mock_process.communicate.return_value = (
            b"Account: ALIAS (123) extra\n"
            b"Account: aws-01 (123456789012)\n"
            b"arn:aws:iam::123456789012:role/dev\n",
            None,
        )
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        with caplog.at_level("ERROR"):
            helper = Saml2AwsHelper("config_file", None, False)
            result = helper.run_saml2aws_list_roles()

        assert result == [("arn:aws:iam::123456789012:role/dev", "aws-01")]
        assert "Account: ALIAS (123) extra" in caplog.text

    @patch("saml2awsmulti.saml2aws_helper.load_saml2aws_config")
    @patch("getpass.getpass")
    @patch("subprocess.Popen")
    def test_run_saml2aws_login_success(self, mock_popen, mock_getpass, mock_load_config):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "testpass"

        mock_process = Mock()
        mock_process.communicate.return_value = (b"Login successful\n", None)
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        helper = Saml2AwsHelper("config_file", None, False)
        result = helper.run_saml2aws_login("arn:aws:iam::123456789012:role/dev", "dev")

        assert result == 0
        mock_popen.assert_called_once()

    @patch("saml2awsmulti.saml2aws_helper.load_saml2aws_config")
    @patch("getpass.getpass")
    @patch("subprocess.Popen")
    def test_run_saml2aws_login_with_session_duration(
        self, mock_popen, mock_getpass, mock_load_config
    ):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "testpass"

        mock_process = Mock()
        mock_process.communicate.return_value = (b"Login successful\n", None)
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        helper = Saml2AwsHelper("config_file", "7200", False)
        helper.run_saml2aws_login("arn:aws:iam::123456789012:role/dev", "dev")

        # Check that session duration was included in command
        call_args = mock_popen.call_args[0][0]
        assert "--session-duration=7200" in call_args

    @patch("saml2awsmulti.saml2aws_helper.load_saml2aws_config")
    @patch("getpass.getpass")
    @patch("subprocess.Popen")
    def test_run_saml2aws_login_with_browser_autofill(
        self, mock_popen, mock_getpass, mock_load_config
    ):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "testpass"

        mock_process = Mock()
        mock_process.communicate.return_value = (b"Login successful\n", None)
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        helper = Saml2AwsHelper("config_file", None, True)
        helper.run_saml2aws_login("arn:aws:iam::123456789012:role/dev", "dev")

        # Check that browser autofill was included in command
        call_args = mock_popen.call_args[0][0]
        assert "--browser-autofill" in call_args

    @patch("saml2awsmulti.saml2aws_helper.load_saml2aws_config")
    @patch("getpass.getpass")
    @patch("subprocess.Popen")
    def test_run_saml2aws_login_failure(self, mock_popen, mock_getpass, mock_load_config):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "testpass"

        mock_process = Mock()
        mock_process.communicate.return_value = (b"Login failed\n", None)
        mock_process.returncode = 1
        mock_popen.return_value = mock_process

        helper = Saml2AwsHelper("config_file", None, False)
        result = helper.run_saml2aws_login("arn:aws:iam::123456789012:role/dev", "dev")

        assert result == 1

    @patch("saml2awsmulti.saml2aws_helper.load_saml2aws_config")
    @patch("getpass.getpass")
    @patch("subprocess.Popen")
    def test_run_saml2aws_login_command_format(self, mock_popen, mock_getpass, mock_load_config):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "testpass"

        mock_process = Mock()
        mock_process.communicate.return_value = (b"Login successful\n", None)
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        helper = Saml2AwsHelper("config_file", "3600", True)
        helper.run_saml2aws_login("arn:aws:iam::123456789012:role/dev", "dev")

        # Verify the command is a list (no shell=True) and contains expected args
        call_args = mock_popen.call_args[0][0]
        assert isinstance(call_args, list)
        assert "saml2aws" in call_args
        assert "login" in call_args
        assert "--role=arn:aws:iam::123456789012:role/dev" in call_args
        assert "-p" in call_args
        assert "dev" in call_args
        assert "--username=testuser" in call_args
        assert "--skip-prompt" in call_args
        assert "--stdin-password" in call_args
        assert "--session-duration=3600" in call_args
        assert "--browser-autofill" in call_args
        # Password must NOT appear in the command args
        assert not any("testpass" in arg for arg in call_args)
        # Password sent via stdin
        mock_process.communicate.assert_called_once_with(input=b"testpass\n")
