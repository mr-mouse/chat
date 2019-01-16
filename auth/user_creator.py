import auth_client

name = input("Jméno > ")
passw = input("Heslo > ")

hash = auth_client.auth_client(1, 1).get_hash(passw)

with open("client.list", "a+") as f:
    data = f.read()
    out = "\n" + data + name + "," + hash
    f.write(out)
