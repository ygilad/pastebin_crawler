from common.general import general_logger
from dal.paste_db import paste_db
from workers.common import WorkerThreadBase


class PasteSaverWorker(WorkerThreadBase):

    def __init__(self, in_q=None, out_q=None):
        super().__init__(in_q, out_q)
        self._log = general_logger(self.__class__.__name__)

    def _db(self):
        if not hasattr(self, '_db_obj'):
            self._db_obj = paste_db()
        return self._db_obj

    def perform(self, paste):
        db = self._db()
        db.insert_paste(paste)
        self._log.debug("Saved paste %s" % paste.key)
