class GetMessage(object):

    def __init__(self, filename):
        self._filename = filename

    def __bytes__(self):
        s = "get$$$" + self._filename
        return bytes(s, 'utf-8')

    def get_filename(self):
        return self._filename


class ResMessage(object):

    def __init__(self):
        self._port: int

    def __bytes__(self):
        s = "res$$$" + self._port
