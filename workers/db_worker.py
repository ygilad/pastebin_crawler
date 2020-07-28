from dal.paste_db import PastesDB
from workers.common import WorkerThreadBase


class PasteSaverWorker(WorkerThreadBase):
    def _db(self):
        if not hasattr(self, '_db_obj'):
            self._db_obj = PastesDB()
        return self._db_obj

    def perform(self, paste):
        db = self._db()
        db.insert_paste(paste)
