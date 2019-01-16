#! /usr/bin/env python
from tkinter import *
from threading import Thread
import socket
from tkinter.scrolledtext import ScrolledText
import platform
import os
import auth
import pickle
import time

class chat:
    def __init__(self):
        self.error = False
        self.get_config()
        try:
            user_login = auth.auth_client("192.168.1.111", 12345)
        except:
            self.error_handler("","Nelze se připojit k účovému serveru")

        status = user_login.gui()
        if not status:
            self.error_handler("","Špatné jméno nebo heslo!")

        self.run()
        self.kill()

    def kill(self):
        if platform.system() == "Linux":
            os.system("kill " + str(os.getpid()))
        elif platform.system() == "Windows":
            os.system("taskkill /F /PID " + str(os.getpid()))

    def init_tk(self):
        self.root = Tk()

    def run(self):
        self.connect()
        self.init_tk()
        self.gui(self.root)

        t1 = Thread(target=self.recv)
        t1.start()
        self.root.mainloop()

    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.ip, self.port))
        except Exception as e:
            err_text = "Chyba při připojování k serveru. Zkuste prosím znovu později."
            self.error_handler(e, err_text)

        time.sleep(0.1)
        self.s.send(pickle.dumps([self.name]))

    def get_config(self):
        with open("config.txt", "r") as f:
            data = f.read().split("\n")
        self.name = data[0]
        self.ip = data[1]
        self.port = int(data[2])

    def keypress(self, key):
        try:
            if ord(key.char) == 13:
                self.send()
        except:
            pass

    def send(self):
        text = self.Entry1.get()
        self.Entry1.delete(0, 'end')
        try:
            self.s.send(text.encode())
        except Exception as e:
            err_text = "Chyba při připojování k serveru. Zkuste prosím znovu později."
            self.error_handler(e, err_text)

    def recv(self):
        while(True):
            text = self.s.recv(4096).decode()
            self.Text1.configure(state=NORMAL)
            self.Text1.insert(END, text + '\n')
            self.Text1.see(END)
            self.Text1.configure(state=DISABLED)

    def gui(self, top=None):

        top.geometry("459x370+397+209")
        top.title("SanaChat")
        top.bind('<KeyPress>', self.keypress)

        self.Frame1 = Frame(top)
        self.Frame1.place(relx=0.02, rely=0.03, relheight=0.77, relwidth=0.95)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(width=435)

        self.Text1 = ScrolledText(self.Frame1)
        self.Text1.place(relx=0.02, rely=0.04, relheight=0.93, relwidth=0.96)
        self.Text1.configure(background="white")
        self.Text1.configure(font="TkTextFont")
        self.Text1.configure(selectbackground="#c4c4c4")
        self.Text1.configure(width=416)
        self.Text1.configure(wrap=WORD)
        self.Text1.configure(state=DISABLED)

        self.Frame2 = Frame(top)
        self.Frame2.place(relx=0.02, rely=0.81, relheight=0.18, relwidth=0.95)
        self.Frame2.configure(relief=GROOVE)
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief=GROOVE)
        self.Frame2.configure(width=435)

        self.Entry1 = Entry(self.Frame2)
        self.Entry1.place(relx=0.02, rely=0.15,height=43, relwidth=0.82)
        self.Entry1.configure(background="white")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(width=356)

        self.Button1 = Button(self.Frame2)
        self.Button1.place(relx=0.85, rely=0.15, height=49, width=59)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(text='''Odeslat''')
        self.Button1.configure(width=59)
        self.Button1.configure(command=self.send)

    def error_handler(self, e, text):
        self.error = True
        self.err_tk = Tk()
        self.err_tk.title("Chyba!")
        err_text = text + "\n\n" + str(e)
        w = Label(self.err_tk, text=err_text).pack()
        try:
            self.root.destroy()
        except:
            pass
        self.err_tk.mainloop()
        exit(0)

if __name__ == '__main__':
    chat()
