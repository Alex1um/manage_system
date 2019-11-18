import socket
import time

con = socket.socket()
connected = False
con.settimeout(5)
while 1:
    if not connected:
        try:
            ip, port = input('Куда хотите подключиться?(ip:port)\n').split(':')
            con.connect((ip, int(port)))
            connected = True
        except Exception as f:
            print(f)
    try:
        res = con.recv(1024).decode('utf-8')
        if not res:
            raise ConnectionRefusedError('Сервер разорвал соединение')
        print(res)
        con.send(input().encode('utf-8'))
    except Exception as f:
        con = socket.socket()
        connected = False
        print(f)
    time.sleep(0.02)