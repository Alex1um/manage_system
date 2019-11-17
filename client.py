import socket

con = socket.socket()
connected = False

while 1:
    if not connected:
        try:
            ip, port = input('Куда хотите подключиться?\n').split(':')
            con.connect((ip, int(port)))
            connected = True
        except Exception as f:
            print(f)
    try:
        print(con.recv(1024).decode('utf-8'))
        con.send(input().encode('utf-8'))
    except Exception as f:
        if Exception == ConnectionAbortedError:
            connected = False
