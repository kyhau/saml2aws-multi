import getpass
import logging
import subprocess

from saml2awsmulti.file_io import load_saml2aws_config


class Saml2AwsHelper:
    def __init__(self, configfile, session_duration, browser_autofill):
        self._configfile = configfile
        self._session_duration = session_duration
        self._browser_autofill = browser_autofill
        self._uname = None
        self._upass = None

    def get_credentials(self):
        if self._uname is None or self._upass is None:
            configs = load_saml2aws_config(filename=self._configfile)

            self._uname = configs.get("username")
            if self._uname is None:
                self._uname = input("Username: ")
            else:
                logging.info(f"Username: {self._uname}")

            self._upass = getpass.getpass("Password: ")

        return self._uname, self._upass

    def run_saml2aws_list_roles(self):
        """Return List of (role_arn, account_name)"""
        roles = []
        accounts_dict = {}
        uname, upass = self.get_credentials()

        cmd = f"saml2aws list-roles --username={uname} --password={upass} --skip-prompt"

        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        for line in p.stdout.readlines():
            line = line.decode("utf-8").rstrip("\r|\n")
            logging.debug(line)
            if line.startswith("Account:"):
                try:
                    if "(" in line:
                        # Account: ALIAS (ACCOUNT_NUMBER)
                        acc_name, acc_id = line.replace("(", "").replace(")", "").split(" ")[1:]
                    else:
                        # Account: ACCOUNT_NUMBER
                        acc_name, acc_id = "None", line.split(" ")[1]

                    accounts_dict[acc_id] = acc_name
                except Exception as e:
                    logging.error(e)
                    logging.error(line)
            elif line.startswith("arn:"):
                acc_id = line.split(":")[4]
                roles.append((line, accounts_dict[acc_id]))
        retval = p.wait()

        logging.debug(f"Response Code: {retval}")
        if not roles:
            raise ValueError("Failed to retrieve roles with saml2aws.")
        return roles

    def run_saml2aws_login(self, role_arn, profile_name):
        logging.info(f"Adding {profile_name}...")

        uname, upass = self.get_credentials()
        cmd = (
            f"saml2aws login --role={role_arn} -p {profile_name} "
            f"--username={uname} --password={upass} --skip-prompt"
        )
        if self._session_duration:
            cmd = f"{cmd} --session-duration={self._session_duration}"

        if self._browser_autofill:
            cmd = f"{cmd} --browser-autofill"

        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            logging.debug(line.decode("utf-8").rstrip("\r|\n"))
        retval = p.wait()

        logging.info(f"Response Code: {retval}")
        return retval
