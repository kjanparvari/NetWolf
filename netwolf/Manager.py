import threading


class Manager(object):
    def __init__(self):
        from netwolf.udp import UdpClient, UdpServer
        from netwolf.Members import MembersManager
        from netwolf.Discovery import DiscoveryManager
        self._udp_server = UdpServer(self)
        self._udp_client = UdpClient(self)
        self._discovery_manager = DiscoveryManager(self)
        self._member_manager = MembersManager(self)

    def setup(self):
        pass

    def get_member_manager(self):
        return self._member_manager

    def get_discovery_manager(self):
        return self._discovery_manager

    def get_udp_client(self):
        return self._udp_client

    def broadcast(self, obj):
        friends = self._member_manager.get_friend_list()
        for f in friends:
            self._udp_client.send(str(f.getIp()), obj)

    def tmp(self):
        from netwolf.Serialization import serialize, deserialize
        # from netwolf.Members import Member
        # members = [Member("member 1", "192.168.1.1"), Member("member 2", "192.168.1.2"),
        #            Member("member 3", "192.168.1.3"),
        #            Member("member 4", "192.168.1.4"), Member("member 5", "192.168.1.5"),
        #            Member("member 6", "192.168.1.6")]
        # members = [Member("Leviathan", "192.168.1.102")]
        # self._member_manager.updateList(members)
        # self._member_manager.remove_friend_list()
        # self._member_manager.printList()
        pass
