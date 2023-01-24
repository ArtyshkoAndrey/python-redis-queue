from App.Redis import connection
import json
import logging


class JobContract(object):
    def handle(self):
        pass

    @classmethod
    def dispatch(cls, **kwargs):
        connection.publish('jobs', json.dumps({'class': cls.__name__, 'params': kwargs}))
        logging.debug(json.dumps({'class': cls.__name__, 'params': kwargs}))
        pass
