import abc

import requests
from bs4 import BeautifulSoup


class ScrapePageBase(metaclass=abc.ABCMeta):
    BS4_PARSER = 'lxml'

    def __init__(self, url):
        self._url = url

    def _request_url_content(self):
        res = requests.get(self._url)
        return res.content

    def _soup(self, html_str):
        return BeautifulSoup(html_str, self.__class__.BS4_PARSER)

    @abc.abstractmethod
    def _process_response(self, soup):
        return list()

    def _process_post_response(self, res):
        return res

    def scrape(self):
        content = self._request_url_content()
        res = self._process_response(self._soup(content))
        res = self._process_post_response(res)
        return res
