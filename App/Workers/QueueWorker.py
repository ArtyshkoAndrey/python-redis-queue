import json
import logging
import os
import sys
import time
from threading import Thread

import redis

from App.Contracts import JobContract


class QueueWorker(Thread):
    """
        Worker для выполнения фоновых задач в потоке, На подобии Laravel.
        Использует Redis.
    """

    connection: redis.Redis
    logger: logging
    host: str
    port: int
    tag: str

    def __init__(self, host: str, port: int, tag: str) -> None:
        """
            Инициализация Worker. Подключение к Redis.
            :rtype: None
        """
        super().__init__(name='QueueWorker')
        self.logger = logging.getLogger('QueueWorker')

        self.host = host
        self.port = port
        self.tag = tag

    def run(self) -> None:
        self._connect_redis()

        # while True:
        sub = self.connection.pubsub()
        sub.subscribe(self.tag)
        for data in sub.listen():
            if os.environ['STATUS'] != 'ON':
                self.logger.warning('STOP QUEUE WORKER')
                break
            data = data.get('data')
            try:
                if data is not None:
                    data = json.loads(data)
                    module_name = f"App.Jobs.{data.get('class')}"
                    __import__(module_name)
                    class_job = getattr(sys.modules[module_name], data.get('class'))
                    if JobContract in class_job.mro():
                        job = class_job
                        job = job(**data.get('params'))
                        job.handle()
            except KeyboardInterrupt:
                logging.warning('Вызвано прерывание воркера')
                break
            except Exception:
                logging.warning('Ошибка в валидности параметров для')

    def _connect_redis(self):
        while os.environ['STATUS'] == 'ON' and self.is_redis_available() == False:

            self.logger.debug('Подключение к редис')
            self.logger.debug(f"HOST: {self.host}:{self.port}")
            try:
                self.connection = redis.Redis(host=self.host, port=self.port, db=1, socket_connect_timeout=1)
                self.connection.ping()
            except redis.exceptions.TimeoutError:
                self.logger.warning('Ошибка подключение к Redis')
                time.sleep(5)

    def is_redis_available(self):
        # ... get redis connection here, or pass it in. up to you.
        try:
            self.connection.ping()  # getting None returns None or throws an exception
        except (redis.exceptions.ConnectionError,
                redis.exceptions.BusyLoadingError,
                redis.exceptions.TimeoutError,
                AttributeError):
            return False
        self.logger.debug('Подключение к редис успешно')
        return True
