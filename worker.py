import logging
import os
import time
from configparser import ConfigParser

from App.Workers import QueueWorker

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    config = ConfigParser()
    config.read(os.path.join(os.getcwd(), 'config.ini'))

    assert config.has_option('redis', 'host'), print('Ошибка указании хоста для редис')

    debug = config.getboolean('settings', 'debug') if config.has_option('settings', 'debug') else False
    logging.basicConfig(level=logging.DEBUG if debug else logging.WARNING)

    host = config.get('redis', 'host')
    port = config.getint('redis', 'port') if config.has_option('redis', 'port') else 6379
    tag = config.get('queue', 'tag') if config.has_option('queue', 'tag') else 'default'
    logging.debug(f"Redis HOST = {host}")

    os.environ['STATUS'] = "ON"

    worker = QueueWorker(host, port, tag)
    worker.start()

    while True:
        try:
            time.sleep(3)
            continue
        except (KeyboardInterrupt, Exception):
            break
    print('Завершение программы')
    os.environ['STATUS'] = 'OFF'
    worker.join(1)
