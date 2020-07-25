import threading
import socket

UDP_PORT = 7440


class UdpServer:

    def __init__(self, manager, host_info=None):
        self._manager = manager
        if host_info is None:
            host_info = socket.gethostbyname(socket.gethostname()), UDP_PORT
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(host_info)
        self._thread = threading.Thread(target=self.setup)
        self._thread.start()

    def setup(self):
        print("[UDP Server]: Starting...")
        # self._socket.listen()
        from netwolf.Serialization import deserialize
        from netwolf.Discovery import DiscoveryMessage
        while True:
            msg, addr = self._socket.recvfrom(1024)  # buffer size is 1024 bytes
            print("[UDP Server]: New Discovery Connection from{}".format(addr))
            print(msg)
            res = deserialize(msg)
            if isinstance(res, DiscoveryMessage):
                self._manager.get_discovery_manager().enqueue(res)
            print(res)
            # connection, address = self._socket.accept()
            # t = threading.Thread(target=self._handle_client, args=(connection, address))
            # t.start()

    @staticmethod
    def _handle_client(conn: socket.socket, address):
        from netwolf.Serialization import deserialize
        print("[Discovery Server]: New Discovery Connection from{}".format(address))
        msg = conn.recv(1024)
        res = deserialize(msg)
        print(res)


class UdpClient:
    def __init__(self, manager):
        self._manager = manager
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, server_addr, message):
        server_info = server_addr, UDP_PORT
        print("[UDP Client]: Sending message to {}".format(server_info))
        print(message)
        from netwolf.Serialization import serialize
        self._socket.connect(server_info)  # address , port
        msg = serialize(message)
        self._socket.send(msg)
