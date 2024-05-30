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
input_text = ''  # Initialize input text

# Nastavenie obrazovky
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
aktualnamapa='novamapa.json'
# Rozmery mapy
map_data = load_map_from_json(aktualnamapa)
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
    global running, input_text
    global menime, menimena  # Deklarujeme globálne premenné
    for i in range(len(nazvy_suborov_v_priecinku)):
        obrazok = pygame.image.load('bloky/' + nazvy_suborov_v_priecinku[i])
        obrazok = pygame.transform.scale(obrazok, (block_width * 2, block_height * 2))
        screen.blit(obrazok, (screen_width + block_width * 2 * i, screen_height))

    # Draw the "new" button
    font = pygame.font.Font(None, 36)
    text = font.render('New', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.bottomright = (screen.get_width() - 20, screen.get_height() - 20)
    pygame.draw.rect(screen, (0, 128, 0), text_rect.inflate(20, 10))
    screen.blit(text, text_rect)

    # Draw the input field
    input_box_rect = pygame.Rect(text_rect.left-150, text_rect.top - 40, 200, 30)
    pygame.draw.rect(screen, (255, 255, 255), input_box_rect)
    pygame.draw.rect(screen, (0, 0, 0), input_box_rect, 2)

    input_surface = font.render(input_text, True, (0, 0, 0))
    screen.blit(input_surface, (input_box_rect.x + 5, input_box_rect.y + 5))

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

            if text_rect.collidepoint(mouse_pos):
                print("Klikol si na tlačidlo 'new'")
                if input_text:
                    create_new_json_file(input_text + '.json')
                    input_text = ''  # Clear input text after creating file

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode


def zmena():
    global menime, menimena ,aktualnamapa # Deklarujeme globálne premenné
    if menime[0] is not None and menime[1] is not None and menimena:
        if menimena == 'img.png':
            new_char = 'S'
        else:
            new_char = 'X'

        # Zmena znaku v reťazci
        row = map_data[menime[0]]
        map_data[menime[0]] = row[:menime[1]] + new_char + row[menime[1] + 1:]
        save_map_to_json(aktualnamapa, map_data)
        print(f"Zmenili sme znak na pozícii ({menime[0]}, {menime[1]}) na '{new_char}' a uložili do súboru")
        menime[0], menime[1] = None, None


def create_new_json_file(filename):
    global aktualnamapa
    # Create a map filled with zeros
    new_map_data = [
        "000000000000000000000000000000000000000000",
        "000000000000000000000000000000000000000000",
        "000000000000000000000000000000000000000000",
        "000000000000000000000000000000000000000000",
        "000000000000000000000000000000000000000000",
        "000000000000000000000000000000000000000000",
        "000000000000000000000000000000000000000000",
        "000000000000000000000000000000000000000000",
        "000000000000000000000000000000000000000000",
        "000000000000000000000000000000000000000000",
        "000000000000000000000000000000000000000000",
        "000000000000000000000000000000000000000000",
        "000000000000000000000000000000000000000000",
        "000000000000000000000000000000000000000000",
        "000000000000000000000000000000000000000000",
        "000000000000000000000000000000000000000000"
    ]
    save_map_to_json(filename, new_map_data)
    aktualnamapa=filename
    print(f"Vytvorený nový JSON súbor: {filename}")


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
