from common.general import general_logger
from scraper.common import ScrapePageBase


class PublicPasteScraper(ScrapePageBase):
    PUBLIC_PASTE_URL = 'https://pastebin.com/archive'

    def __init__(self):
        super().__init__(self.__class__.PUBLIC_PASTE_URL)
        self._latest_paste = None
        self._log = general_logger(self.__class__.__name__)

    def set_latest_paste(self, latest_paste):
        self._latest_paste = latest_paste

    def _process_response(self, soup):
        pastes = list()
        for link_tag in soup.select("table.maintable tr a"):
            href = link_tag['href']
            if href.startswith('/archive'):
                continue
            pastes.append(href.strip('/'))

        self._log.info("Found %d paste pages in archive page" % len(pastes))
        return pastes

    def _process_post_response(self, res):
        if self._latest_paste and self._latest_paste in res:
            index = res.index(self._latest_paste)
            res = res[0:index]
            self._log.info(
                "Some pages were already scraped. " +
                "Adding %d pages to scraper queue" % len(res)
            )
        if res:
            self._latest_paste = res[0]
            res.reverse()
        return res
