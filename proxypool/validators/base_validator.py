import scrapy

from twisted.internet.error import TimeoutError

from ..task_queue import RedisProxyQueue
from ..items import ProxyUrlItem
from ..logger import Logger

class BaseValidator(scrapy.Spider):
    name='base_validator'
    proxy_queue=RedisProxyQueue()
    validate_rules=[]
    validate_check_sign=[]
    logger=Logger()

    custom_settings = {
        'DOWNLOAD_TIMEOUT': 1,
        'CONCURRENT_REQUESTS': 50,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 50,
        'RETRY_ENABLED': False,
        'DOWNLOADER_MIDDLEWARES': {
            'proxypool.middlewares.TimerMiddleware': 500,
        },
        'ITEM_PIPELINES': {
            'proxypool.pipelines.RedisProxyPipeline': 200,
        }
    }

    def start_requests(self):
        while not self.proxy_queue.empty():
            proxy=self.proxy_queue.get().decode('utf-8')
            for rule in self.validate_rules:
                for url in rule['urls']:
                    yield scrapy.Request(url, meta={'proxy':proxy},
                        callback=self.parse, errback=self.parse_error, dont_filter=True)

    def parse(self, response):
        url=response.meta['proxy']
        speed=response.meta['speed']
        if not self.is_valuable(response):
            return None

        self.logger.log("url:%-35s speed:%f"%(url, speed))
        return ProxyUrlItem(url=url, speed=speed)

    def is_valuable(self, response):
        for sign in self.validate_check_sign:
            if sign not in response.text:
                return False
        return True

    def parse_error(self, failure):
        if failure.check(TimeoutError):
            # print("Timeout")
            pass

