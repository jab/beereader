from beereader.tests import *

class TestReaderController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='reader', action='index'))
        # Test response...
