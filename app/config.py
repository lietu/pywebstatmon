from yaml import load


class Config(object):
    """Configuration manager"""

    def __init__(self):
        """Set up our basic configuration variables"""
        self.http_port = None
        self.log_file = None
        self.monitors = {}

    def read_from_file(self, path):
        """Load configuration parameters from a file"""

        with open(path, 'r') as source:
            data = load(source)

        if "http_port" in data:
            self.http_port = data["http_port"]

        if "log_file" in data:
            self.log_file = data["log_file"]

        if "monitors" in data:
            # For monitors, make sure they've got all keys regardless of how
            # it was in config
            self.monitors = {}
            for url in data["monitors"]:
                self.monitors[url] = self._monitor_fill(data["monitors"][url])

    def override_monitor_setting(self, name, value):
        """Override a monitor setting on all monitors"""

        for url in self.monitors:
            self.monitors[url][name] = value

    def validate(self):
        """Validate that the config contents are sane"""

        # TODO: I was too lazy to write this now.

        pass

    @staticmethod
    def _monitor_fill(entry):
        """Fill in the blanks for optional settings on a monitor config"""

        if not "content" in entry:
            entry["content"] = []

        return entry
