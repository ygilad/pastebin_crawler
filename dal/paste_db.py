import abc

from common.entities import Paste
from common.general import Borg, PasteBinTime
from tinydb import TinyDB


def paste_db():
    # This factory function for PastesTinyDB will allow
    # switching dal implementations quickly
    return PastesTinyDB()


class PastesDBBase(Borg, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def insert_paste(self, paste):
        pass

    @abc.abstractmethod
    def get_latest_paste(self):
        return dict()


class PastesTinyDB(PastesDBBase):
    PASTE_DB_FILENAME = 'pastes.db.json'
    MATA_DB_FILENAME = 'meta.db.json'

    def __init__(self):
        super().__init__()

        if not hasattr(self, '_pastes_db'):
            self._pastes_db = TinyDB(self.__class__.PASTE_DB_FILENAME)
        if not hasattr(self, '_meta_db'):
            self._meta_db = TinyDB(self.__class__.MATA_DB_FILENAME)

    def insert_paste(self, paste):
        if isinstance(paste, Paste):
            paste = paste.to_dict()
        self._pastes_db.insert(paste)

        self._update_latest_paste(paste)

    def get_latest_paste(self):
        meta_records = self._meta_db.all()
        return meta_records[0] if meta_records else None

    def _update_latest_paste(self, paste):
        meta_record = self.get_latest_paste()
        if meta_record:
            record_ts = PasteBinTime(meta_record['date']).to_ts()
            paste_ts = PasteBinTime(paste['date']).to_ts()

            # if no need to change the current record - return before change
            if meta_record['key'] == paste['date'] or record_ts > paste_ts:
                return

        self._meta_db.truncate()
        self._meta_db.insert(paste)
