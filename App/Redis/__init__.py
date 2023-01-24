import redis
connection = redis.Redis(host='localhost', port=6379, db=1, socket_connect_timeout=1)
