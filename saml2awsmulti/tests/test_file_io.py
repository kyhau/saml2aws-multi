from saml2awsmulti.file_io import (
    read_lines_from_file,
)


def test_read_lines_from_file():
    assert read_lines_from_file("") == []
