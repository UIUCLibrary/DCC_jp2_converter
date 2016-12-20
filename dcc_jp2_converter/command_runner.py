import subprocess
import logging

logger = logging.getLogger(__name__)


class CommandRunner:
    stderr = None
    stdout = None

    def run(self, command: list):
        logger.debug("Running command \"{}\"".format(" ".join(command)))
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = p.communicate()
        self.stderr = stderr.strip()
        self.stdout = stdout.strip()
        if p.returncode != 0:
            raise RuntimeError("Command {} returned error {}".format(command, p.returncode))

    def get_output(self)->(str, str):
        """

        Returns:
            Tuple: standard out, standard error

        """
        return self.stdout, self.stderr
