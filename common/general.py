import arrow


class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class PasteBinTime:
    PASTEBIN_TIME_FORMAT = 'dddd Do of MMMM YYYY HH:mm:ss A ZZ'

    def __init__(self, time_str):
        # CDT/CST are not supported in arrow. convert
        time_str = time_str.replace('CDT', '-05:00')
        time_str = time_str.replace('CST', '-06:00')

        self._arrow = arrow.get(time_str, self.__class__.PASTEBIN_TIME_FORMAT)

    def to_utc(self):
        return self._arrow.to('utc').format(self.__class__.PASTEBIN_TIME_FORMAT)

    def to_ts(self):
        return self._arrow.timestamp
