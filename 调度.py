import gevent
import httpx
from 自动化.爬虫.模板.MessageQueue import Queue
from parsel import Selector
import pymysql
import pymongo
import redis


class Requests:
    def __init__(self, url: str, header=None):
        if header is None:
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 "
                              "Safari/537.36 QIHU 360EE"}
        self.url = url
        self.header = header

    def run(self):
        print(self.url)
        response = httpx.get(self.url, headers=self.header)
        response.encoding = 'utf-8'
        return response.text


class Schedule:
    def __init__(self, urls):
        self.queue = Queue('schedule')
        for i in urls:
            self.queue.put(i)

    def run(self):
        while not self.queue.empty():
            item = self.queue.get()
            self.parse(item, self.queue)

    def parse(self, item, queue):
        pass


class Parse:
    def __init__(self, html, queue):
        self.selector = Selector(html)
        self.queue = queue

    def parse(self):
        pass


class Pipeline:
    def __init__(self, item, type, db):
        self.item = item
        self.type = type
        self.db = db

    def run(self):
        pass


class MySQL:
    pass


class MongoDB:
    pass


class Redis:
    def __init__(self, item, db):
        self.item = item
        self.db = db
        self.red = redis.StrictRedis(host='127.0.0.1', port=6379, db=2)

    def save(self):
        print(f'开始保存{self.item}')
        self.red.hmset(self.db, self.item)


class FileDownload:
    def __init__(self, item):
        self.item = item

    def download(self):
        pass


def main():
    pass


if __name__ == "__main__":
    main()
