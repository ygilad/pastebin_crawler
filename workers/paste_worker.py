from scraper.paste_page import PastePageScraper
from workers.common import WorkerThreadBase


class PasteScrapingWorker(WorkerThreadBase):
    def perform(self, task):
        scraper = PastePageScraper(task.key)
        res = scraper.scrape()
        return res
