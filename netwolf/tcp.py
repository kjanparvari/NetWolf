import time
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

    def _handle_client(self, conn, addr, file=None):
        print(f"[TCP Server]: New connection from {addr} ")
        connected = True
        from netwolf.Serialization import decode
        while connected:
            msg_length = str(decode(conn.recv(HEADER)), 'utf-8')
            if msg_length:
                msg_length = int(msg_length)
                print(f"length: {msg_length}")
                msg = decode(conn.recv(msg_length))
                if str(msg, 'utf-8') == DISCONNECT_MESSAGE:
                    connected = False
                else:
                    file.write(msg)
                file.close()
                from netwolf.Serialization import encode
                conn.send(encode(bytes("[TCP]: File transmission was successfull", 'utf-8')))
        print(f"[TCP Server]: Disconnecting from {addr}")
        conn.close()
        self._manager.get_file_manager().receiving_file_finished()
        time.sleep(0.5)
        self._socket.close()

    def _start(self, file):
        self._socket.listen()
        print(f"[TCP Server]: Server is listening on {self._server_info[0]}")
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
        threading.Thread(target=self._send, args=(dest_addr, port, f, filename)).start()

    def _send(self, server_address, port, file, filename):
        print(f"[TCP Client]: sending file{filename} to {server_address} on port {port}")
        from netwolf.Serialization import encode, decode
        server_info = server_address, port
        message = file.read()
        self._socket.connect(server_info)
        message = encode(bytes(message))
        msg_length = len(message)
        send_length = str(msg_length)
        for i in range(0, HEADER - len(str(msg_length))):
            send_length += " "
        # send_length += b' ' * (HEADER - len(send_length))
        send_length = encode(bytes(send_length, 'utf-8'))
        self._socket.send(send_length)
        self._socket.send(message)
        print(str(decode(self._socket.recv(2048))))
        message = encode(bytes(DISCONNECT_MESSAGE, 'utf-8'))
        send_length = str(msg_length)
        for i in range(0, HEADER - len(str(msg_length))):
            send_length += " "
        # send_length += b' ' * (HEADER - len(send_length))
        send_length = encode(bytes(send_length, 'utf-8'))
        self._socket.send(send_length)
        self._socket.send(message)
        print(str(decode(self._socket.recv(2048)), 'utf-8'))
        print(f"[TCP Client]: Disconnecting from {server_address}")
        file.close()
