from time import time, sleep
from threading import Thread
from .config import Config
from monitor import Monitor
from web.server import start as start_frontend
from utils.log import log, set_log_file, enable as enable_log


class App(object):
    """
    Main application logic.

    Should stay fairly thin, relays info between components.
    """

    def __init__(self, config='config.yaml'):
        self.config = Config()
        self.config.read_from_file(config)
        self.config.validate()

        self.results = {}
        self.monitors = []
        self.frontend = None
        self.thread = None

    def start(self, args):
        """Start up all of the application components"""

        enable_log()

        # Make sure the results have some data in it before the web requests
        # come in
        self.results = App._init_results(self.config)

        if args.poll_seconds:
            self.config.override_monitor_setting(
                'poll_seconds',
                args.poll_seconds
            )

        if self.config.log_file:
            set_log_file(self.config.log_file)
            log.debug("Opening log file {}".format(self.config.log_file))

        self._start_monitoring()

        if self.config.http_port:
            log.info("Starting web frontend on port {}".format(
                self.config.http_port
            ))
            self._start_frontend()

    def get_config(self):
        """Convenient way to get the application config"""

        return self.config

    def get_results(self):
        """Convenient way to get the latest monitor results"""

        return self.results

    def _start_frontend(self):
        """Start the web frontend"""

        self.frontend = start_frontend(self)

    def _start_monitoring(self):
        """Start monitoring the URLs"""

        for url in self.config.monitors:
            log.info("Monitoring {} every {} seconds".format(
                url,
                self.config.monitors[url]["poll_seconds"]
            ))
            self.monitors.append({
                "monitor": Monitor(url, self.config.monitors[url]),
                "nextRun": time()
            })

        def _loop():
            """Monitoring loop"""

            while True:
                now = time()

                for item in self.monitors:
                    # Is it time to run this monitor yet?
                    if item["nextRun"] < now:
                        # Run it
                        monitor = item["monitor"]
                        url = monitor.get_url()
                        result = monitor.check()

                        # Update results
                        self.results[url] = result

                        # Update next run time
                        settings = monitor.get_settings()
                        item["nextRun"] = time() + float(
                            settings["poll_seconds"])

                # Wait a while to not eat all CPU
                sleep(1)

        self.thread = Thread(target=_loop)

        # For some reason this is needed for the main process to catch
        # CTRL+C properly
        self.thread.daemon = True

        self.thread.start()

    @staticmethod
    def _init_results(config):
        """Initialize clean "results" for monitors"""

        results = {}
        for url in config.monitors:
            results[url] = None

        return results
