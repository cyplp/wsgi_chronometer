import unittest

from wsgi_chronometer import chronometer_filter_factory
from wsgi_chronometer import ChronoFilter

class TestFactory(unittest.TestCase):
    """
    """
    def testchronometer_filter_factory(self):
        """
        Test chronometer_filter_factory.
        """
        cf = chronometer_filter_factory('a', 'foo', foo='baz')
        self.assertTrue(isinstance(cf, ChronoFilter))
