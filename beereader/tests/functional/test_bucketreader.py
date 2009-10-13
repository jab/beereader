from beereader.tests import *

class TestBucketreaderController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='bucketreader', action='index'))
        # Test response...
