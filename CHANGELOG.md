# Change Log
All notable changes to this project will be documented in this file.

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