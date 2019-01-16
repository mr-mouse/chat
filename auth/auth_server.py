import socket
import threading
import pickle

class auth:
    def __init__(self):
        self.load_config()
        self.init_socket()

        self.run()

    def load_config(self):
        with open("config.txt", "r") as f:
            data = f.read().split("\n")
            self.ip = data[0]
            self.port = int(data[1])

    def init_socket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.ip, self.port))
        self.s.listen(50)

    def handle_tcp(self, sock, addr):
        print("new connection from: ", addr)
        data = sock.recv(1024)
        list = pickle.loads(data)
        found = False

        f = open("client.list", "r")
        lines = f.readlines()
        f.close()

        for line in lines:
            line_list = line.split(",")
            print(line_list)
            if line_list[0] == list[0]:
                print("name found")
                if line_list[1] == list[1] + "\n":
                    found = True
                    sock.send("True".encode())
                    break
        if not found:
            sock.send("False".encode())

        sock.close()

    def run(self):
        while True:
            sock, addr = self.s.accept()
            t = threading.Thread(target=self.handle_tcp, args=(sock, addr))
            t.start()

auth()
