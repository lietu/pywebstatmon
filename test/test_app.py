from unittest import TestCase
from app import Config, App


class ConfigTest(TestCase):
    """
    Tests the Config class' capability to read and validate the config.
    """

    def test_read_example(self):
        """Just try to read the example config and make sure we do it right"""

        config = Config()
        config.read_from_file('config.example.yaml')


class AppTest(TestCase):
    """
    Tests the core application logic.
    """

    def test_init_results(self):
        """Make sure _init_results does what is expected"""

        config = Config()
        config.monitors = {
            "http://test/": {},
            "http://test2/": {}
        }

        result = App._init_results(config)

        assert result["http://test/"] is None
        assert result["http://test2/"] is None
