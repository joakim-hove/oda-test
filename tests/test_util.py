import datetime
import unittest
import pytest

from scraper.util import Throttle


class TestScraperUtil:


    def test_throttle(self):
        t1 = Throttle(max_speed = 0)
        t1.add_download(1024*1024*1024)

        st = datetime.datetime.now()
        t1.wait()
        dt = datetime.datetime.now() - st
        assert dt.total_seconds() <  1


        t2 = Throttle(max_speed=1024)
        t2.add_download(1024)
        st = datetime.datetime.now()
        t2.wait()
        dt = datetime.datetime.now() - st
        assert pytest.approx(dt.total_seconds(), 0.1) == 1
