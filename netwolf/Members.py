import ipaddress
from typing import List
from os import path, stat


class Member(object):

    def __init__(self, name, ip):
        self._name: str = name
        self._ip: ipaddress.IPv4Address = ipaddress.IPv4Address(ip)

    def __str__(self):
        return "name: " + self._name + "\n" + "ip: " + str(self._ip)

    def __eq__(self, other):
        if self._name == other.getName() and self._ip == other.getIp():
            return True
        else:
            return False

    def __bytes__(self):
        s = "mem$$$" + self._name + ":" + str(self._ip)
        return bytes(s, 'utf-8')

    def getName(self):
        return self._name

    def getIp(self):
        return self._ip


class MembersManager(object):
    _friends_path = "./friends.nw"

    def __init__(self, manager):
        self._manager = manager
        self._membersList: List[Member] = []
        self._readList()
        self.updateList([self.get_current_member()])
        self._saveList()

    def _merge(self, new_list: List[Member]):
        for m in new_list:
            if not self._exists(m):
                self._add_member(m)

    def _exists(self, member: Member) -> bool:
        for m in self._membersList:
            if m.__eq__(member):
                return True
        else:
            return False

    def _readList(self):
        from netwolf.Serialization import deserialize
        if not path.exists(self._friends_path):
            f = open(self._friends_path, 'w')
            f.close()
            lst = []
        else:
            with open(self._friends_path, 'rb') as friends_file:
                if stat(self._friends_path).st_size == 0:
                    lst = []
                else:
                    lst = deserialize(friends_file.read())
                    friends_file.close()
        if isinstance(lst, Member):
            self._membersList = [lst]
        else:
            self._membersList = lst

    def _saveList(self, lst=None):
        from netwolf.Serialization import serialize
        if lst is None:
            lst = self._membersList
        with open(self._friends_path, 'wb') as friends_file:
            friends_file.write(serialize(lst))
            friends_file.close()

    def _add_member(self, member: Member):
        self._membersList.append(member)

    def updateList(self, new_list: List[Member] = None):
        self._readList()
        if new_list is not None:
            self._merge(new_list)
        self._saveList()

    def remove_friend_list(self):
        self._membersList = []
        self._saveList([])

    def get_friend_list(self) -> List[Member]:
        lst = self._membersList.copy()
        # lst.remove(self.get_current_member())
        return lst

    def printList(self, lst: List[Member] = None):
        if lst is None:
            self._readList()
            lst = self._membersList
        if len(lst) == 0:
            print("Friend List Is Empty!")
            return
        print("----------------")
        for mem in lst:
            print(mem)
            print("----------------")

    @staticmethod
    def get_current_member() -> Member:
        import socket
        name = socket.gethostname()
        ip = socket.gethostbyname(name)
        return Member(name, ip)

    def get_sendable_list(self, dest: Member):
        print("Preparing List to send to\n{}".format(str(dest)))
        lst = self._membersList.copy()
        lst.remove(dest)
        # lst.remove(self.get_current_member())
        return lst
