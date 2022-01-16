import datetime
import time

import requests
from bs4 import BeautifulSoup

def parse(text):
    return BeautifulSoup(text, features="lxml")

class Throttle:

    def __init__(self, max_bandwidth):
        self.start_time = datetime.datetime.now()
        self.total_download = 0
        self.max_bandwidth = max_bandwidth


    def add_download(self, data_size):
        self.total_download += data_size


    def wait(self):
        if self.max_bandwidth:
            target_time = self.start_time + datetime.timedelta(seconds=self.total_download / self.max_bandwidth)

            now = datetime.datetime.now()
            if target_time > now:
                dt = target_time - now
                time.sleep(dt.total_seconds())


class FetchResult:
    def __init__(self, http_status, dom = None, content = None, url = None):
        self.http_status = http_status
        self.dom = dom
        self.content = content

    def __bool__(self):
        return self.http_status == 200



class Fetcher:
    def __init__(self, host, throttle):
        self.host = host
        self.throttle = throttle
        self.request_session = requests.Session()
        self.errors = {}

    def url(self, path):
        return self.host + path


    @classmethod
    def html_filter(cls, text, class_filter):
        dom = parse(text)
        if class_filter:
            tag,class_ = class_filter
            dom = dom.find_all(tag, class_ = class_)
        return dom


    def fetch_dom(self, url, class_filter = None):
        print(f"Fetching: {url}")
        self.throttle.wait()
        respons = self.request_session.get(url)
        if respons.status_code == 200:
            self.throttle.add_download(len(respons.content))
            dom = self.html_filter(respons.content, class_filter)
            return FetchResult(respons.status_code, dom=dom)
        else:
            error_result = FetchResult(respons.status_code, content=respons.text, url=url)
            self.errors.append(error_result)
            return error_result


