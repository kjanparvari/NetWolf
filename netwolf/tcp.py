import threading
import socket

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


class TcpServer(object):

    def __init__(self, manager):
        self._manager = manager

    def get_file(self, sender_addr, port, filename):
        f = self._manager.get_file_manager().create_file(filename)
        threading.Thread(target=self._setup, args=(f, port)).start()

    def _setup(self, file, port):
        print(f"[TCP Server] server is starting on port {port}...")
        server_address = socket.gethostbyname(socket.gethostname())
        self._server_info = (server_address, port)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(self._server_info)
        self._start(file)

    @staticmethod
    def _handle_client(conn, addr, file=None):
        print(f"[TCP Server]: New connection from {addr} ")
        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                else:
                    file.write(msg)
                file.close()
                print(f"[{addr}] {msg}")
                conn.send("[TCP]: File transmission was successfull".encode(FORMAT))
        conn.close()

    def _start(self, file):
        self._socket.listen()
        print(f"[TCP Server]: Server is listening on {self._server_info[0]}")
        while True:
            conn, addr = self._socket.accept()
            threading.Thread(target=self._handle_client, args=(conn, addr, file)).start()


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

    def send_file(self, dest_addr, port, filename):
        f = self._manager.get_file_manager().get_file(filename)
        threading.Thread(target=self._send, args=(dest_addr, port, f)).start()

    def _send(self, server_address, port, file):
        server_info = server_address, port
        message = file.read()
        self._socket.connect(server_info)
        message = message.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self._socket.send(send_length)
        self._socket.send(message)
        print(self._socket.recv(2048).decode(FORMAT))

        message = DISCONNECT_MESSAGE.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self._socket.send(send_length)
        self._socket.send(message)
        print(self._socket.recv(2048).decode(FORMAT))

        file.close()
