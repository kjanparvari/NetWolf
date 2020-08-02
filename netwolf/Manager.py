import threading


class Manager(object):
    def __init__(self):
        from netwolf.udp import UdpClient, UdpServer
        from netwolf.Members import MembersManager
        from netwolf.Discovery import DiscoveryManager
        from netwolf.FileManager import FileManager
        from netwolf.tcp import TcpClient, TcpServer

        self._udp_server = UdpServer(self)
        self._udp_client = UdpClient(self)
        self._tcp_server = TcpServer(self)
        self._tcp_client = TcpClient(self)
        self._discovery_manager = DiscoveryManager(self)
        self._member_manager = MembersManager(self)
        self._file_manager = FileManager(self)
        # self._tcp_client.reserve_port()

    def setup(self):
        pass

    def get_file_manager(self):
        return self._file_manager

    @staticmethod
    def get_host_info():
        import socket
        name = socket.gethostname()
        addr = socket.gethostbyname(name)
        return name, addr

    def get_member_manager(self):
        return self._member_manager

    def get_discovery_manager(self):
        return self._discovery_manager

    def get_udp_client(self):
        return self._udp_client

    def get_tcp_client(self):
        return self._tcp_client

    def get_tcp_server(self):
        return self._tcp_server

    def broadcast(self, obj):
        friends = self._member_manager.get_friend_list()
        for f in friends:
            self._udp_client.send(str(f.getIp()), obj)

    def tmp(self):
        from netwolf.Serialization import serialize, deserialize
        from netwolf.Members import Member
        members = [Member("member 1", "192.168.1.1"), Member("member 2", "192.168.1.2"),
                   Member("member 3", "192.168.1.3"),
                   Member("member 4", "192.168.1.4"), Member("member 5", "192.168.1.5"),
                   Member("member 6", "192.168.1.6")]
        # members = [Member("Leviathan", "192.168.1.105")]
        self._member_manager.updateList(new_list=members)
        # self._member_manager.remove_friend_list()
        # self._member_manager.printList()
        # self._file_manager.request_file("a.txt")
        # self._file_manager.request_file("a.txt")
        # self._tcp_server.get_file('192.168.1.105', 4040, 'a.txt')
        # self._tcp_client.send_file('192.168.1.105', 4040, 'a.txt')
        pass
