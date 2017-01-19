"""Used for running and logging commands."""

import logging
import subprocess
from typing import Tuple

logger = logging.getLogger("dcc_jp2_converter")


class CommandRunner:
    """Used for executing commands."""

    stderr = None
    stdout = None

    def run(self, command: list):
        """
        Execute command.

        Args:
            command: Command with arguments in a list format

        """
        logger.debug("Running command \"{}\"".format(" ".join(command)))
        p = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True)
        stdout, stderr = p.communicate()
        self.stderr = stderr.strip()
        self.stdout = stdout.strip()
        if p.returncode != 0:
            raise RuntimeError(
                "Command {} returned error {}".format(command, p.returncode))

    def get_output(self) -> Tuple[str, str]:
        """
        Get the information written to standard out and standard error.

        Returns:
            Tuple: standard out, standard error

        """
        return str(self.stdout), str(self.stderr)
