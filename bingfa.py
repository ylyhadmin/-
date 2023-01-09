from multiprocessing.dummy import Process, Queue
from threading import Thread
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 "
                  "Safari/537.36 QIHU 360EE"}


class DownloadThread(Thread):
    def __init__(self, url, pq):
        Thread.__init__(self)
        self.url = url
        self.pq = pq
        self.content = None

    def run(self) -> None:
        print(f'开始下载{self.url}')
        response = requests.get(self.url, headers=headers)
        response.encoding = 'utf-8'
        self.content = response.text
        self.get_content()
        print(f'{self.url}下载完毕')

    def get_content(self):
        self.pq.put((self.url, self.content))


class DownloadProcess(Process):
    def __init__(self, dq, pq):
        Process.__init__(self)
        self.dq = dq
        self.pq = pq

    def run(self) -> None:
        while True:
            try:
                url = self.dq.get(timeout=5)
                dt = DownloadThread(url, self.pq)
                dt.start()
                dt.join()
            except Exception:
                break
        print('下载完毕')


class SaveThread(Thread):
    def __init__(self, p):
        Thread.__init__(self)
        self.p = p

    def run(self):
        pass

    def save_mongo(self, item):
        pass

    def save_image(self, item):
        pass

    def save_json(self, item):
        pass

    def save_csv(self, item):
        pass

    def save_txt(self, item):
        pass

    def save_xml(self, item):
        pass


class ParseThread(Thread):
    def __init__(self, url, html, dq):
        Thread.__init__(self)
        self.url = url
        self.html = html
        self.dq = dq

    def run(self) -> None:
        pass


class ParseProcess(Process):
    def __init__(self, dq, pq):
        Process.__init__(self)
        self.dq = dq
        self.pq = pq

    def run(self) -> None:
        while True:
            try:
                url, html = self.pq.get(timeout=5)
                pt = ParseThread(url, html, self.dq)
                pt.start()
                pt.join()
            except Exception:
                break
        print('解析完毕')
