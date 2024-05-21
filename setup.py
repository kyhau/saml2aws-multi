from setuptools import find_packages, setup

__title__ = "saml2awsmulti"
__version__ = "1.0.0"
__author__ = "kyhau"
__email__ = "virtualda+github@gmail.com"
__uri__ = "https://github.com/kyhau/saml2aws-multi"
__summary__ = "A helper script using saml2aws to login and retrieve AWS temporary credentials for multiple roles in different accounts."

__requirements__ = [
    "boto3~=1.34",
    "click~=8.1",
    "InquirerPy~=0.3",
]

__entry_points__ = {
    "console_scripts": [
        "awslogin = saml2awsmulti.aws_login:main_cli",
    ]
}

CLASSIFIERS = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3 :: Only",
]

setup(
    author=__author__,
    author_email=__email__,
    classifiers=CLASSIFIERS,
    data_files=[
        ("", ["CHANGELOG.md"]),
    ],
    description=__summary__,
    entry_points=__entry_points__,
    install_requires=__requirements__,
    name=__title__,
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.10",
    url=__uri__,
    version=__version__,
    zip_safe=False,
)
