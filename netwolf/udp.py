import threading
import socket

UDP_DISCOVERY_PORT = 7440
UDP_MESSAGE_PORT = 7880


class UdpServer:

    def __init__(self, manager):
        self._manager = manager

        # setting up discovery server
        host_info = socket.gethostbyname(socket.gethostname()), UDP_DISCOVERY_PORT
        self._discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._discovery_socket.bind(host_info)
        self._thread = threading.Thread(target=self._setup_discovery_server)
        self._thread.start()

        # setting up messages server
        host_info = socket.gethostbyname(socket.gethostname()), UDP_MESSAGE_PORT
        self._messages_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._messages_socket.bind(host_info)
        self._thread = threading.Thread(target=self._setup_messages_server)
        self._thread.start()

    def _setup_discovery_server(self):
        print("[UDP Discovery Server]: Starting...")
        from netwolf.Serialization import deserialize
        from netwolf.Discovery import DiscoveryMessage
        while True:
            msg, addr = self._discovery_socket.recvfrom(1024)  # buffer size is 1024 bytes
            print("[UDP Discovery Server]: New Discovery Connection from {}".format(addr))
            res = deserialize(msg)
            if isinstance(res, DiscoveryMessage):
                self._manager.get_discovery_manager().enqueue(res)

    def _setup_messages_server(self):
        print("[UDP Messages Server]: Starting...")
        from netwolf.Serialization import deserialize
        from netwolf.FileRequests import GetMessage, ResMessage, SndMessage
        while True:
            msg, (addr, port) = self._messages_socket.recvfrom(512)  # buffer size is 512 bytes
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
        port: int
        if isinstance(message, DiscoveryMessage):
            port = UDP_DISCOVERY_PORT
        elif isinstance(message, str):
            port = UDP_MESSAGE_PORT
        else:
            return
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_info = server_addr, port
        if isinstance(message, DiscoveryMessage):
            print("[UDP Client]: Sending discovery message to {}".format(server_info))
        else:
            print("[UDP Client]: Sending message to {}".format(server_info))
        from netwolf.Serialization import serialize
        s.connect(server_info)  # address , port
        msg = serialize(message)
        s.send(msg)
