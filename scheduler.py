from multiprocessing import Process
from queue import PriorityQueue
import time

# from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
import redis

# from proxypool.spiders.__init__ import all_spiders
from proxypool.logger import Logger
from proxypool.rules import (
    TASKS,
    DB_HOST, DB_PORT, DB_ID,
    DB_TASK_QUEUE_NAME, DB_RAW_IPPOOL_NAME, DB_IPPOOL_NAME,
    DB_SPLIT_SYMBOL,
)

class Task_dict:
    def __init__(self, taskname, task, start_time):
        self.taskname=taskname
        self.task=task
        self.start_time=start_time

    def __lt__(self, other):
        return self.start_time<other.start_time

class Scheduler:
    logger=Logger()
    def __init__(self):
        self.logger=Logger()
        self.que=PriorityQueue()
        self.rdb=redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_ID)
        self.pipe=self.rdb.pipeline(transaction=True)

    def start_spider(self):
        # prepare_task_items()
        settings = get_project_settings()
        process=CrawlerProcess(settings)
        process.crawl('common_spider')
        process.start()
        # configure_logging(settings)
        # runner = CrawlerRunner(settings)
        # print(all_spiders)
        # #for spider in all_spiders:
        # #d=runner.crawl(all_spiders[0])
        # d = runner.join()
        # d.addBoth(lambda _: reactor.stop())
        # reactor.run()

    def start_validator(self):
        settings = get_project_settings()
        process=CrawlerProcess(settings)
        process.crawl('baidu_validator')
        process.start()

    def schedule(self):
        self.logger.log('start schedule')
        while not self.que.empty():
            self.que.get()
        time_start=time.time()
        for taskname, task in TASKS.items():
            self.que.put(Task_dict(
                taskname, task,
                time_start,
            ))

        while not self.que.empty():
            time_now=time.time()
            task_dict=self.que.get()
            self.logger.log('now waiting for '+task_dict.taskname)
            if time_now<task_dict.start_time:
                time.sleep(task_dict.start_time-time_now)

            self.start_processing(task_dict.taskname, task_dict.task)

            time_now=time.time()
            self.que.put(Task_dict(
                task_dict.taskname, task_dict.task,
                time_now+task_dict.task['interval']*60,
            ))
            # print(time_now+task['interval']*60, task)


    def start_processing(self, taskname, task):
        self.logger.log('\n'+"*"*54)
        self.logger.log('%-20s%s'%(taskname, 'start'))

        task_queue=[taskname+DB_SPLIT_SYMBOL+x for x in task["resource"]]
        self.rdb.delete(DB_RAW_IPPOOL_NAME)
        self.pipe.lpush(DB_TASK_QUEUE_NAME, *task_queue)
        self.pipe.execute()

        self.logger.log('%-20s%s'%(taskname, 'crawling'))
        process=Process(target=self.start_spider)
        process.start()
        process.join()
        ippool_size=self.ippool_turn_raw()

        self.logger.log('%-20s%s'%(taskname, 'validating'))
        process=Process(target=self.start_validator)
        process.start()
        process.join()

        ippool_size_now=self.rdb.zcard(DB_IPPOOL_NAME)
        self.logger.log('%-20s%s %03d\n'%(taskname, 'contribution', ippool_size_now-ippool_size))
        self.logger.log("*"*54)

    def ippool_turn_raw(self):
        ippool=self.rdb.zrange(DB_IPPOOL_NAME, 0, -1)
        ippool_size=len(ippool)
        if ippool_size>0:
            self.pipe.sadd(DB_RAW_IPPOOL_NAME, *ippool)
            self.pipe.delete(DB_IPPOOL_NAME)
        self.pipe.execute()
        return ippool_size
