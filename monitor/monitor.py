from time import time
from utils.log import log

# To support Python 2 and 3
try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen


class Monitor(object):
    """
    Monitor that a web page looks good.
    """

    def __init__(self, url, settings):
        self.url = url
        self.settings = settings

    def get_url(self):
        """Accessor to the URL we are working with"""

        return self.url

    def get_settings(self):
        """Accessor to the settings we are working with"""

        return self.settings

    def check(self):
        """Check our monitoring target"""

        result = False

        result_log = "{url}: {result}"

        try:
            start = time()
            contents = self._fetch_contents()
            end = time()
            elapsed = "{:.3f}".format(end - start)

            if self._check_contents(contents, self.settings):
                log.info(result_log.format(
                    url=self.url,
                    result="GOOD {} ms response time".format(elapsed)
                ))

                result = elapsed
            else:
                log.warning(result_log.format(
                    url=self.url,
                    result="BAD, Content mismatch, {} ms response time".format(
                        elapsed
                    )
                ))

        except IOError as e:
            log.error(result_log.format(
                url=self.url,
                result="BAD, Connection error: {}".format(e)
            ))

        return result

    def _fetch_contents(self):
        """Simply fetch the URL contents"""

        return urlopen(self.url).read()

    @staticmethod
    def _check_contents(contents, settings):
        """Determine if the contents match the content filters we have"""

        if settings["content"]:
            for text in settings["content"]:
                if not text in contents:
                    return False

        return True
