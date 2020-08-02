class GetMessage(object):

    def __init__(self, filename):
        self._filename = filename

    def __bytes__(self):
        s = "get$$$" + self._filename
        return bytes(s, 'utf-8')

    def get_filename(self):
        return self._filename

    def __str__(self):
        return f"get {self._filename}"


class ResMessage(object):

    def __init__(self, port: int):
        self._port = port

    def __bytes__(self):
        s = "res$$$" + str(self._port)
        return bytes(s, 'utf-8')

    def get_port(self):
        return self._port

    def __str__(self):
        return f"res on port {self._port}"


class SndMessage(object):

    def __bytes__(self):
        s = "snd$$$"
        return bytes(s, 'utf-8')

    def __str__(self):
        return "send"
