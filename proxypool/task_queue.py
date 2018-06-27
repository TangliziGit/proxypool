import redis
from multiprocessing import Queue

from .rules import (
    TASKS,
    DB_HOST, DB_PORT, DB_ID,
    DB_TASK_QUEUE_NAME, DB_RAW_IPPOOL_NAME,
    DB_SPLIT_SYMBOL,
)

class RedisProxyQueue:
    def __init__(self):
        self.rdb=redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_ID)
        self.urls=self.rdb.smembers(DB_RAW_IPPOOL_NAME)
        self.queue=Queue()
        self._put_urls()

    def get(self):
        return self.queue.get()

    def empty(self):
        return self.queue.empty()

    def _put_urls(self):
        for url in self.urls:
            self.queue.put(url)

class RedisTaskQueue:
    def __init__(self):
        self.rdb=redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_ID)

    def get(self):
        # print(self.rdb.lpop(DB_TASK_QUEUE_NAME).decode('utf-8').split(DB_SPLIT_SYMBOL))
        item_name, item_url=self.rdb.lpop(DB_TASK_QUEUE_NAME).decode('utf-8').split(DB_SPLIT_SYMBOL)
        return {"name":item_name, "url":item_url}

class TaskQueue:
    def __init__(self, read_task_items=True):
        self.queue=Queue()
        if read_task_items:
            self._put_items()

    def get(self):
        return self.queue.get()

    def put(self, item):
        raise NotImplementedError

    def empty(self):
        return self.queue.empty()

    def _put_items(self):
        for taskname, task in TASKS.items():
            for url in task["resource"]:
                self.queue.put(
                    {"name": taskname, "url":url}
                )
