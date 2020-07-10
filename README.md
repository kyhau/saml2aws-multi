# saml2aws-multi

[![githubactions](https://github.com/kyhau/saml2aws-multi/workflows/Build-Test/badge.svg)](https://github.com/kyhau/saml2aws-multi/actions)
[![travisci](https://travis-ci.org/kyhau/saml2aws-multi.svg?branch=master)](https://travis-ci.org/kyhau/saml2aws-multi) 
[![codecov](https://codecov.io/gh/kyhau/saml2aws-multi/branch/master/graph/badge.svg)](https://codecov.io/gh/kyhau/saml2aws-multi)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](http://en.wikipedia.org/wiki/MIT_License)

A helper script provides a easy-to-use command line interface to support login to multiple roles of different
accounts with saml2aws. 

Support Python >= 3.7

TODO Screenshot

## Build and Run

```
virtualenv env
. env/bin/activate      # (or env\Scripts\activate on Windows)
pip install -e .


# Select which profiles to get credentials
awslogin [--session-duration <session duration in seconds>] [--keyword <keyword>] [-refresh-cached-roles] [--debug]

# Example: Pre select profiles by the given keywork
awslogin -k <keyword>


# Set the selected profile as default
awslogin switch
```

## Tox Tests and Build the Wheels

```
pip install -r requirements-build.txt
tox -r
```
