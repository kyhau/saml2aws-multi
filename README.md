# saml2aws-multi

[![CI](https://github.com/kyhau/saml2aws-multi/actions/workflows/ci.yml/badge.svg)](https://github.com/kyhau/saml2aws-multi/actions/workflows/ci.yml)
[![Codecov](https://codecov.io/gh/kyhau/saml2aws-multi/branch/main/graph/badge.svg)](https://codecov.io/gh/kyhau/saml2aws-multi)
[![CodeQL](https://github.com/kyhau/saml2aws-multi/workflows/CodeQL/badge.svg)](https://github.com/kyhau/saml2aws-multi/actions/workflows/codeql-analysis.yml)
[![Snyk Checks](https://github.com/kyhau/saml2aws-multi/workflows/Snyk%20Checks/badge.svg)](https://github.com/kyhau/saml2aws-multi/actions/workflows/snyk.yml)
[![Secrets Scan](https://github.com/kyhau/saml2aws-multi/workflows/Secrets%20Scan/badge.svg)](https://github.com/kyhau/saml2aws-multi/actions/workflows/secrets-scan.yml)
![Python Version](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/kyhau/saml2aws-multi)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](http://en.wikipedia.org/wiki/MIT_License)

A helper script providing an easy-to-use command line interface to login and retrieve AWS temporary credentials for multiple roles across different accounts using [saml2aws](https://github.com/Versent/saml2aws).

![Example-RoleName](docs/Example-RoleName.png)

All notable changes to this project will be documented in [CHANGELOG](./CHANGELOG.md).

**Supports Python 3.12, 3.13, 3.14**

## ✨ Features

### 🔧 Development Tools
- **[Poetry](https://python-poetry.org/)** - Modern dependency management
- **[Makefile](Makefile)** - Convenient command shortcuts for common tasks
- **[pytest](https://pytest.org/)** - Testing framework with coverage reporting
- **[black](https://black.readthedocs.io/)** - Code formatting
- **[flake8](https://flake8.pycqa.org/)** - Python code linting

### 🔐 Security & Code Quality
- **[CodeQL](https://codeql.github.com)** - Automated security analysis ([workflow](.github/workflows/codeql-analysis.yml))
- **[Secrets Scan](https://github.com/gitleaks/gitleaks)** - Gitleaks and TruffleHog for detecting hardcoded secrets ([workflow](.github/workflows/secrets-scan.yml))
- **[Snyk](https://snyk.io/)** - Vulnerability scanning ([workflow](.github/workflows/snyk.yml))
- **[Dependabot](https://docs.github.com/en/code-security/dependabot)** - Automated dependency updates ([config](.github/dependabot.yml))

### 🚀 CI/CD
- **[GitHub Actions](https://github.com/features/actions)** - Automated testing across Python 3.12-3.14
- **[Codecov](https://codecov.io/)** - Code coverage reporting
- **Stale Issue Management** - Automatically closes inactive issues

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
  -b, --browser-autofill          Enable browser-autofill.
  -d, --debug                     Enable debug mode.  [default: False]
  --help                          Show this message and exit.

Commands:
  chained  List chained role profiles specified in ~/.aws/config
  clean    Remove expired credentials from ~/.aws/credentials
  switch   Switch default profile (shows only non-expired profiles)
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

5. To remove expired credentials from `~/.aws/credentials`, run

    ```
    awslogin clean
    ```

6. To change your `default` profile in `~/.aws/credentials`, run

    ```
    awslogin switch
    ```

    `switch` automatically hides expired profiles from the list.

7. If you have roles in different accounts with the same role names, you can use `--profile-name-format RoleName-AccountAlias`, such that the profile names will include both role name and account alias.  Alternatively, you can also change `DEFAULT_PROFILE_NAME_FORMAT` in the code to `RoleName-AccountAlias`.

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
## 🚀 Installation

### Prerequisites

Before installing, ensure you have:

1. **Python 3.12+** installed
2. **[saml2aws](https://github.com/Versent/saml2aws)** installed
   - See [install-saml2aws.sh](install-saml2aws.sh) for a Linux installation script
   - For other platforms, follow the [official installation guide](https://github.com/Versent/saml2aws#install)
3. **saml2aws config file** (`~/.saml2aws`) - Run `saml2aws configure` to create

### Installation Options

Choose the installation method that best fits your use case:

#### Option 1: pipx (Recommended for end users)

[pipx](https://pipx.pypa.io/) installs the CLI in an isolated environment while making it globally available:

```bash
# Install pipx if needed
pip install pipx

# Install saml2awsmulti
pipx install .

# Run from anywhere
awslogin --help
awslogin
```

#### Option 2: pip (Simple installation)

```bash
# Install directly with pip
pip install .

# Run the CLI
awslogin --help
awslogin
```

#### Option 3: Development Installation

For contributing or development work, see [CONTRIBUTING.md](CONTRIBUTING.md).

## 🤝 Contributing

Contributions are welcome! Please see:
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - Community standards

## 🔒 Security

For security issues, please see [SECURITY.md](SECURITY.md) for our security policy and reporting guidelines.
