import socket
def main():
    # Nastavenia servera
    server_address = ('localhost', 12345)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(server_address)
    print('Server je pripravený prijímať spojenie')

    # Slovník pre uchovanie adries klieantov a farieb ich kociek
    clients = {}

    # Hlavný cyklus servera
    while True:
        data, address = server_socket.recvfrom(1024)
        if data.decode() == "client disconnected":
            clients.pop(address)
            for client in clients.keys():
                pass
            server_socket.sendto("spoluhrac odpojeny".encode(), client)
            print("hrac odpojeny")
            continue
        print(f"Prijaté dáta od klienta {address}: {data.decode()}")  # Vypíšeme prijaté údaje

        # Ak klient ešte nie je v slovníku, pridáme ho spolu s farbou jeho kocky
        if address not in clients:
            if len(clients) == 0:
                clients[address] = 'blue'
            elif len(clients) == 1:
                for client in clients.keys():
                    pass
                server_socket.sendto("spoluhrac pripojeny".encode(),client)
                clients[address] = 'red'
            print(f"Pripojil sa: {clients[address]}")

        # Rozoslanie prijatých údajov všetkým klientom, ktorí nie sú odosielateľom
        for client_address in clients:
            if client_address != address:
                server_socket.sendto(data, client_address)
                print(data, client_address)

if __name__ == "__main__":
    main()
