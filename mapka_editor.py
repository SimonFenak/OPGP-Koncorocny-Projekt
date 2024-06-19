import json
import pygame
import sys
import os


class dekoracia:
    def __init__(self,nazov,osa_x,osa_y,velkost_x,velkost_y):
        self.nazov=nazov
        self.osa_x=osa_x
        self.osa_y = osa_y
        self.velkost_x = velkost_x
        self.velkost_y = velkost_y

dekoracie=[]

# Načítanie mapy z JSON
def load_map_from_json(filename):
    global dekoracie
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        dekoraciiii=data['map'][1]
        for i in dekoraciiii:
            dekoracie.append(dekoracia(nazov=i[0],osa_x=i[1]/ 5 * 3,osa_y=i[2]/ 5 * 3,velkost_x=i[3],velkost_y=i[4]))
        print("Načítané údaje z JSON:", data)  # Diagnostický výstup
        return data['map'][0]


# Uloženie mapy do JSON
def save_map_to_json(filename, map_data):
    global dekoracie
    with open(filename, 'w', encoding='utf-8') as file:
        skusaj=[]
        for i in dekoracie:
            skusaj.append([i.nazov,i.osa_x* 5  /3,i.osa_y* 5  /3,i.velkost_x,i.velkost_y])
        data = {'map': [map_data,skusaj]}
        json.dump(data, file, ensure_ascii=False, indent=4)


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
aktualnamapa = 'map_level.json'
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
aktivny_obr=None
img1 = pygame.image.load('bloky/stone.png')
img1 = pygame.transform.scale(img1, (block_width, block_height))
img2 = pygame.image.load('bloky/door.png')
img2 = pygame.transform.scale(img2, (block_width, block_height))
img3 = pygame.image.load('bloky/trap.png')
img3 = pygame.transform.scale(img3, (block_width, block_height))
pocet = 1
running = True
# Získaj cestu k adresáru "bloky"
cesta_k_priecinku = 'bloky/'
cesta_k_priecinku_dec = 'decorations/'
# Získaj všetky názvy súborov v adresári
nazvy_suborov = os.listdir(cesta_k_priecinku)
nazvy_suborov_dec = os.listdir(cesta_k_priecinku_dec)
over=False
# Vytvor prázdny zoznam pre ukladanie názvov súborov
nazvy_suborov_v_priecinku = []
nazvy_suborov_v_priecinku_dec = []

# Prejdi cez každý názov súboru a pridaj ho do zoznamu
for subor in nazvy_suborov:
    nazvy_suborov_v_priecinku.append(subor)
for subor in nazvy_suborov_dec:
    nazvy_suborov_v_priecinku_dec.append(subor)

# Vypíš názvy súborov
print(nazvy_suborov_v_priecinku)
ahoj=dekoracia(nazov=nazvy_suborov_v_priecinku_dec[0],osa_x=screen_width/2,osa_y=screen_height/2,velkost_x=block_width,velkost_y=block_height/2)
print(ahoj.nazov+'nihhaa')
def draw_map(map_data):
    for y, row in enumerate(map_data):
        for x, char in enumerate(row):
            if char == 'S':
                screen.blit(img, (x * block_width, y * block_height))
            elif char == 'D':
                screen.blit(img2, (x * block_width, y * block_height))
            elif char == 'T':
                screen.blit(img3, (x * block_width, y * block_height))
            else:
                screen.blit(img1, (x * block_width, y * block_height))


def draw_decoration_menu():
    global dec_obrazok,dekoracie
    for i in range(len(nazvy_suborov_v_priecinku_dec)):
        dec_obrazok = pygame.image.load('decorations/' + nazvy_suborov_v_priecinku_dec[i])
        dec_obrazok = pygame.transform.scale(dec_obrazok, (block_width * 2, block_height * 2))
        screen.blit(dec_obrazok, (block_width * 2 * i, screen_height))
    if dekoracie:
        for i in dekoracie:
            dec_obrazok = pygame.image.load('decorations/' + i.nazov)
            dec_obrazok = pygame.transform.scale(dec_obrazok, (i.velkost_x, i.velkost_y))
            screen.blit(dec_obrazok, (i.osa_x, i.osa_y))
