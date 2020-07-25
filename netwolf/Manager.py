import threading


class Manager(object):
    def __init__(self):
        from netwolf.udp import UdpClient, UdpServer
        from netwolf.Members import MembersManager
        from netwolf.Discovery import DiscoveryManager
        self._udp_server = UdpServer()
        self._udp_client = UdpClient()
        self._discovery_manager = DiscoveryManager(self, self._udp_server, self._udp_client)
        self._member_manager = MembersManager(self)

    def setup(self):
        pass

    def get_member_manager(self):
        return self._member_manager

    def tmp(self):
        from netwolf.Serialization import serialize, deserialize
        # from netwolf.Members import Member
        # members = [Member("member 1", "192.168.1.1"), Member("member 2", "192.168.1.2"),
        #            Member("member 3", "192.168.1.3"),
        #            Member("member 4", "192.168.1.4"), Member("member 5", "192.168.1.5"),
        #            Member("member 6", "192.168.1.6")]
        # self._member_manager.updateList(members)
        # self._member_manager.remove_friend_list()
        self._member_manager.printList()

