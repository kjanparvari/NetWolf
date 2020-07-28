import threading
import socket

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


class TcpServer(object):

    def __init__(self):
        server_address = socket.gethostbyname(socket.gethostname()),
        self._server_info = (server_address, PORT)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(self._server_info)
        self._thread = threading.Thread(target=self._setup())
        self._thread.start()

    def _setup(self):
        print("[STARTING] server is starting...")
        self._start()

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

    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, server_address, message):
        server_info = server_address, PORT
        self._socket.connect(server_info)
        message = message.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self._socket.send(send_length)
        self._socket.send(message)
        print(self._socket.recv(2048).decode(FORMAT))
