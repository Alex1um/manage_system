import socket
import struct
import time


def receiver(group, port=48666):
    # Look up multicast group address in name server and find out IP version
    addrinfo = socket.getaddrinfo(group, None)[0]
    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
    # Allow multiple copies of this program on one machine
    # (not strictly needed)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(5)
    # Bind it to the port
    s.bind(('', port))

    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
    # Join group
    if addrinfo[0] == socket.AF_INET: # IPv4
        mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # Loop, printing any data we receive
    return s.recvfrom(1500)


con = socket.socket()
connected = False
con.settimeout(5)
while 1:
    if not connected:
        s = input('Куда хотите подключиться?(ip:порт)\n'
                  'Если не знаете одну из частей, замените ее на *\n'
                  'Если не знаете, нажмите Enter\n').replace('*', '')
        s = s.split(':') if ':' in s else s.split()
        port = 48666
        try:
            if len(s) > 1:
                ip, port = s
                if port and ip:
                    con.connect((ip, int(port)))
                    connected = True
                    continue
            port, sender = receiver('225.0.0.250', port=int(port))
            con.connect((sender[0], int(port.decode('utf-8'))))
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