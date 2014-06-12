from unittest import TestCase
from pywebstatmon import _parse_args


class StartupTest(TestCase):
    """
    Tests the tool's startup script.

    Mostly pointless to test ArgParse, it's fairly sure to work right, but it's
    nice to be safe and know the return values don't change, and I used this to
    confirm that the nosetests stuff works right. ;)
    """

    def test_help(self):
        """Just make sure that --help seems to work"""

        try:
            _parse_args(['--help'])
        except SystemExit:
            # TODO: Would be nice to validate that some usage info was shown
            assert True

    def test_no_args(self):
        """Make sure no arguments means no global override for poll_seconds"""

        result = _parse_args()

        assert result.poll_seconds is None

    def test_poll_seconds(self):
        """Make sure --poll_seconds=X works"""

        result = _parse_args(['--poll_seconds=60'])

        assert result.poll_seconds == 60
