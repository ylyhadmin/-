import redis
import pickle
import time


class Queue:
    def __init__(self, db):
        self.redis = redis.Redis(host='127.0.0.1', port=6379, db=1)
        self.db = db

    def put(self, data):
        self.redis.lpush(self.db, pickle.dumps(data))

    def get(self, timeout=1):
        for i in range(timeout * 100):
            try:
                return pickle.loads(self.redis.rpop(self.db))
            except Exception:
                time.sleep(0.01)
        raise TimeoutError('获取时间超时')

    def empty(self):
        return self.redis.llen(self.db) == 0

    def len(self):
        return self.redis.llen(self.db)

    def clear(self):
        self.redis.delete(self.db)


class Stack:
    def __init__(self, db):
        self.redis = redis.Redis(host='127.0.0.1', port=6379, db=1)
        self.db = db

    def put(self, data):
        self.redis.lpush(self.db, pickle.dumps(data))

    def get(self, timeout=1):
        for i in range(timeout * 100):
            try:
                return pickle.loads(self.redis.lpop(self.db))
            except Exception:
                time.sleep(0.01)
        raise TimeoutError('获取时间超时')

    def empty(self):
        return self.redis.llen(self.db) == 0

    def len(self):
        return self.redis.llen(self.db)

    def clear(self):
        self.redis.delete(self.db)


class PriorityQueue:
    def __init__(self, db):
        self.redis = redis.Redis(host='127.0.0.1', port=6379, db=1)
        self.db = db

    def put(self, data, score):
        self.redis.zadd(self.db, {pickle.dumps(data): score, })

    def get(self, timeout=1):
        for i in range(timeout * 100):
            try:
                content = pickle.loads(self.redis.zrevrange(self.db, self.len()-1, self.len()-1)[0])
                self.redis.zremrangebyrank(self.db, 0, 0)
                return content
            except Exception as e:
                print(e)
                time.sleep(0.01)
        raise TimeoutError('获取时间超时')

    def empty(self):
        return self.redis.zcount(self.db, 0, 10000) == 0

    def len(self):
        return self.redis.zcount(self.db, 0, 10000)

    def clear(self):
        self.redis.delete(self.db)
