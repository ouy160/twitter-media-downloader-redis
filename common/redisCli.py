import redis

pool = redis.ConnectionPool(host='localhost', port=6379, password=123456, decode_responses=True, max_connections=20)


def getConnection():
    return redis.Redis(connection_pool=pool)
