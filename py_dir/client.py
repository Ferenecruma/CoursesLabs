from time import time
import socket


class ClientError(Exception):
    """Base class for exceptions in this module."""
    pass

class Client:
    def __init__(self, host, port, timeout = None):
        self.host = host
        self.port = port
        self.timeout = timeout
        try:
            self.connection = socket.create_connection((self.host, self.port), self.timeout)
        except socket.error:
            raise ClientError()

    def put(self, key, value, timestamp = None):
        timestamp = timestamp or int(time())
        try:
            self.connection.sendall(f"put {key} {value} {timestamp}\n".encode())
        except socket.error:
            raise ClientError()
        self.read_response()

    def get(self, key):
        try:
            self.connection.sendall(f"get {key}\n".encode())
        except socket.error:
            raise ClientError()
        payload = self.read_response()

        data = {}
        if payload == "":
            return data
        try:
            for row in payload.split("\n"):
                key, value, timestamp = row.split()
                if key not in data:
                    data[key] = []
                data[key].append((int(timestamp), float(value)))
        except ValueError:
            raise ClientError()
        for key in data: # sorting data by timestamps
            data[key].sort(key=lambda x: x[0])
        return data

    def read_response(self):
        data = b""
        while not data.endswith(b"\n\n"):
            try:
                data += self.connection.recv(1024)
            except socket.error:
                raise ClientError()

        decoded_data = data.decode()

        status, payload = decoded_data.split("\n", 1)
        payload = payload.strip()

        if status == "error":
            raise ClientError()

        return payload

if __name__ == "__main__":
    client = Client("127.0.0.1", 8888, timeout=5)
    print(client.get("*"))
