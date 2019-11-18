import socket
from threading import Thread
import sqlite3
import time
from clases import *


class Connection(Thread):
    conn: socket.socket

    def __init__(self, conn, adr, cls):
        super().__init__()
        self.conn, self.adr = conn, adr
        self.logined = False
        self.cls = cls
        self.cls.attempts[self.adr[0]] = 3
        self.send('Введите логин и пароль')

    def run(self):
        while 1:
            try:
                data = self.conn.recv(1024).decode('utf-8')
                if not self.logined:
                    if self.login(data) is False:
                        break
                else:
                    self.send(self.user.execute(data, self))
            except Exception as f:
                print(f)
                self.close_connection()
                break
            time.sleep(0.02)

    def login(self, data):
        params = data.split()
        if len(params[:2]) == 2:
            res = self.cls.sql.execute(f'SELECT * FROM users'
                                       f' WHERE login = "{params[0]}" '
                                       f'AND password = "{params[1]}"'
                                       ).fetchone()
            if res is not None:
                del self.cls.attempts[self.adr[0]]
                self.user = eval(f'{res[-2]}("{res[1]}", "{self.adr[0]}", "{res[-1]}")')
                self.send(f'Вы вошли как {res[-2]}\nВведите ? для списка команд')
                self.logined = True
            else:
                self.cls.attempts[self.adr[0]] -= 1
                a = self.cls.attempts[self.adr[0]]
                self.send('Неправильный логин или пароль\nОсталось попыток ' + str(a) if a else 'Вы заблокированы на 5 минут')
                if not self.cls.attempts[self.adr[0]]:
                    self.close_connection()
                    self.cls.timed.add(self.adr[0])
                    time.sleep(600)
                    self.cls.timed.remove(self.adr[0])
                    return False

    def send(self, msg):
        self.conn.send(str(msg).encode('utf-8'))

    def close_connection(self):
        self.conn.close()
        self.cls.connections.remove(self)
        if self.logined:
            self.cls.sql.execute(f'UPDATE users SET times = "{self.user.end()}" WHERE login = "{self.user.login}"')
            self.cls.sql.commit()

    def __repr__(self):
        return f'{self.adr[0]}:{self.adr[1]}'


class Program:

    def __init__(self, port):
        self.socket = socket.socket()
        self.socket.bind(("", port))
        self.socket.listen(10)
        self.connections = []
        self.timed = set()
        self.attempts = {}
        self.sql = sqlite3.connect('users.db', check_same_thread=False)

    def run(self):
        while 1:
            conn, adr = self.socket.accept()
            try:
                if adr[0] not in self.timed:
                    conn.settimeout(30)
                    self.connections.append(Connection(conn, adr, self))
                    self.connections[-1].start()
                    print(f'Новое соединение: {adr[0]}:{adr[1]} - {time.strftime("%d.%m.%Y %H:%M:%S")}')
                    print('Текущие пользователи:', *self.connections)
                else:
                    conn.close()
            except Exception as f:
                print(f)
            time.sleep(0.02)


a = Program(745)
a.run()