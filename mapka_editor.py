import json
import pygame
import sys
import os

class skusam():
    def __init__(self):
        self.menime = [None, None]
        self.menimena = ''

# Načítanie mapy z JSON
def load_map_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        print("Načítané údaje z JSON:", data)  # Diagnostický výstup
        return data['map'][0]

# Uloženie mapy do JSON
def save_map_to_json(filename, map_data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump({'map': [map_data]}, file, ensure_ascii=False, indent=4)

# Inicializácia Pygame
pygame.init()
menime = [None, None]
menimena = ''

# Nastavenie obrazovky
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# Rozmery mapy
map_data = load_map_from_json('map_data.json')
print("Načítaná mapa:", map_data)  # Diagnostický výstup

rows = len(map_data)
cols = len(map_data[0])
screen_width = (screen_width / 5) * 3
screen_height = (screen_height / 5) * 3
block_width = screen_width // cols
block_height = screen_height // rows

# Načítanie obrázkov a zmena ich veľkosti
img = pygame.image.load('bloky/img.png')
img = pygame.transform.scale(img, (block_width, block_height))

img1 = pygame.image.load('bloky/img_1.png')
img1 = pygame.transform.scale(img1, (block_width, block_height))
pocet = 1
running = True
# Získaj cestu k adresáru "bloky"
cesta_k_priecinku = 'bloky/'

# Získaj všetky názvy súborov v adresári
nazvy_suborov = os.listdir(cesta_k_priecinku)

# Vytvor prázdny zoznam pre ukladanie názvov súborov
nazvy_suborov_v_priecinku = []

# Prejdi cez každý názov súboru a pridaj ho do zoznamu
for subor in nazvy_suborov:
    nazvy_suborov_v_priecinku.append(subor)

# Vypíš názvy súborov
print(nazvy_suborov_v_priecinku)

def draw_map(map_data):
    for y, row in enumerate(map_data):
        for x, char in enumerate(row):
            if char == 'S':
                screen.blit(img, (x * block_width, y * block_height))
            else:
                screen.blit(img1, (x * block_width, y * block_height))

def draw_menu():
    global running
    global menime, menimena  # Deklarujeme globálne premenné
    for i in range(len(nazvy_suborov_v_priecinku)):
        obrazok = pygame.image.load('bloky/' + nazvy_suborov_v_priecinku[i])
        obrazok = pygame.transform.scale(obrazok, (block_width*2, block_height*2))
        screen.blit(obrazok, (screen_width + block_width * 2 * i, screen_height))

    for event in pygame.event.get():  # Pridané, aby bolo možné spracovať udalosť MOUSEBUTTONDOWN
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            block_x = mouse_pos[0] // block_width
            block_y = mouse_pos[1] // block_height
            try:
                print(map_data[int(block_y)][int(block_x)])
                menime[0], menime[1] = int(block_y), int(block_x)
                zmena()
            except Exception as e:
                print("Chyba pri prístupe k map_data:", e)  # Diagnostický výstup
                pass
            for i in range(len(nazvy_suborov_v_priecinku)):
                obrazok_rect = obrazok.get_rect(topleft=(screen_width + block_width * 2 * i, screen_height))
                if obrazok_rect.collidepoint(mouse_pos):
                    print("Klikol si na obrazok", nazvy_suborov_v_priecinku[i])
                    menimena = nazvy_suborov_v_priecinku[i]
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

def zmena():
    global menime, menimena  # Deklarujeme globálne premenné
    if menime[0] is not None and menime[1] is not None and menimena:
        if menimena == 'img.png':
            new_char = 'S'
        else:
            new_char = 'X'

        # Zmena znaku v reťazci
        row = map_data[menime[0]]
        map_data[menime[0]] = row[:menime[1]] + new_char + row[menime[1] + 1:]
        save_map_to_json('map_data.json', map_data)
        print(f"Zmenili sme znak na pozícii ({menime[0]}, {menime[1]}) na '{new_char}' a uložili do súboru")
        menime[0], menime[1] = None, None

# Hlavná slučka

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    draw_map(map_data)
    draw_menu()
    pygame.display.flip()

# Ukončenie Pygame
pygame.quit()
sys.exit()
