from unittest.mock import patch

import pytest

from saml2awsmulti.selector import prompt_profile_selection, prompt_roles_selection


class TestPromptProfileSelection:
    @patch("saml2awsmulti.selector.inquirer")
    def test_prompt_profile_selection_success(self, mock_inquirer):
        mock_inquirer.select.return_value.execute.return_value = "dev"
        options = ["dev", "test", "prod"]

        result = prompt_profile_selection(options)

        assert result == "dev"
        mock_inquirer.select.assert_called_once_with(
            message="Please choose the profile",
            choices=options,
            default=None,
        )

    def test_prompt_profile_selection_empty_options(self):
        with pytest.raises(ValueError, match="No profiles retrieved for selection"):
            prompt_profile_selection([])

    def test_prompt_profile_selection_none_options(self):
        with pytest.raises(ValueError, match="No profiles retrieved for selection"):
            prompt_profile_selection(None)

    @patch("saml2awsmulti.selector.inquirer")
    def test_prompt_profile_selection_single_option(self, mock_inquirer):
        mock_inquirer.select.return_value.execute.return_value = "dev"
        options = ["dev"]

        result = prompt_profile_selection(options)

        assert result == "dev"
        mock_inquirer.select.assert_called_once()

    @patch("saml2awsmulti.selector.inquirer")
    def test_prompt_profile_selection_cancel(self, mock_inquirer):
        mock_inquirer.select.return_value.execute.return_value = None
        options = ["dev", "test", "prod"]

        result = prompt_profile_selection(options)

        assert result is None


class TestPromptRolesSelection:
    @patch("saml2awsmulti.selector.inquirer")
    def test_prompt_roles_selection_success(self, mock_inquirer):
        mock_inquirer.checkbox.return_value.execute.return_value = ["dev", "test"]
        options = ["dev", "test", "prod"]
        last_selected = ["dev"]

        result = prompt_roles_selection(options, last_selected)

        assert result == ["dev", "test"]
        mock_inquirer.checkbox.assert_called_once()

    @patch("saml2awsmulti.selector.inquirer")
    def test_prompt_roles_selection_with_choices(self, mock_inquirer):
        mock_inquirer.checkbox.return_value.execute.return_value = ["dev"]
        options = ["dev", "test", "prod"]
        last_selected = ["dev"]

        prompt_roles_selection(options, last_selected)

        # Verify that choices were created correctly
        call_args = mock_inquirer.checkbox.call_args
        choices = call_args[1]["choices"]

        # Check that choices have correct enabled state
        assert len(choices) == 3
        # The first choice (dev) should be enabled since it's in last_selected
        assert choices[0].enabled is True
        # The other choices should be disabled
        assert choices[1].enabled is False
        assert choices[2].enabled is False

    @patch("saml2awsmulti.selector.inquirer")
    def test_prompt_roles_selection_no_last_selected(self, mock_inquirer):
        mock_inquirer.checkbox.return_value.execute.return_value = ["test"]
        options = ["dev", "test", "prod"]
        last_selected = []

        result = prompt_roles_selection(options, last_selected)

        assert result == ["test"]

        # Verify that all choices are disabled
        call_args = mock_inquirer.checkbox.call_args
        choices = call_args[1]["choices"]

        for choice in choices:
            assert choice.enabled is False

    @patch("saml2awsmulti.selector.inquirer")
    def test_prompt_roles_selection_multiple_last_selected(self, mock_inquirer):
        mock_inquirer.checkbox.return_value.execute.return_value = ["dev", "prod"]
        options = ["dev", "test", "prod"]
        last_selected = ["dev", "prod"]

        result = prompt_roles_selection(options, last_selected)

        assert result == ["dev", "prod"]

        # Verify that correct choices are enabled
        call_args = mock_inquirer.checkbox.call_args
        choices = call_args[1]["choices"]

        assert choices[0].enabled is True  # dev
        assert choices[1].enabled is False  # test
        assert choices[2].enabled is True  # prod

    def test_prompt_roles_selection_empty_options(self):
        with pytest.raises(ValueError, match="No roles retrieved for selection"):
            prompt_roles_selection([], [])

    def test_prompt_roles_selection_none_options(self):
        with pytest.raises(ValueError, match="No roles retrieved for selection"):
            prompt_roles_selection(None, [])

    @patch("saml2awsmulti.selector.inquirer")
    def test_prompt_roles_selection_cancel(self, mock_inquirer):
        mock_inquirer.checkbox.return_value.execute.return_value = []
        options = ["dev", "test", "prod"]
        last_selected = ["dev"]

        result = prompt_roles_selection(options, last_selected)

        assert result == []

    @patch("saml2awsmulti.selector.inquirer")
    def test_prompt_roles_selection_transformer(self, mock_inquirer):
        mock_inquirer.checkbox.return_value.execute.return_value = ["dev", "test"]
        options = ["dev", "test", "prod"]
        last_selected = []

        prompt_roles_selection(options, last_selected)

        # Verify that transformer function is set
        call_args = mock_inquirer.checkbox.call_args
        transformer = call_args[1]["transformer"]

        # Test the transformer function
        result = transformer(["dev", "test"])
        assert result == "2 role(s) selected"

        result = transformer(["dev"])
        assert result == "1 role(s) selected"

        result = transformer([])
        assert result == "0 role(s) selected"

    @patch("saml2awsmulti.selector.inquirer")
    def test_prompt_roles_selection_cycle_enabled(self, mock_inquirer):
        mock_inquirer.checkbox.return_value.execute.return_value = ["dev"]
        options = ["dev", "test", "prod"]
        last_selected = []

        prompt_roles_selection(options, last_selected)

        # Verify that cycle is enabled
        call_args = mock_inquirer.checkbox.call_args
        assert call_args[1]["cycle"] is True

    @patch("saml2awsmulti.selector.inquirer")
    def test_prompt_roles_selection_message(self, mock_inquirer):
        mock_inquirer.checkbox.return_value.execute.return_value = ["dev"]
        options = ["dev", "test", "prod"]
        last_selected = []

        prompt_roles_selection(options, last_selected)

        # Verify the message
        call_args = mock_inquirer.checkbox.call_args
        assert call_args[1]["message"] == "Please choose the role"
