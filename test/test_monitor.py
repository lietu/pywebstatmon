from mock import Mock
from unittest import TestCase
from monitor import Monitor


class MonitorTest(TestCase):
    """Make sure the Monitor class seems sane"""

    def test_check_contents(self):
        """Confirm that _check_contents does it's job"""

        doc = """
        This is a webpage, trust me. See, here's an element: <h1>
        Keyword.
        Key phrase.

        The End.
        """

        settings = {
            "content": ["Keyword", "Key phrase"]
        }

        result = Monitor._check_contents(doc, settings)
        assert result is True

    def test_ioerror(self):
        """Confirm correct behavior on network error"""

        monitor = Monitor('http://fake', {})
        monitor._fetch_contents = Mock(side_effect=IOError)
        result = monitor.check()

        assert result is False

    def test_invalid_content(self):
        """Confirm correct behavior on invalid content"""

        monitor = Monitor('http://fake', {})
        monitor._fetch_contents = Mock(return_value="Some fake content")
        monitor._check_contents = Mock(return_value=False)
        result = monitor.check()

        assert result is False

    def test_good_content(self):
        """Confirm that everything works right if the content is good"""

        monitor = Monitor('http://fake', {"content":["fake"]})
        monitor._fetch_contents = Mock(return_value="Some fake content")
        result = monitor.check()

        assert result is not False
