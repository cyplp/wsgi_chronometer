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

def app(environ, start_response):
    """from http://www.python.org/dev/peps/pep-0333/"""
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello world!\n']


class TestChronoFilter(unittest.TestCase):
    def test__init__(self):
        """
        Test __init__.
        """

        c = ChronoFilter(app, **{})

        self.assertEquals(c._app, app)
        self.assertEquals(c._sep, '-')
        self.assertEquals(c._fields, [])

        c = ChronoFilter(app, **{'separator': '*'})

        self.assertEquals(c._app, app)
        self.assertEquals(c._sep, '*')
        self.assertEquals(c._fields, [])

        c = ChronoFilter(app, **{'fields': 'HOST'})
        self.assertEquals(c._app, app)
        self.assertEquals(c._sep, '-')
        self.assertEquals(c._fields, ['HOST'])

        c = ChronoFilter(app, **{'separator': '+', 'fields': 'HOST'})
        self.assertEquals(c._app, app)
        self.assertEquals(c._sep, '+')
        self.assertEquals(c._fields, ['HOST'])

        c = ChronoFilter(app, **{'fields': 'HOST PATH'})
        self.assertEquals(c._app, app)
        self.assertEquals(c._sep, '-')
        self.assertEquals(c._fields, ['HOST', 'PATH'])


    def test__call__(self):
        """
        Test __call__
        """
        c = ChronoFilter(app, **{})

        def fakeStartResponse(status, headers):
            return []

        # minimal environ for webob
        environ = {'REQUEST_METHOD': 'GET',
                   'PATH_INFO': '/',
                   'SERVER_PROTOCOL': 'HTTP',
                   'SERVER_NAME': 'HERE',
                   'wsgi.url_scheme': 'http',
                   'SERVER_PORT': '4343'}

        result = c(environ, fakeStartResponse)
        self.assertEquals(result, ['Hello world!\n'])

        c = ChronoFilter(app, **{'fields': 'HOST SERVER_PORT'})

        result = c(environ, fakeStartResponse)
        self.assertEquals(result, ['Hello world!\n'])
