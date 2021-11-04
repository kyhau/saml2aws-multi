from saml2awsmulti.aws_login import (
    create_profile_name_from_role_arn,
)


def test_create_profile_name_from_role_arn():
    role_arn = "arn:aws:iam::123456789012:role/dev"
    account_alias = "aws-01"

    assert "dev" == create_profile_name_from_role_arn(
        role_arn, account_alias, "RoleName"
    )
    assert "dev-aws-01" == create_profile_name_from_role_arn(
        role_arn, account_alias, "RoleName-AccountAlias"
    )
