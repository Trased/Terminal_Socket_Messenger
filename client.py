import socket
import select
import sys
name = input("Insert your name: ")
# Creaza un socket IPv4, TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conectare la serverul care asculta pe portul 5000
s.connect(('127.0.0.1', 5000))

s.sendall(bytes('--Name=' + str(name), encoding = "ascii"))

while True:
    try:
        while True:
            try:
                ready, _, _ = select.select([sys.stdin], [], [], 0)
                if ready and sys.stdin.read(1) != '':
                    message = input()
                    s.sendall(bytes(message, encoding="ascii"))

                ready_to_read, _, _ = select.select([s], [], [], 0)
                if(ready_to_read):
                    data = s.recv(1024).decode('utf8')
                    print(data)
            except KeyboardInterrupt:
                break
    except KeyboardInterrupt:
        break

# Inchide conexiune
s.close()