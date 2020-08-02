import struct
import threading
import socket

UDP_DISCOVERY_PORT = 7440
UDP_MESSAGE_PORT = 7880


class UdpServer:

    def __init__(self, manager):
        self._manager = manager

        # setting up discovery server
        host_info = socket.gethostbyname(socket.gethostname()), UDP_DISCOVERY_PORT
        # host_info = socket.gethostbyname('0.0.0.0'), UDP_DISCOVERY_PORT
        self._discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._discovery_socket.bind(host_info)
        threading.Thread(target=self._setup_discovery_server).start()

        # setting up messages server
        host_info = socket.gethostbyname(socket.gethostname()), UDP_MESSAGE_PORT
        self._messages_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._messages_socket.bind(host_info)
        threading.Thread(target=self._setup_messages_server).start()

    def _setup_discovery_server(self):
        print("[UDP Discovery Server]: Starting ...")
        while True:
            msg, (addr, port) = self._discovery_socket.recvfrom(1024)  # buffer size is 1024 bytes
            print('hello')
            threading.Thread(target=self._handle_discovery_msg, args=(msg, addr, port)).start()

    def _handle_discovery_msg(self, msg, addr, port):
        from netwolf.Serialization import deserialize
        from netwolf.Discovery import DiscoveryMessage
        print(f"[UDP Discovery Server]: New Discovery Connection from {addr}")
        res = deserialize(msg)
        if isinstance(res, DiscoveryMessage):
            self._manager.get_discovery_manager().enqueue(res)
        else:
            print(f"[UDP Server]: Unknown Message : {res}")

    def _setup_messages_server(self):
        print("[UDP Messages Server]: Starting...")

        while True:
            msg, (addr, port) = self._messages_socket.recvfrom(512)  # buffer size is 512 bytes
            threading.Thread(target=self._handle_file_msg, args=(msg, addr, port)).start()

    def _handle_file_msg(self, msg, addr, port):
        from netwolf.Serialization import deserialize
        from netwolf.FileRequests import GetMessage, ResMessage, SndMessage
        print("[UDP Messages Server]: New Message Connection from {}".format(addr))
        res = deserialize(msg)
        if isinstance(res, GetMessage):
            self._manager.get_file_manager().receive_get_message(res, addr)
        elif isinstance(res, ResMessage):
            self._manager.get_file_manager().receive_res_message(res, addr)
        elif isinstance(res, SndMessage):
            self._manager.get_file_manager().receive_snd_message(addr)
        else:
            print(f"[UDP Server]: Unknown Message : {res}")


class UdpClient:
    def __init__(self, manager):
        self._manager = manager

    def send(self, server_addr, message):
        threading.Thread(target=self._send(server_addr, message)).start()

    @staticmethod
    def _send(server_addr, message):
        from netwolf.Discovery import DiscoveryMessage
        from netwolf.FileRequests import GetMessage, SndMessage, ResMessage
        port: int
        if isinstance(message, DiscoveryMessage):
            port = UDP_DISCOVERY_PORT
        elif isinstance(message, GetMessage) or isinstance(message, SndMessage) or isinstance(message, ResMessage):
            port = UDP_MESSAGE_PORT
        else:
            return
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server_info = server_addr, port
        if isinstance(message, DiscoveryMessage):
            print(f"[UDP Client]: Sending discovery message to {server_addr} on port {port}")
        else:
            print(f"[UDP Client]: Sending message to {server_addr} on port {port}")
        from netwolf.Serialization import serialize
        s.connect(server_info)  # address , port
        msg = serialize(message)
        s.sendto(msg, server_info)
