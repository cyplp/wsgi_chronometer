import time


def chronometer_filter_factory(app, global_conf, **kwargs):
    """

    """
    return ChronoFilter(app, kwargs)


class ChronoFilter(object):
    def __init__(self, app, args):
        self._app = app
        self._args = args

    def __call__(self, environ, start_response):
        begin = time.time()
        result = self._app(environ, start_response)
        end = time.time()
        # TODO factor this, use logging ?
        print environ['REQUEST_METHOD'], end - begin, environ['PATH_INFO']
        return result


