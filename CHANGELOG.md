# Change Log
All notable changes to this project will be documented in this file.

1.2.0 - 2025-10-18
==================
- **Modernized project structure** to match python-repo-template best practices
- **Updated Python support** to 3.10, 3.11, 3.12, and 3.13
- **Changed build system** from setuptools to poetry-core for cleaner, modern builds
- **Moved tests directory** from `saml2awsmulti/tests/` to `tests/` at repo root
- **Updated Makefile** with comprehensive targets matching template:
  - Added `setup-init` for first-time setup
  - Added `install`, `install-dev`, `install-test`, `install-all` targets
  - Renamed `test-coverage` to `test-with-coverage`
  - Renamed `yamllint` to `lint-yaml`
  - Added `lint-python` for Python linting
  - Added `format-python` for code formatting with black
  - Added `pre-commit` for running all quality checks
- **Updated GitHub workflows**:
  - Renamed `build-and-test.yml` to `ci.yml`
  - Added Snyk vulnerability scanning workflow
  - Added Python linting to CI pipeline
  - Improved CI/CD with better path filtering and concurrency controls
- **Updated dependabot.yml** to use Poetry ecosystem only (removed redundant pip)
- **Added cursor rules** (`.cursor/rules/`) for development workflow documentation
- **Added black** to dev dependencies for code formatting
- **Removed setuptools/wheel** from dev dependencies (no longer needed with poetry-core)
- **Updated README.md** with modern structure, badges, and comprehensive documentation
- **Streamlined pyproject.toml** by removing duplicate metadata and using poetry-core

1.1.1 - 2025-10-12
==================
- Migrated from `uv` to Poetry for dependency management to enable Dependabot support
- Added `make update-deps` and `make lock` targets for dependency management
- Updated build system to use Poetry while maintaining setuptools compatibility

1.1.0 - 2024-12-21
==================
- Supported new option `--browser-autofill|-b` to enable browser-autofill in saml2aws

1.0.1 - 2024-05-21
==================
- Test with Python 3.12.
- No longer test with Python 3.8 and Python 3.9.

1.0.0 - 2023-02-15
==================
- Replaced `PyInquirer` with [InquirerPy](https://github.com/kazhala/InquirerPy) - https://github.com/kyhau/saml2aws-multi/issues/20
- Updated to use and support major version updates of `flake8` and `tox`.
- Test with Python 3.11.
- No longer test with Python 3.7.

0.4.0 - 2022-01-25
==================
- Updated `awslogin chained` to support option `--from-profile|-p` for showing chained roles from the ~/.aws/config for the given profile (specified with `from-profile|-p`).

0.3.1 - 2021-10-20
==================
- Support parsing info of AWS account that does not have account alias when calling `saml2aws list-roles`.

0.3.0 - 2021-05-08
==================
- Renamed `--keyword|-k` to `--pre-select|-s`.
- Supported new option `--shortlisted|-l` to show the list of roles having profile name matching the given keyword(s).

0.2.0 - 2020-09-01
==================
- Supported new commands `chained` and `whoami`.
- Fixed loading previously selected role no longer exists.

0.1.0 - 2019-09-30
==================
- Initial version of saml2awsmulti.
