import socket
import threading
import pickle
from datetime import datetime

class server:
    def __init__(self):
        self.users = []
        self.name_list = []

        self.load_cfg()
        self.init_socket()
        self.run()

    def load_cfg(self):
        with open("server_cfg.txt", "r", ) as f:
            conf = f.read().split("\n")
            self.ip = conf[0]
            self.port = int(conf[1])
            self.max_users = int(conf[2])
            f.close()

    def init_socket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.ip, self.port))
        self.s.listen(self.max_users)

    def handle_tcp(self, sock, addr):
        conf = pickle.loads(sock.recv(1024))
        name = conf[0]
        self.name_list.append(name)

        self.send_all((name + " se připojil").encode())

        with open("history.txt", "r") as f:
            sock.send(f.read().encode())
            f.close()

        self.log_add("connection from: " + str(addr) +" - " + name)
        sock.send("\n\n                         Vítej v chatroom!\n\n".encode())
        while True:
            try:
                data = sock.recv(1024).decode()
            except:
                break
            if data == "":
                break

            info = "[" + datetime.now().strftime('%H:%M:%S') + " " + name + "] "
            processed = info + data
            if data[0] != "/":
                print(info + data)
                self.log_add(info + data)
                self.send_all((info + data).encode())

            elif data[0] == "/":
                splitd = data.split(" ")
                if splitd[0] == "/msg":
                    namesend = splitd[1]
                    sep = " "
                    data = sep.join(splitd[2:])
                    loop = 0
                    for listname in self.name_list:
                        if splitd[1] == listname:
                            self.users[loop].send((info + data).encode())
                        loop += 1
        self.log_add(str(addr) +" - " + name + " has disconnected")
        self.send_all((name + " se odpojil").encode())

    def send_all(self, data):
        with open("history.txt", "r") as f:
            hist = f.read().split("\n")
            f.close()

        if len(hist) >= 50:
            hist = hist[1:]
        hist.append(data.decode())
        out = "\n".join(hist)

        with open("history.txt", "w") as f:
            f.write(out)
            f.close()

        loop = 0
        for client in self.users:
            try:
                client.send(data)
            except Exception as e:
                print("chyba v odesilani:", e)
                self.users.remove(client)
                self.name_list.remove(self.name_list[loop])
            loop += 1

    def log_add(self, data):
        with open("log.txt", "r") as f:
            log = f.read() + "\n"
        with open("log.txt", "w") as f:
            f.write(log + data)

    def run(self):
        while True:
            sock, addr = self.s.accept()
            self.users.append(sock)
            t = threading.Thread(target=self.handle_tcp, args=(sock, addr))
            t.start()

server()
