import socket

# Nastavenia servera
server_address = ('localhost', 12345)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_address)
print('Server je pripravený prijímať spojenie')

# Slovník pre uchovanie adries klientov a farieb ich kociek
clients = {}

# Hlavný cyklus servera
while True:
    data, address = server_socket.recvfrom(1024)
    print(f"Prijaté dáta od klienta {address}: {data.decode()}")  # Vypíšeme prijaté údaje

    # Ak klient ešte nie je v slovníku, pridáme ho spolu s farbou jeho kocky
    if address not in clients:
        if len(clients) == 0:
            clients[address] = 'blue'
        elif len(clients) == 1:
            clients[address] = 'red'

    # Rozoslanie prijatých údajov všetkým klientom, ktorí nie sú odosielateľom
    for client_address in clients:
        if client_address != address:
            server_socket.sendto(data, client_address)
