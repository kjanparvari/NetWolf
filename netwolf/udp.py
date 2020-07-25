import threading
import socket

UDP_PORT = 7440


class UdpServer:

    def __init__(self, host_info=None):
        if host_info is None:
            host_info = socket.gethostbyname(socket.gethostname()), UDP_PORT
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(host_info)

    def setup(self):
        print("[Discovery Server]: Starting...")
        self._socket.listen()
        while True:
            connection, address = self._socket.accept()
            t = threading.Thread(target=self._handle_client, args=(connection, address))
            t.start()

    @staticmethod
    def _handle_client(conn: socket.socket, address):
        from netwolf.Serialization import deserialize
        print("[Discovery Server]: New Discovery Connection from{}".format(address))
        msg = conn.recv(1024)
        res = deserialize(msg)
        print(res)


class UdpClient:
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, server_addr, message):
        server_info = server_addr, UDP_PORT
        from netwolf.Serialization import serialize
        self._socket.connect(server_info)  # address , port
        msg = serialize(message)
        self._socket.send(msg)
