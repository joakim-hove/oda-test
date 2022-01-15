import datetime
import time

import requests
from bs4 import BeautifulSoup

class Throttle:

    def __init__(self, max_speed=1024*256*0):
        self.start_time = datetime.datetime.now()
        self.total_download = 0
        self.max_speed = max_speed


    def add_download(self, data_size):
        self.total_download += data_size


    def wait(self):
        if self.max_speed:
            target_time = self.start_time + datetime.timedelta(seconds=self.total_download / self.max_speed)

            now = datetime.datetime.now()
            if target_time > now:
                dt = target_time - now
                time.sleep(dt.total_seconds())


class FetchResult:
    def __init__(self, http_status, dom = None, content = None):
        self.http_status = http_status
        self.dom = dom
        self.content = content

    def __bool__(self):
        return self.http_status == 200



class Fetcher:
    def __init__(self):
        self.throttle = Throttle()
        self.request_session = requests.Session()

    @classmethod
    def html_filter(cls, text, class_filter):
        dom = BeautifulSoup(text, features="html.parser")
        if class_filter:
            tag,class_ = class_filter
            dom = dom.find_all(tag, class_ = class_)
        return dom


    def fetch_dom(self, url, class_filter = None):
        print(f"Fetching: {url}")
        respons = self.request_session.get(url)
        if respons.status_code == 200:
            dom = self.html_filter(respons.content, class_filter)
            return FetchResult(respons.status_code, dom=dom)
        else:
            return FetchResult(respons.status_code, content=respons.text)


