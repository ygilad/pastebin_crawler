from scraper.common import ScrapePageBase


class PublicPasteScraper(ScrapePageBase):
    PUBLIC_PASTE_URL = 'https://pastebin.com/archive'

    def __init__(self):
        super().__init__(self.__class__.PUBLIC_PASTE_URL)
        self._latest_paste = None

    def set_latest_paste(self, latest_paste):
        self._latest_paste = latest_paste

    def _process_response(self, soup):
        pastes = list()
        for link_tag in soup.select("table.maintable tr a"):
            href = link_tag['href']
            if href.startswith('/archive'):
                continue
            pastes.append(href.strip('/'))
        return pastes

    def _process_post_response(self, res):
        if self._latest_paste and self._latest_paste in res:
            index = res.index(self._latest_paste)
            res = res[0:index]
        if res:
            self._latest_paste = res[0]
            res.reverse()
        return res
