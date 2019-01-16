import hashlib
import pickle
import socket
from tkinter import *

class auth_client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.init_socket()

    def init_socket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.ip, self.port))

    def get_hash(self, passw):
        hash = hashlib.sha256(str(passw).encode()).hexdigest()
        return hash

    def login(self, name, passwd):
        list = []
        list.append(str(name))
        list.append(self.get_hash(passwd))

        to_send = pickle.dumps(list)
        self.s.send(to_send)

        self.recived = self.s.recv(1024).decode()
        if self.recived == "True":
            return True
        else:
            return False

    def keypress(self, key):
        try:
            if ord(key.char) == 13:
                self.confirm_buttn()
        except:
            pass

    def gui(self):
        self.top = Tk()
        self.top.geometry("283x129+404+115")
        self.top.title("SanaChat login")
        self.top.configure(highlightcolor="black")
        self.top.bind('<KeyPress>', self.keypress)

        self.Entry1 = Entry(self.top)
        self.Entry1.place(relx=0.35, rely=0.16,height=23, relwidth=0.59)
        self.Entry1.configure(background="white")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(selectbackground="#c4c4c4")

        self.Entry2 = Entry(self.top)
        self.Entry2.place(relx=0.35, rely=0.47,height=23, relwidth=0.59)
        self.Entry2.configure(background="white")
        self.Entry2.configure(font="TkFixedFont")
        self.Entry2.configure(selectbackground="#c4c4c4")
        self.Entry2.configure(show="*")

        self.Label1 = Label(self.top)
        self.Label1.place(relx=0.07, rely=0.16, height=21, width=49)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(text='''Jméno:''')

        self.Label2 = Label(self.top)
        self.Label2.place(relx=0.07, rely=0.47, height=21, width=45)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(text='''Heslo:''')

        self.Button1 = Button(self.top)
        self.Button1.place(relx=0.71, rely=0.7, height=29, width=69)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(text='''Přihlásit''')
        self.Button1.configure(command=self.confirm_buttn)

        self.top.mainloop()
        try:
            if self.recived == "True":
                return True
            else:
                return False
        except:
            pass
    def confirm_buttn(self):
        self.login(self.Entry1.get(), self.Entry2.get())
        self.top.destroy()
