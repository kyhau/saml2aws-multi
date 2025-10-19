import os
import tempfile
from configparser import ConfigParser

from saml2awsmulti.file_io import (
    get_aws_profiles,
    load_saml2aws_config,
    read_csv,
    read_lines_from_file,
    write_aws_profiles,
    write_csv,
)


class TestReadLinesFromFile:
    def test_read_lines_from_file_nonexistent(self):
        result = read_lines_from_file("nonexistent_file.txt")
        assert result == []

    def test_read_lines_from_file_empty_string(self):
        result = read_lines_from_file("")
        assert result == []

    def test_read_lines_from_file_existing(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("line1\nline2\nline3\n")
            temp_file = f.name

        try:
            result = read_lines_from_file(temp_file)
            assert result == ["line1", "line2", "line3"]
        finally:
            os.unlink(temp_file)

    def test_read_lines_from_file_with_whitespace(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("  line1  \n  line2  \n  line3  \n")
            temp_file = f.name

        try:
            result = read_lines_from_file(temp_file)
            assert result == ["line1", "line2", "line3"]
        finally:
            os.unlink(temp_file)

    def test_read_lines_from_file_empty_lines(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("line1\n\nline2\n\n")
            temp_file = f.name

        try:
            result = read_lines_from_file(temp_file)
            assert result == ["line1", "", "line2", ""]
        finally:
            os.unlink(temp_file)


class TestWriteCsv:
    def test_write_csv_simple(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            temp_file = f.name

        try:
            data = [["col1", "col2"], ["val1", "val2"]]
            write_csv(temp_file, data)

            with open(temp_file, "r") as f:
                content = f.read()
                assert "col1,col2" in content
                assert "val1,val2" in content
        finally:
            os.unlink(temp_file)

    def test_write_csv_with_directories(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = os.path.join(temp_dir, "subdir", "test.csv")
            data = [["col1", "col2"], ["val1", "val2"]]

            write_csv(csv_file, data)

            assert os.path.exists(csv_file)
            with open(csv_file, "r") as f:
                content = f.read()
                assert "col1,col2" in content

    def test_write_csv_empty_data(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            temp_file = f.name

        try:
            write_csv(temp_file, [])

            with open(temp_file, "r") as f:
                content = f.read()
                assert content == ""
        finally:
            os.unlink(temp_file)


class TestReadCsv:
    def test_read_csv_simple(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("col1,col2\nval1,val2\nval3,val4\n")
            temp_file = f.name

        try:
            result = list(read_csv(temp_file))
            expected = [["col1", "col2"], ["val1", "val2"], ["val3", "val4"]]
            assert result == expected
        finally:
            os.unlink(temp_file)

    def test_read_csv_with_whitespace(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(" col1 , col2 \n val1 , val2 \n")
            temp_file = f.name

        try:
            result = list(read_csv(temp_file))
            expected = [["col1", "col2"], ["val1", "val2"]]
            assert result == expected
        finally:
            os.unlink(temp_file)

    def test_read_csv_with_comments(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("# This is a comment\ncol1,col2\n# Another comment\nval1,val2\n")
            temp_file = f.name

        try:
            result = list(read_csv(temp_file))
            expected = [["col1", "col2"], ["val1", "val2"]]
            assert result == expected
        finally:
            os.unlink(temp_file)

    def test_read_csv_with_empty_lines(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("col1,col2\n\nval1,val2\n\n")
            temp_file = f.name

        try:
            result = list(read_csv(temp_file))
            expected = [["col1", "col2"], ["val1", "val2"]]
            assert result == expected
        finally:
            os.unlink(temp_file)

    def test_read_csv_custom_delimiter(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("col1|col2\nval1|val2\n")
            temp_file = f.name

        try:
            result = list(read_csv(temp_file, delimiter="|"))
            expected = [["col1", "col2"], ["val1", "val2"]]
            assert result == expected
        finally:
            os.unlink(temp_file)


class TestLoadSaml2awsConfig:
    def test_load_saml2aws_config_simple(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("username=testuser\npassword=testpass\nurl=https://example.com\n")
            temp_file = f.name

        try:
            result = load_saml2aws_config(temp_file)
            expected = {
                "username": "testuser",
                "password": "testpass",
                "url": "https://example.com",
            }
            assert result == expected
        finally:
            os.unlink(temp_file)

    def test_load_saml2aws_config_with_whitespace(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(" username = testuser \n password = testpass \n")
            temp_file = f.name

        try:
            result = load_saml2aws_config(temp_file)
            expected = {"username": "testuser", "password": "testpass"}
            assert result == expected
        finally:
            os.unlink(temp_file)

    def test_load_saml2aws_config_empty_values(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("username=testuser\npassword=\nurl=https://example.com\n")
            temp_file = f.name

        try:
            result = load_saml2aws_config(temp_file)
            expected = {"username": "testuser", "url": "https://example.com"}
            assert result == expected
        finally:
            os.unlink(temp_file)

    def test_load_saml2aws_config_no_equals(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("username=testuser\ninvalid_line\nurl=https://example.com\n")
            temp_file = f.name

        try:
            result = load_saml2aws_config(temp_file)
            expected = {"username": "testuser", "url": "https://example.com"}
            assert result == expected
        finally:
            os.unlink(temp_file)


class TestGetAwsProfiles:
    def test_get_aws_profiles_simple(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(
                "[default]\naws_access_key_id = test_key\naws_secret_access_key = test_secret\n"
            )
            temp_file = f.name

        try:
            result = get_aws_profiles(temp_file)
            assert isinstance(result, ConfigParser)
            assert "default" in result.sections()
            assert result["default"]["aws_access_key_id"] == "test_key"
        finally:
            os.unlink(temp_file)

    def test_get_aws_profiles_multiple_sections(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(
                "[default]\naws_access_key_id = test_key\n\n"
                "[profile dev]\naws_access_key_id = dev_key\n"
            )
            temp_file = f.name

        try:
            result = get_aws_profiles(temp_file)
            assert "default" in result.sections()
            assert "profile dev" in result.sections()
            assert result["default"]["aws_access_key_id"] == "test_key"
            assert result["profile dev"]["aws_access_key_id"] == "dev_key"
        finally:
            os.unlink(temp_file)

    def test_get_aws_profiles_nonexistent_file(self):
        result = get_aws_profiles("nonexistent_file.ini")
        assert isinstance(result, ConfigParser)
        assert len(result.sections()) == 0


class TestWriteAwsProfiles:
    def test_write_aws_profiles_simple(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            temp_file = f.name

        try:
            config = ConfigParser()
            config["default"] = {
                "aws_access_key_id": "test_key",
                "aws_secret_access_key": "test_secret",
            }

            write_aws_profiles(temp_file, config)

            with open(temp_file, "r") as f:
                content = f.read()
                assert "[default]" in content
                assert "aws_access_key_id = test_key" in content
                assert "aws_secret_access_key = test_secret" in content
        finally:
            os.unlink(temp_file)

    def test_write_aws_profiles_multiple_sections(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            temp_file = f.name

        try:
            config = ConfigParser()
            config["default"] = {"aws_access_key_id": "test_key"}
            config["profile dev"] = {"aws_access_key_id": "dev_key"}

            write_aws_profiles(temp_file, config)

            with open(temp_file, "r") as f:
                content = f.read()
                assert "[default]" in content
                assert "[profile dev]" in content
                assert "aws_access_key_id = test_key" in content
                assert "aws_access_key_id = dev_key" in content
        finally:
            os.unlink(temp_file)

    def test_write_aws_profiles_empty_config(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            temp_file = f.name

        try:
            config = ConfigParser()
            write_aws_profiles(temp_file, config)

            with open(temp_file, "r") as f:
                content = f.read()
                assert content == ""
        finally:
            os.unlink(temp_file)
