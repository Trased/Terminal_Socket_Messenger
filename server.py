import socket
import threading
import select

socket_list = {}
socket_connection = {}
name_list = {}
name_change = False
def comm_thread(conn, key, value):
    while 1:
        while 1:
            # Asteapta data, buffer de 1024 octeti
            ready, _, _ = select.select([conn], [], [], 0)
            if(ready):
                data = conn.recv(1024)
                # Daca functia recv returneaza None, clientul a inchis conexiunea
                if not data:
                    break
                if data.startswith(bytes('--Name=', encoding = "ascii")):
                    name_list[value] = data[7:].decode('utf8')
                    data = "Ti-ai schimbat numele."
                    conn.sendall(bytes(data, encoding = "ascii"))
                    break

                # Trimite datele receptionate
                for other_value in socket_connection.keys():
                    if other_value != value:
                        socket_connection[other_value].sendall(bytes(name_list[value] + ': ' + data.decode('utf8'), encoding="ascii"))

    conn.close()

# Creaza un socket IPv4, TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Asociere la adresa locala, portul 5000
s.bind(('127.0.0.1', 5000))
# Coada de asteptare pentru conexiuni de lungime 1
s.listen(5)
# Asteapta conexiuni
print('Asteapta conexiuni (oprire server cu Ctrl-C)')
while 1:
    try:
        conn, addr = s.accept()
    # La apasarea tastelor Ctrl-C se iese din blucla while 1
    except KeyboardInterrupt:
        break
    print('S-a conectat clientul', addr)
    key, value = addr
    socket_list.setdefault(key, [])
    socket_list[key].append(value)
    socket_connection[value] = conn
    try:
        threading.Thread(target=comm_thread, args=(conn, key, value)).start()
    except:
        print("Eroare la pornirea thread-ului")
