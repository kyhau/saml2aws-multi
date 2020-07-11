# saml2aws-multi

[![githubactions](https://github.com/kyhau/saml2aws-multi/workflows/Build-Test/badge.svg)](https://github.com/kyhau/saml2aws-multi/actions)
[![travisci](https://travis-ci.org/kyhau/saml2aws-multi.svg?branch=master)](https://travis-ci.org/kyhau/saml2aws-multi) 
[![codecov](https://codecov.io/gh/kyhau/saml2aws-multi/branch/master/graph/badge.svg)](https://codecov.io/gh/kyhau/saml2aws-multi)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](http://en.wikipedia.org/wiki/MIT_License)

A helper script provides an easy-to-use command line interface to support login and retrieve AWS temporary
credentials for multiple roles of different accounts with [saml2aws](https://github.com/Versent/saml2aws). 

![Example-RoleName](assets/Example-RoleName.png)

Support Python >= 3.7

## Usage

```
$ awslogin --help
Usage: awslogin [OPTIONS] COMMAND [ARGS]...

  Get credentials for multiple accounts with saml2aws

Options:
  -k, --keyword TEXT              Pre-select roles with the given keyword(s)
  -f, --profile-name-format [RoleName|RoleName-AccountAlias]
                                  Profile name format  [default: RoleName]
  -r, --refresh-cached-roles      [default: False]
  -t, --session-duration TEXT     Session duration in seconds
  -d, --debug                     [default: False]
  --help                          Show this message and exit.

Commands:
  switch  Switch default profile

```

### Usage Examples

1. When you run `awslogin` the first time, the script retrieves the roles associated to the username and password
you provided, then saves the roles to `<user_home>/.saml2aws-multi/aws_login_roles.csv`, such that the
script does not need to call `list_roles` every time you run `awslogin`.

    For example, if you have role ARNs like:
    ```
    RoleArn, AccountAlias
    arn:aws:iam::123456789012:role/aws-01-dev, aws-01
    arn:aws:iam::123456789012:role/aws-01-tst, aws-01
    arn:aws:iam::213456789012:role/aws-02-dev, aws-02
    arn:aws:iam::313456789012:role/aws-03-dev, aws-03
    ```
    Then, the profile names will look like
    ![Example-RoleName-init](assets/Example-RoleName-init.png)

    To refresh the content of `aws_login_roles.csv`, just run

    ```
    awslogin --refresh-cached-roles
    ```

2. When you run `awslogin`, the script pre-selects the options you selected last time.

    ![Example-RoleName](assets/Example-RoleName.png)
    To refresh the content of `aws_login_roles.csv`, just run

3. Use `--keyword` or `-k` to pre-select option by keyword(s).

    ```
    awslogin -k dev -k tst
    ```

4. To change your `default` profile in `<user_home>/.aws/credentials`, run

    ```
    awslogin switch
    ```

5. If you have roles in different accounts with the same role names, you can use 
`--profile-name-format RoleName-AccountAlias`, such that the profile names will include both role name and account
alias.  Alternatively, you can also change `DEFAULT_PROFILE_NAME_FORMAT` in the code to `RoleName-AccountAlias`.

    For example, if you have role ARNs like:
    ```
    RoleArn, AccountAlias
    arn:aws:iam::123456789012:role/dev, aws-01
    arn:aws:iam::123456789012:role/tst, aws-01
    arn:aws:iam::213456789012:role/dev, aws-02
    arn:aws:iam::313456789012:role/dev, aws-03
    ```
    Then, the profile names will look like
    ![Example-RoleName-AccountAlias](assets/Example-RoleName-AccountAlias.png)


## Build and Run

```
virtualenv env
. env/bin/activate      # (or env\Scripts\activate on Windows)
pip install -e .
awslogin --help
```

## Tox Tests and Build the Wheels

```
pip install -r requirements-build.txt
tox -r
```
