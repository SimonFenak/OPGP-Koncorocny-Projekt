import test1
import test2
import serverUDP
import sys 


def choose_option(option):
    serverUDP.main()
    if option == 1:
        test1.main()
    elif option == 2:
        test2.main()
    elif option == 3:
        return


print("Vitaj v hre PRISON BREAK")
vstup = int(input("Vyber z možností (1 Hráč Dominik) (2 Hráč Šimon) (3 Ukončiť)"))
choose_option(vstup)