import subprocess
from unittest.mock import Mock, mock_open, patch

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

    @patch('saml2awsmulti.saml2aws_helper.load_saml2aws_config')
    @patch('builtins.input')
    @patch('getpass.getpass')
    def test_get_credentials_from_config(self, mock_getpass, mock_input, mock_load_config):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "testpass"

        helper = Saml2AwsHelper("config_file", None, False)
        username, password = helper.get_credentials()

        assert username == "testuser"
        assert password == "testpass"
        mock_input.assert_not_called()
        mock_getpass.assert_called_once()

    @patch('saml2awsmulti.saml2aws_helper.load_saml2aws_config')
    @patch('builtins.input')
    @patch('getpass.getpass')
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

    @patch('saml2awsmulti.saml2aws_helper.load_saml2aws_config')
    @patch('getpass.getpass')
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

    @patch('saml2awsmulti.saml2aws_helper.load_saml2aws_config')
    @patch('getpass.getpass')
    @patch('subprocess.Popen')
    def test_run_saml2aws_list_roles_success(self, mock_popen, mock_getpass, mock_load_config):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "testpass"

        # Mock subprocess output
        mock_process = Mock()
        mock_process.stdout.readlines.return_value = [
            b"Account: aws-01 (123456789012)\n",
            b"arn:aws:iam::123456789012:role/dev\n",
            b"Account: aws-02 (213456789012)\n",
            b"arn:aws:iam::213456789012:role/test\n"
        ]
        mock_process.wait.return_value = 0
        mock_popen.return_value = mock_process

        helper = Saml2AwsHelper("config_file", None, False)
        result = helper.run_saml2aws_list_roles()

        expected = [
            ("arn:aws:iam::123456789012:role/dev", "aws-01"),
            ("arn:aws:iam::213456789012:role/test", "aws-02")
        ]
        assert result == expected
        mock_popen.assert_called_once()

    @patch('saml2awsmulti.saml2aws_helper.load_saml2aws_config')
    @patch('getpass.getpass')
    @patch('subprocess.Popen')
    def test_run_saml2aws_list_roles_no_account_alias(self, mock_popen, mock_getpass, mock_load_config):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "testpass"

        # Mock subprocess output with no account alias
        mock_process = Mock()
        mock_process.stdout.readlines.return_value = [
            b"Account: 123456789012\n",
            b"arn:aws:iam::123456789012:role/dev\n"
        ]
        mock_process.wait.return_value = 0
        mock_popen.return_value = mock_process

        helper = Saml2AwsHelper("config_file", None, False)
        result = helper.run_saml2aws_list_roles()

        expected = [("arn:aws:iam::123456789012:role/dev", "None")]
        assert result == expected

    @patch('saml2awsmulti.saml2aws_helper.load_saml2aws_config')
    @patch('getpass.getpass')
    @patch('subprocess.Popen')
    def test_run_saml2aws_list_roles_no_roles(self, mock_popen, mock_getpass, mock_load_config):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "testpass"

        # Mock subprocess output with no roles
        mock_process = Mock()
        mock_process.stdout.readlines.return_value = [
            b"Account: aws-01 (123456789012)\n"
        ]
        mock_process.wait.return_value = 0
        mock_popen.return_value = mock_process

        helper = Saml2AwsHelper("config_file", None, False)

        with pytest.raises(ValueError, match="Failed to retrieve roles with saml2aws"):
            helper.run_saml2aws_list_roles()

    @patch('saml2awsmulti.saml2aws_helper.load_saml2aws_config')
    @patch('getpass.getpass')
    @patch('subprocess.Popen')
    def test_run_saml2aws_list_roles_parse_error(self, mock_popen, mock_getpass, mock_load_config):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "testpass"

        # Mock subprocess output with malformed account line
        mock_process = Mock()
        mock_process.stdout.readlines.return_value = [
            b"Account: malformed line\n",
            b"arn:aws:iam::123456789012:role/dev\n"
        ]
        mock_process.wait.return_value = 0
        mock_popen.return_value = mock_process

        helper = Saml2AwsHelper("config_file", None, False)

        with pytest.raises(ValueError, match="Failed to retrieve roles with saml2aws"):
            helper.run_saml2aws_list_roles()

    @patch('saml2awsmulti.saml2aws_helper.load_saml2aws_config')
    @patch('getpass.getpass')
    @patch('subprocess.Popen')
    def test_run_saml2aws_login_success(self, mock_popen, mock_getpass, mock_load_config):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "testpass"

        mock_process = Mock()
        mock_process.stdout.readlines.return_value = [b"Login successful\n"]
        mock_process.wait.return_value = 0
        mock_popen.return_value = mock_process

        helper = Saml2AwsHelper("config_file", None, False)
        result = helper.run_saml2aws_login("arn:aws:iam::123456789012:role/dev", "dev")

        assert result == 0
        mock_popen.assert_called_once()

    @patch('saml2awsmulti.saml2aws_helper.load_saml2aws_config')
    @patch('getpass.getpass')
    @patch('subprocess.Popen')
    def test_run_saml2aws_login_with_session_duration(self, mock_popen, mock_getpass, mock_load_config):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "testpass"

        mock_process = Mock()
        mock_process.stdout.readlines.return_value = [b"Login successful\n"]
        mock_process.wait.return_value = 0
        mock_popen.return_value = mock_process

        helper = Saml2AwsHelper("config_file", "7200", False)
        helper.run_saml2aws_login("arn:aws:iam::123456789012:role/dev", "dev")

        # Check that session duration was included in command
        call_args = mock_popen.call_args[0][0]
        assert "--session-duration=7200" in call_args

    @patch('saml2awsmulti.saml2aws_helper.load_saml2aws_config')
    @patch('getpass.getpass')
    @patch('subprocess.Popen')
    def test_run_saml2aws_login_with_browser_autofill(self, mock_popen, mock_getpass, mock_load_config):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "testpass"

        mock_process = Mock()
        mock_process.stdout.readlines.return_value = [b"Login successful\n"]
        mock_process.wait.return_value = 0
        mock_popen.return_value = mock_process

        helper = Saml2AwsHelper("config_file", None, True)
        helper.run_saml2aws_login("arn:aws:iam::123456789012:role/dev", "dev")

        # Check that browser autofill was included in command
        call_args = mock_popen.call_args[0][0]
        assert "--browser-autofill" in call_args

    @patch('saml2awsmulti.saml2aws_helper.load_saml2aws_config')
    @patch('getpass.getpass')
    @patch('subprocess.Popen')
    def test_run_saml2aws_login_failure(self, mock_popen, mock_getpass, mock_load_config):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "testpass"

        mock_process = Mock()
        mock_process.stdout.readlines.return_value = [b"Login failed\n"]
        mock_process.wait.return_value = 1
        mock_popen.return_value = mock_process

        helper = Saml2AwsHelper("config_file", None, False)
        result = helper.run_saml2aws_login("arn:aws:iam::123456789012:role/dev", "dev")

        assert result == 1

    @patch('saml2awsmulti.saml2aws_helper.load_saml2aws_config')
    @patch('getpass.getpass')
    @patch('subprocess.Popen')
    def test_run_saml2aws_login_command_format(self, mock_popen, mock_getpass, mock_load_config):
        mock_load_config.return_value = {"username": "testuser"}
        mock_getpass.return_value = "testpass"

        mock_process = Mock()
        mock_process.stdout.readlines.return_value = [b"Login successful\n"]
        mock_process.wait.return_value = 0
        mock_popen.return_value = mock_process

        helper = Saml2AwsHelper("config_file", "3600", True)
        helper.run_saml2aws_login("arn:aws:iam::123456789012:role/dev", "dev")

        # Verify the command format
        call_args = mock_popen.call_args[0][0]
        expected_parts = [
            "saml2aws login",
            "--role=arn:aws:iam::123456789012:role/dev",
            "-p dev",
            "--username=testuser",
            "--password=testpass",
            "--skip-prompt",
            "--session-duration=3600",
            "--browser-autofill"
        ]

        for part in expected_parts:
            assert part in call_args
