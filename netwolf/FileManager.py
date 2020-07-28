from os import path, mkdir
import time


class FileManager(object):
    _files_dir: str = ".//files"

    def __init__(self, manager):
        self._manager = manager
        self._get_msg_lock = False
        self._sent_time: time = None
        self._senders = []
        if not path.exists(self._files_dir):
            mkdir(self._files_dir)
        print(self.exists("a.txt"))
        print(self.get_size("a.txt"))

    def exists(self, filename: str) -> bool:
        dr = self._get_file_path(filename)
        if path.exists(dr) and path.isfile(dr):
            return True
        else:
            return False

    def _get_file_path(self, filename: str) -> str:
        return self._files_dir + "//" + filename

    def get_size(self, filename: str) -> int:
        if not self.exists(filename):
            return 0
        else:
            return path.getsize(self._get_file_path(filename))

    def _set_sent_time(self):
        self._sent_time = time.time()

    def send_get_message(self, filename):
        if not self._get_msg_lock:
            self._get_msg_lock = True
            self._senders.clear()
            self._set_sent_time()
            from netwolf.FileRequests import GetMessage
            msg = GetMessage(filename)
            self._manager.broadcast(msg)
        else:
            return False

    def receive_get_message(self, msg):
        filename = msg.get_file_name()
        if self.exists(filename):
            from netwolf.FileRequests import ResMessage
            pass

    def send_res_message(self):
        pass

    def receive_res_message(self):
        pass
