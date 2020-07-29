import logging

from common.general import general_logger
from scraper.paste_page import PastePageScraper
from workers.common import WorkerThreadBase


class PasteScrapingWorker(WorkerThreadBase):
    def __init__(self, in_q=None, out_q=None):
        super().__init__(in_q, out_q)
        self._log = general_logger(self.__class__.__name__)

    def perform(self, task):
        scraper = PastePageScraper(task.key)
        res = scraper.scrape()

        if self._log.isEnabledFor(logging.DEBUG):
            self._log.debug("Scraped paste page: %s" % res.to_dict())
        return res
