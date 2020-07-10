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

### Linux
```
virtualenv env
. env/bin/activate
pip install -e .
awslogin sample/SampleServerList.txt
```

### Windows
```
virtualenv env
env\Scripts\activate
pip install -e .
awslogin sample\SampleServerList.txt
```

## Tox Tests and Build the Wheels

```
pip install -r requirements-build.txt
tox -r
```
