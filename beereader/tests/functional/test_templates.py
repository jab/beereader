from beereader.tests import *

class TestTemplatesController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='templates', action='index'))
        # Test response...
