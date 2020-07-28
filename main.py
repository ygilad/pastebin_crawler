import queue
from time import sleep

from common.entities import ScrapingTask
from common.general import Borg
from dal.paste_db import PastesDB
from scraper.public_pastes import PublicPasteScraper
from workers.db_worker import PasteSaverWorker
from workers.paste_worker import PasteScrapingWorker


class PasteBinScrapeProducer(Borg):
    NEW_SCRAPE_INTERVAL = 120
    MAX_ITERATIONS = 100
    SCRAPER_WORKER_COUNT = 1

    def __init__(self):
        super().__init__()

        self._scraper_q = queue.Queue()
        self._db_saver_q = queue.Queue()

        self._workers = list()
        for i in range(self.__class__.SCRAPER_WORKER_COUNT):
            self._workers.append(PasteScrapingWorker(in_q=self._scraper_q, out_q=self._db_saver_q))
        self._workers.append(PasteSaverWorker(in_q=self._db_saver_q))

        self._scraper = PublicPasteScraper()
        latest_paste = PastesDB().get_latest_paste()
        if latest_paste:
            self._scraper.set_latest_paste(latest_paste['key'])

    def main_loop(self):
        for worker in self._workers:
            worker.start()

        for i in range(self.__class__.MAX_ITERATIONS):
            pastes = self._scraper.scrape()

            for paste in pastes:
                self._scraper_q.put(ScrapingTask(paste))

            sleep(self.__class__.NEW_SCRAPE_INTERVAL)

        for worker in self._workers:
            worker.join()


if __name__ == '__main__':
    PasteBinScrapeProducer().main_loop()
