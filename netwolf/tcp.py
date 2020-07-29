import threading
import socket

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


class TcpServer(object):

    def __init__(self, manager):
        self._manager = manager

    def _setup(self, port):
        print("[TCP Server] server is starting...")
        server_address = socket.gethostbyname(socket.gethostname())
        self._server_info = (server_address, port)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(self._server_info)
        threading.Thread(target=self._start).start()

    @staticmethod
    def _handle_client(conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False

                print(f"[{addr}] {msg}")
                conn.send("Msg received".encode(FORMAT))

        conn.close()

    def _start(self):
        self._socket.listen()
        print(f"[LISTENING] Server is listening on {self._server_info[0]}")
        while True:
            conn, addr = self._socket.accept()
            thread = threading.Thread(target=self._handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    def _find_port(self):
        pass


class TcpClient(object):

    def __init__(self, manager):
        self._manager = manager
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._reserved_ports = []

    def reserve_port(self) -> int:
        with socket.socket() as s:
            s.bind(('', 0))
            port = s.getsockname()[1]
            if self._reserved_ports.__contains__(port):
                return self.reserve_port()
            else:
                print("[TCP Client]: port " + str(port) + " is reserved")
                return port

    def remove_reserved_port(self, port):
        self._reserved_ports.remove(port)

    def send(self, server_address, port, message):
        server_info = server_address, port
        self._socket.connect(server_info)
        message = message.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self._socket.send(send_length)
        self._socket.send(message)
        print(self._socket.recv(2048).decode(FORMAT))
