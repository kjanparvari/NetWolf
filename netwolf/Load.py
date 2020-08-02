import time
import threading


class LoadController:

    def __init__(self, wm):
        self._tickets: int = 5
        self._reserves = []
        self._WAIT_TIME = wm * 2
        threading.Thread(target=self._setup_timer).start()

    def reserve_ticket(self, addr, filename):
        if self._tickets > 0:
            self._tickets -= 1
            t = addr, filename, False
            self._reserves.append(t)
            threading.Thread(target=self._setup_req_timer, args=t).start()
            return True
        else:
            return False

    def confirm(self, addr, filename):
        for t in self._reserves:
            if t[0] == addr and t[1] == filename and t[2] is False:
                self._reserves.remove(t)
                return True
        return False

    def _setup_req_timer(self, req):
        time.sleep(self._WAIT_TIME)
        for t in self._reserves:
            if t[0] == req[0] and t[1] == req[1] and t[2] is False:
                self._reserves.remove(t)
                self._tickets += 1
                break

    def _setup_timer(self):
        while True:
            time.sleep(2 * self._WAIT_TIME)
            if self._tickets < 5:
                self._tickets += 1
