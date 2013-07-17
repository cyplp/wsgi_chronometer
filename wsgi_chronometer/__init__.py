import time
import datetime

from webob import Request

def chronometer_filter_factory(app, global_conf, **kwargs):
    """
    Factory for pasteDeploy.

    app is a wsgi app,
    global_conf is a dictionnary containing __file__ and here,
    kwargs are args in the parameters passed in the pastedeploy file conf.

    return a ChronoFilter.
    """

    return ChronoFilter(app, **kwargs)


class ChronoFilter(object):
    """
    Wsgi Middleware for mesuring time execution (and display other things).
    """
    def __init__(self, app, **kwargs):
        """
        Constructor.

        app wsgi to chronometer,
        kwargs : conf for ChronoFilter :
          - separator : string for separate fields in display (default: '-'),
          - fields list of fields to display
          .. TODO list fields.
        """
        self._app = app

        if 'separator' in kwargs:
            self._sep = kwargs['separator']
        else:
            self._separator = '-'

        if 'fields' in kwargs:
            self._fields = kwargs['fields'].split()
        else:
            self._fields = []

    def __call__(self, environ, start_response):
        """
        Call of the wsgi app.
        """
        begin = time.time()

        req = Request(environ)
        resp = req.get_response(self._app)

        result = resp(environ, start_response)

        end = time.time()

        choice = {
            'SERVER_SOFTWARE': None, # 'waitress'
            'SCRIPT_NAME': req.script_name,
            'REQUEST_METHOD': req.method,
            'PATH_INFO': req.path_info,
            'SERVER_PROTOCOL': req.http_version,
            'QUERY_STRING': req.query_string,
            'HTTP_USER_AGENT': req.user_agent,
            'SERVER_NAME': req.server_name,
            'REMOTE_ADDR': req.remote_addr,
            'wsgi.url_scheme': req.scheme,
            'SERVER_PORT': req.server_port,

            'HTTP_HOST': req.host,
#            'wsgi.multithread': True, # TODO
            'HTTP_ACCEPT': str(req.accept),
#            'wsgi.version': (1, 0),
#            'wsgi.run_once': False,

#            'wsgi.multiprocess': False,
#            'webob._parsed_cookies': ({}, '')
            'STATUS': resp.status,
            'STATUS_CODE': resp.status_code,
            'DATETIME': str(datetime.datetime.now()),
            'TIME': "%.02fms" % ((end- begin) * 1000),
            }


        data = []
        for field in self._fields:
            try:
                data.append(choice[field])
            except KeyError:
                data.append(' ')
        sep = " %s " % (self._sep)
        print sep.join(data)
        return result


""" {'webob._parsed_query_vars': (GET([]), ''),
'SERVER_SOFTWARE': 'waitress',
'SCRIPT_NAME': '',
'REQUEST_METHOD': 'GET',
'PATH_INFO': '/',
'SERVER_PROTOCOL': 'HTTP/1.1',
'QUERY_STRING': '',
'HTTP_USER_AGENT':
'curl/7.21.6 (x86_64-pc-linux-gnu) libcurl/7.21.6 OpenSSL/1.0.0e zlib/1.2.3.4 libidn/1.22 librtmp/2.3',
'SERVER_NAME': 'localhost',
'REMOTE_ADDR': '127.0.0.1',
'wsgi.url_scheme': 'http',
'SERVER_PORT': '6543',
'wsgi.input': <_io.BytesIO object at 0x2153770>,
'HTTP_HOST': '0.0.0.0:6543',
'wsgi.multithread': True,
'HTTP_ACCEPT': '*/*',
'wsgi.version': (1, 0),
'wsgi.run_once': False,
'wsgi.errors': <open file '<stderr>', mode 'w' at 0x7fd726114270>,
'wsgi.multiprocess': False,
'wsgi.file_wrapper': <class 'waitress.buffers.ReadOnlyFileBasedBuffer'>,
'webob._parsed_cookies': ({}, '')}"""
