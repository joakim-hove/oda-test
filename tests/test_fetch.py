import datetime
import pytest
import unittest

from scraper.util import *


class TestFetcher(unittest.TestCase):

    def test_fetcher_result(self):
        f1 = FetchResult(199)
        assert not f1

        f2 = FetchResult(200)
        assert f2


    def test_filter(self):
        empty_html = """
<html>
</html>
        """
        a = Fetcher.html_filter(empty_html, class_filter = ("a", "class"))
        assert a == []


        with_one_anchor = """
<html>
        <a href="abc", class="class1">Link text</a>
</html>
        """

        a = Fetcher.html_filter(with_one_anchor, class_filter = ("a", "class1"))
        assert len(a) == 1
        assert a[0].text == "Link text"

        with_two_anchors = """
<html>
        <a href="abc", class="class1">Link text1</a>
        <a href="abc", class="class2">Link text</a>
        <a href="abc", class="class1">Link text2</a>
</html>
        """

        a = Fetcher.html_filter(with_two_anchors, class_filter = ("a", "class1"))
        assert len(a) == 2
        assert a[0].text == "Link text1"
        assert a[1].text == "Link text2"

