from setuptools import find_packages, setup

__title__ = "saml2awsmulti"
__version__ = "0.2.0"
__author__ = "Kay Hau"
__email__ = "virtualda@gmail.com"
__uri__ = "https://github.com/kyhau/ssllabs-scan"
__summary__ = "A helper script using saml2aws to login and retrieve AWS temporary credentials for multiple roles in different accounts."

__requirements__ = [
    "click~=7.1",
    "PyInquirer~=1.0",
]

__entry_points__ = {
    "console_scripts": [
        "awslogin = saml2awsmulti.aws_login:main_cli",
    ]
}

CLASSIFIERS = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3 :: Only",
]

setup(
    author=__author__,
    author_email=__email__,
    classifiers=CLASSIFIERS,
    data_files=[
        ("", ["ReleaseNotes.md"]),
    ],
    description=__summary__,
    entry_points=__entry_points__,
    install_requires=__requirements__,
    name=__title__,
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.6",
    url=__uri__,
    version=__version__,
    zip_safe=False,
)
