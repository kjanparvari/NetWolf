import threading
from typing import List
import time


class DiscoveryMessage(object):

    def __init__(self, members):
        from netwolf.Members import Member
        self._members: List[Member] = members

    def __str__(self):
        s = ""
        for m in self._members:
            s += str(m) + "\n" + "----------------" + '\n'
        return s

    def __bytes__(self):
        s = 'dis$$$'
        flag = False
        for m in self._members:
            if flag:
                s += '$$$'
            flag = True
            s += m.getName() + ':' + str(m.getIp())
        return bytes(s, 'utf-8')

    def get_members(self):
        return self._members


class DiscoveryManager(object):
    _PERIOD = 10 * 1  # sec

    def __init__(self, manager, udp_server, udp_client):
        self._manager = manager
        self._receive_queue = []

        from netwolf.udp import UdpServer, UdpClient
        self._send_connection: UdpClient = udp_client
        self._receive_connection: UdpServer = udp_server

        self._timer_thread = threading.Thread(target=self.timer)
        self._timer_thread.start()

        self._queue_thread = threading.Thread(target=self._check_queue)
        self._queue_thread.start()

    def enqueue(self, msg: DiscoveryMessage):
        self._receive_queue.append(msg)

    def _check_queue(self):
        while True:
            if len(self._receive_queue) != 0:
                d: DiscoveryMessage = self._receive_queue.pop(0)
                self._manager.get_member_manager().updateList(d.get_members())

    def getPeriod(self):
        return self._PERIOD

    def _send(self, dest, lst):
        self._send_connection.send(str(dest.getIp()), lst)

    def setPeriod(self, p):
        self._PERIOD = p

    def timer(self):
        while True:
            time.sleep(self._PERIOD)
            print("[Discovery Client]: Time to send")
            friends = self._manager.get_member_manager().get_friend_list()
            for f in friends:
                lst = self._manager.get_member_manager().get_sendable_list(f)
                print("[Discovery Client]: Sending list to\n{}".format(str(f)))
                print(self._manager.get_member_manager().printList(lst))
                t = threading.Thread(target=self._send, args=(f, lst))
                t.start()
