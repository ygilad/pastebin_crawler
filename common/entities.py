from common.general import PasteBinTime


class EntityBase:
    def to_dict(self):
        return self.__dict__.copy()


class Paste(EntityBase):
    NAME_PLACEHOLDERS = ['guest', 'anonymous', 'unknown']

    def __init__(self, key=None, url=None, date=None, user=None, title=None, content=None):
        self.key = key
        self.url = url
        self.date = date
        self.user = user
        self.title = title
        self.content = content

    def cleanup(self):
        self.date = PasteBinTime(self.date).to_utc()
        self.user = self.__class__._cleanup_placeholders(self.user)
        self.title = self.__class__._cleanup_placeholders(self.title)
        self.content = self.content.strip()

    @classmethod
    def _cleanup_placeholders(cls, string):
        string = string.strip()
        if string.lower() in cls.NAME_PLACEHOLDERS:
            string = ''
        return string


class ScrapingTask(EntityBase):
    def __init__(self, key=None):
        self.key = key