def handle_decoration_menu_click(mouse_pos):
    global dec_obrazok
    for i in range(len(nazvy_suborov_v_priecinku_dec)):
        obrazok_rect = pygame.Rect(block_width * 2 * i, screen_height, block_width * 2, block_height * 2)
        if obrazok_rect.collidepoint(mouse_pos):
            print("Klikol si na obrazok", nazvy_suborov_v_priecinku_dec[i])
            dekoracie.append(dekoracia(nazov=nazvy_suborov_v_priecinku_dec[i],osa_x=screen_width* 5/3/2,osa_y=screen_height* 5/ 3/2,velkost_x=block_width,velkost_y=block_height))
def handle_decoration_click(mouse_pos):
    global dekoracie,aktivny_obr,over
    for i in range(len(dekoracie)):
        obrazok_rect = pygame.Rect(dekoracie[i].osa_x, dekoracie[i].osa_y, dekoracie[i].velkost_x, dekoracie[i].velkost_y )
        if over:
            aktivny_obr = None
            over = False
            save_map_to_json(aktualnamapa, map_data)
            return
        if obrazok_rect.collidepoint(mouse_pos):
            aktivny_obr=i
            over=True
            save_map_to_json(aktualnamapa, map_data)
            return
def draw_menu():
    global menime, menimena, input_text
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
    input_box_rect = pygame.Rect(text_rect.left - 150, text_rect.top - 40, 200, 30)
    pygame.draw.rect(screen, (255, 255, 255), input_box_rect)
    pygame.draw.rect(screen, (0, 0, 0), input_box_rect, 2)

    input_surface = font.render(input_text, True, (0, 0, 0))
    screen.blit(input_surface, (input_box_rect.x + 5, input_box_rect.y + 5))


def handle_menu_click(mouse_pos):
    global menime, menimena, input_text
    block_x = mouse_pos[0] // block_width
    block_y = mouse_pos[1] // block_height
    try:
        print(map_data[int(block_y)][int(block_x)])
        menime[0], menime[1] = int(block_y), int(block_x)
        zmena()
    except Exception as e:
        pass

    for i in range(len(nazvy_suborov_v_priecinku)):
        obrazok_rect = pygame.Rect(screen_width + block_width * 2 * i, screen_height, block_width * 2, block_height * 2)
        if obrazok_rect.collidepoint(mouse_pos):
            print("Klikol si na obrazok", nazvy_suborov_v_priecinku[i])
            menimena = nazvy_suborov_v_priecinku[i]

    text_rect = pygame.Rect(screen.get_width() - 20 - 80, screen.get_height() - 20 - 20, 80, 20)
    if text_rect.collidepoint(mouse_pos):
        print("Klikol si na tlačidlo 'new'")
        if input_text:
            create_new_json_file(input_text + '.json')
            input_text = ''  # Clear input text after creating file
def aktivuj_posuvanie(mouse_pos):
    global aktivny_obr,dekoracie
    dec_obrazok = pygame.image.load('decorations/' + dekoracie[aktivny_obr].nazov)
    dec_obrazok = pygame.transform.scale(dec_obrazok, (dekoracie[aktivny_obr].velkost_x, dekoracie[aktivny_obr].velkost_y))
    dekoracie[aktivny_obr].osa_x=mouse_pos[0]
    dekoracie[aktivny_obr].osa_y = mouse_pos[1]
    print(mouse_pos)
    screen.blit(dec_obrazok, (mouse_pos))
def handle_key_down(event):
    global running, input_text
    if event.key == pygame.K_ESCAPE:
        running = False
    elif event.key == pygame.K_BACKSPACE:
        input_text = input_text[:-1]
    else:
        input_text += event.unicode


def zmena():
    global menime, menimena, aktualnamapa  # Deklarujeme globálne premenné
    if menime[0] is not None and menime[1] is not None and menimena:
        if menimena == 'img.png':
            new_char = 'S'
        elif menimena == 'door.png':
            new_char = 'D'
        elif menimena == 'trap.png':
            new_char = 'T'
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
    aktualnamapa = filename
    print(f"Vytvorený nový JSON súbor: {filename}")


# Hlavná slučka

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            handle_decoration_menu_click(mouse_pos)
            handle_decoration_click(mouse_pos)
            handle_menu_click(mouse_pos)
        elif event.type == pygame.KEYDOWN:
            handle_key_down(event)

    draw_map(map_data)
    draw_decoration_menu()
    draw_menu()
    if aktivny_obr!=None:
        aktivuj_posuvanie(pygame.mouse.get_pos())
    pygame.display.flip()

# Ukončenie Pygame
pygame.quit()
sys.exit()
