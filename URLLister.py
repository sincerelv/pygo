# encoding:utf-8
import httplib, urllib, urlparse
from sgmllib import SGMLParser


# 解析指定的网页的html，得到该页面的超链接列表
class URLLister(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.urls = []

    def start_a(self, attrs):
        href = [v for k, v in attrs if k == 'href']
        if href:
            self.urls.extend(href)
