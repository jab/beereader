from beereader.tests import *

class TestBucketfeederController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='bucketfeeder', action='index'))
        # Test response...
