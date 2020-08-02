import threading
from os import path, mkdir
import time


class FileManager(object):
    _files_dir: str = ".//files"
    _MAX_WAIT_TIME = 5

    def __init__(self, manager):
        from netwolf.Load import LoadController
        self._manager = manager
        self._load_controller = LoadController(self._MAX_WAIT_TIME)
        self._get_msg_lock = False
        self._waiting_for_res = False
        self._requested_filename = ""
        self._sent_time: time = None
        self._senders = []
        self._requests = []
        if not path.exists(self._files_dir):
            mkdir(self._files_dir)

    def exists(self, filename: str) -> bool:
        dr = self._get_file_path(filename)
        if path.exists(dr) and path.isfile(dr):
            return True
        else:
            return False

    def create_file(self, filename):
        p = self._get_file_path(filename)
        f = open(p, 'wb')
        return f

    def get_file(self, filename):
        p = self._get_file_path(filename)
        f = open(p, 'rb')
        return f

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

    def _check_timer(self):
        while True:
            if (time.time() - self._sent_time) > self._MAX_WAIT_TIME:
                self._waiting_for_res = False
                self._choose_sender()
                break

    def _choose_sender(self):
        if len(self._senders) == 0:
            print("[File Manager]: No one had the requested file ...")
            self.receiving_file_finished()
            return False
        else:
            min_time = self._MAX_WAIT_TIME
            chosen_one = None
            chosen_port: int = -1
            for t in self._senders:
                if t[2] < min_time:
                    min_time = t[2]
                    chosen_one = t[0]
                    chosen_port = t[1]
            self._send_snd_message(chosen_one, chosen_port)
            return True

    def request_file(self, filename):
        if not self._get_msg_lock:
            print(f"[File Manager]: Requesting for {filename}")
            self._get_msg_lock = True
            self._requested_filename = filename
            self._senders.clear()
            self._send_get_message(filename)
            self._waiting_for_res = True
            self._set_sent_time()
            self._start_timer()
        else:
            print("[File Manager]: Already waiting for another file ...")
            return

    def _send_get_message(self, filename):
        from netwolf.FileRequests import GetMessage
        msg = GetMessage(filename)
        self._manager.broadcast(msg)

    def receive_get_message(self, msg, sender_addr):
        print(f"[File Manager]: {sender_addr} requested for a file named {msg.get_filename()}")
        filename = msg.get_filename()
        if self.exists(filename):
            if self._load_controller.reserve_ticket(sender_addr, filename):
                port = self._manager.get_tcp_client().reserve_port()
                t = filename, sender_addr, port
                self._requests.append(t)
                from netwolf.FileRequests import ResMessage
                res = ResMessage(port)
                self._send_res_message(sender_addr, res)

    def _send_res_message(self, dest_addr, msg):
        print(f"[File Manager]: telling {dest_addr} that requested file is existing")
        self._manager.get_udp_client().send(str(dest_addr), msg)

    def receive_res_message(self, msg, sender_addr):
        print(f"[File Manager]: {sender_addr} had requested file (requested port: {msg.get_port()}).")
        if self._waiting_for_res:
            rt = time.time() - self._sent_time
            port = msg.get_port()
            info = sender_addr, port, rt
            self._senders.append(info)
        else:
            print("[File Manager]: Response message arrived too late ...")

    def _send_snd_message(self, dest_addr, port):
        print(f"[File Manager]: sending file ({self._requested_filename}) to {dest_addr} on port {port}")
        from netwolf.FileRequests import SndMessage
        msg = SndMessage()
        self._manager.get_udp_client().send(str(dest_addr), msg)
        self._manager.get_tcp_server().get_file(dest_addr, port, self._requested_filename)

    def receive_snd_message(self, sender_addr):
        found = False
        for t in self._requests:
            if t[1] == sender_addr:
                found = True
                self._load_controller.confirm(t[1], t[0])
                self._manager.get_tcp_client().send_file(t[1], t[2], t[0])
                print(
                    f"[File Manager]: {sender_addr} will send the requested file ({t[0]}) on port {t[2]}")
                break
        if not found:
            print("[Error]: error occurred in finding requested file")
            return

    def receiving_file_finished(self):
        print(f"[File Manager]: terminating request for file.")
        self._get_msg_lock = False
        self._requested_filename = ""
        self._senders.clear()
        self._sent_time: time = None
        self._waiting_for_res = False
