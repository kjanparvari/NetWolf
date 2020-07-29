import threading
from os import path, mkdir
import time


class FileManager(object):
    _files_dir: str = ".//files"
    _MAX_WAIT_TIME = 5

    def __init__(self, manager):
        self._manager = manager
        self._get_msg_lock = False
        self._waiting_for_res = False
        self._sent_time: time = None
        self._senders = []
        self._reserved_port: int = -1
        if not path.exists(self._files_dir):
            mkdir(self._files_dir)

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

    def _start_timer(self):
        threading.Thread(target=self._check_timer).start()

    def _choose_sender(self):
        self._waiting_for_res = False
        if len(self._senders) == 0:
            print("No one had requested file ...")
        else:
            min_time = self._MAX_WAIT_TIME
            chosen_one = None
            for t in self._senders:
                if t[1] < min_time:
                    min_time = t[1]
                    chosen_one = t[0]
            from netwolf.FileRequests import ResMessage
            from netwolf.tcp import TcpClient
            self._reserved_port = self._manager.get_udp_client().reserve_port()
            msg = ResMessage(self._reserved_port)
            self._send_res_message(chosen_one, msg)

    def _check_timer(self):
        while True:
            if (time.time() - self._sent_time) > self._MAX_WAIT_TIME:
                self._choose_sender()

    def send_get_message(self, filename):
        if not self._get_msg_lock:
            self._get_msg_lock = True
            self._senders.clear()
            self._set_sent_time()
            self._start_timer()
            from netwolf.FileRequests import GetMessage
            msg = GetMessage(filename)
            self._waiting_for_res = True
            self._manager.broadcast(msg)
        else:
            print("[Error]: Already waiting for another file...")
            return False

    def receive_get_message(self, msg, sender_info):
        if self._waiting_for_res:
            filename = msg.get_file_name()
            if self.exists(filename):
                from netwolf.FileRequests import ResMessage
                pass
        else:
            print("[Error]: Response message arrived too late ...")

    def _send_res_message(self, dest_addr, msg):
        self._manager.get_udp_client().send(str(dest_addr), msg)

    def receive_res_message(self, msg, sender_info):
        pass
