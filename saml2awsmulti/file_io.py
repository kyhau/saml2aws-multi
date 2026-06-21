import csv
from configparser import ConfigParser
from os import makedirs
from os.path import dirname, exists


def write_csv(output_filename, data_list):
    makedirs(dirname(output_filename), exist_ok=True)
    with open(output_filename, "w") as f:
        csv_out = csv.writer(f)
        for item in data_list:
            csv_out.writerow(item)


def read_csv(filename, delimiter=","):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        for row in reader:
            if row and not row[0].startswith("#"):
                yield list(map(str.strip, row))


def read_lines_from_file(filename):
    if exists(filename):
        with open(filename) as f:
            content = f.readlines()
        return [x.strip() for x in content]
    return []


def load_saml2aws_config(filename):
    # Use ConfigParser so values containing '=' (e.g. URLs with query strings) are parsed correctly.
    cp = ConfigParser(allow_no_value=True)
    cp.read(filename)
    configs = {}
    for section in cp.sections():
        for key, value in cp.items(section):
            if value:
                configs[key] = value
    return configs


def get_aws_profiles(filename):
    cp = ConfigParser()
    cp.read(filename)
    return cp


def write_aws_profiles(filename, config):
    with open(filename, "w") as configfile:
        config.write(configfile)
