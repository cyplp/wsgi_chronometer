import time
import datetime


def chronometer_filter_factory(app, global_conf, **kwargs):
    """

    """
    return ChronoFilter(app, **kwargs)


class ChronoFilter(object):
    def __init__(self, app, **kwargs):
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
        begin = time.time()
        result = self._app(environ, start_response)
        end = time.time()
        
        data = [str(datetime.datetime.now())]
        for field in self._fields:
            try:
                data.append(environ[field])
            except KeyError:
                data.append(' ')
                
        data.append(str((end- begin) * 1000))
        sep = " %s " % (self._sep)
        print sep.join(data)
        return result


