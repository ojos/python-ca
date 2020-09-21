from redis import ConnectionPool, StrictRedis


class Redis(object):
    _pool = None

    @classmethod
    def get(cls, host: str='localhost', port: int=6379, db: int=0) -> StrictRedis:
        if cls._pool is None:
            cls._pool = ConnectionPool(host=host, port=port, db=db)
        conn = StrictRedis(connection_pool=cls._pool)
        return conn

    @classmethod
    def close(cls):
        cls._pool.disconnect()