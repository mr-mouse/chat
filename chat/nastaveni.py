from tkinter import *

class config:
    def __init__(self):
        self.root = Tk()

        self.config()
        self.set()

        self.root.mainloop()

    def config(self):

        self.root.geometry("325x181+607+199")
        self.root.title("Sanachat nastavení")



        self.Entry1 = Entry(self.root)
        self.Entry1.place(relx=0.4, rely=0.11,height=23, relwidth=0.51)
        self.Entry1.configure(background="white")
        self.Entry1.configure(font="TkFixedFont")

        self.Entry2 = Entry(self.root)
        self.Entry2.place(relx=0.4, rely=0.33,height=23, relwidth=0.51)
        self.Entry2.configure(background="white")
        self.Entry2.configure(font="TkFixedFont")

        self.Entry3 = Entry(self.root)
        self.Entry3.place(relx=0.4, rely=0.55,height=23, relwidth=0.51)
        self.Entry3.configure(background="white")
        self.Entry3.configure(font="TkFixedFont")

        self.Label1 = Label(self.root)
        self.Label1.place(relx=0.06, rely=0.55, height=21, width=96)
        self.Label1.configure(text='''PORT serveru:''')

        self.Label2 = Label(self.root)
        self.Label2.place(relx=0.18, rely=0.11, height=21, width=49)
        self.Label2.configure(text='''Jméno:''')

        self.Label3 = Label(self.root)
        self.Label3.place(relx=0.12, rely=0.33, height=21, width=73)
        self.Label3.configure(text='''IP serveru:''')

        self.Button1 = Button(self.root)
        self.Button1.place(relx=0.71, rely=0.77, height=29, width=64)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(text='''Uložit''')
        self.Button1.configure(command=self.save)

    def set(self):
        with open("config.txt", "r") as f:
            data = f.read().split("\n")
        self.Entry1.insert(END, data[0])
        self.Entry2.insert(END, data[1])
        self.Entry3.insert(END, data[2])

    def save(self):
        data = self.Entry1.get() + "\n" + self.Entry2.get() + "\n" + self.Entry3.get()
        with open("config.txt", "w")as f:
            f.write(data)
        self.root.destroy()

config()
