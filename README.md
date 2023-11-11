# saml2aws-multi

[![githubactions](https://github.com/kyhau/saml2aws-multi/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/kyhau/saml2aws-multi/actions/workflows/build-and-test.yml)
[![codecov](https://codecov.io/gh/kyhau/saml2aws-multi/branch/main/graph/badge.svg)](https://app.codecov.io/gh/kyhau/saml2aws-multi/tree/main)
[![CodeQL](https://github.com/kyhau/saml2aws-multi/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/kyhau/saml2aws-multi/actions/workflows/codeql-analysis.yml)
[![SecretsScan](https://github.com/kyhau/saml2aws-multi/actions/workflows/secrets-scan.yml/badge.svg)](https://github.com/kyhau/saml2aws-multi/actions/workflows/secrets-scan.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](http://en.wikipedia.org/wiki/MIT_License)

This is a helper script providing an easy-to-use command line interface to support login and retrieve AWS temporary credentials for multiple roles of different accounts with [saml2aws](https://github.com/Versent/saml2aws).

![Example-RoleName](docs/Example-RoleName.png)

All notable changes to this project will be documented in [CHANGELOG](./CHANGELOG.md).

---
## Built with
- Python - support Python 3.8, 3.9, 3.10, 3.11.
- [CodeQL](https://codeql.github.com) is [enabled](.github/workflows/codeql-analysis.yml) in this repository.
- [Dependabot](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates) is [enabled](.github/dependabot.yml) for auto dependency updates.
- [Gitleaks](https://github.com/gitleaks/gitleaks) and [TruffleHog](https://github.com/trufflesecurity/trufflehog) are enabled in this GitHub Actions [workflow](.github/workflows/secrets-scan.yml) for detecting and preventing hardcoded secrets.
- [Snyk](https://github.com/snyk/actions) is enabled for vulnerability scanning and auto pull-request.

---
## Usage

```
$ awslogin --help
Usage: awslogin [OPTIONS] COMMAND [ARGS]...

  Get credentials for multiple accounts with saml2aws

Options:
  -l, --shortlisted TEXT          Show only roles with the given keyword(s);
                                  e.g. -l keyword1 -l keyword2...

  -s, --pre-select TEXT           Pre-select roles with the given keyword(s);
                                  e.g. -s keyword1 -s keyword2...

  -n, --profile-name-format [RoleName|RoleName-AccountAlias]
                                  Set the profile name format.  [default:
                                  RoleName]

  -r, --refresh-cached-roles      Re-retrieve the roles associated to the
                                  username and password you providedand save
                                  the roles into <home>/.saml2aws-
                                  multi/aws_login_roles.csv.  [default: False]

  -t, --session-duration TEXT     Set the session duration in seconds,
  -d, --debug                     Enable debug mode.  [default: False]
  --help                          Show this message and exit.

Commands:
  chained  List chained role profiles specified in ~/.aws/config
  switch   Switch default profile
  whoami   Who am I?
```

### Usage Examples

1. When you run `awslogin` the first time, the script retrieves the roles associated to the username and password you provided, then saves the roles to `<user_home>/.saml2aws-multi/aws_login_roles.csv`, such that the script does not need to call `list_roles` every time you run `awslogin`.

    For example, if you have role ARNs like:
    ```
    RoleArn, AccountAlias
    arn:aws:iam::123456789012:role/aws-01-dev, aws-01
    arn:aws:iam::123456789012:role/aws-01-tst, aws-01
    arn:aws:iam::213456789012:role/aws-02-dev, aws-02
    arn:aws:iam::313456789012:role/aws-03-dev, aws-03
    ```
    Then, the profile names will look like
    ![Example-RoleName-init](docs/Example-RoleName-init.png)

    To refresh the content of `aws_login_roles.csv`, just run

    ```
    awslogin --refresh-cached-roles
    ```

2. When you run `awslogin`, the script pre-selects the options you selected last time.

    ![Example-RoleName](docs/Example-RoleName.png)

3. Use `--pre-select` or `-s` to pre-select option by keyword(s).

    ```
    awslogin -s dev -s tst
    ```

4. Use `--shortlisted` or `-l` to show the list of roles having profile name matching the given keyword(s).

    ```
    awslogin -l dev -l tst
    ```

5. To change your `default` profile in `<user_home>/.aws/credentials`, run

    ```
    awslogin switch
    ```

6. If you have roles in different accounts with the same role names, you can use `--profile-name-format RoleName-AccountAlias`, such that the profile names will include both role name and account alias.  Alternatively, you can also change `DEFAULT_PROFILE_NAME_FORMAT` in the code to `RoleName-AccountAlias`.

    For example, if you have role ARNs like:
    ```
    RoleArn, AccountAlias
    arn:aws:iam::123456789012:role/dev, aws-01
    arn:aws:iam::123456789012:role/tst, aws-01
    arn:aws:iam::213456789012:role/dev, aws-02
    arn:aws:iam::313456789012:role/dev, aws-03
    ```
    Then, the profile names will look like
    ![Example-RoleName-AccountAlias](docs/Example-RoleName-AccountAlias.png)

---
## Build and run

1. Install [saml2aws](https://github.com/Versent/saml2aws). See also
   [install-saml2aws.sh](install-saml2aws.sh) for Linux, or
   [Install-saml2aws.ps1](Install-saml2aws.ps1) for Windows.

2. Create `saml2aws` config file (`~/.saml2aws`) by running `saml2aws configure`.

3. Build and run

```
# Create and activate a new virtual env (optional)
virtualenv env
. env/bin/activate      # (or env\Scripts\activate on Windows)

# Install and run
pip install -e .
awslogin --help
```

---
## Run Tox tests and build the wheels

```
pip install -r requirements-build.txt
tox -r
```
