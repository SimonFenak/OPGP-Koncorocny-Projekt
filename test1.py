# -*- coding: utf-8 -*-
import ast
import json
import pygame
import socket
import sys
class player:
    def __init__(self,block_width,block_height):
        self.player_img = pygame.image.load('player.png')
        self.player_width = block_width
        self.player_height = block_height-5
        self.player_img = pygame.transform.scale(self.player_img, (self.player_width, self.player_height))
        self.player_speed = 1
        self.player_x = 0
        self.player_y = 0
    def zaokruhli(self,block_height):
        nasob=self.player_y/block_height
        self.player_y=round(nasob)*block_height+5

class dekoracia:
    def __init__(self,nazov,osa_x,osa_y,velkost_x,velkost_y):
        self.nazov=nazov
        self.osa_x=osa_x
        self.osa_y = osa_y
        self.velkost_x = velkost_x
        self.velkost_y = velkost_y
# Načítanie JSON dát zo súboru
with open('map_data.json', 'r', encoding='utf-8') as file:
    level_data = json.load(file)
dekoralist=level_data['map'][1]
dekoracie=[]


# Spracovanie mapy
map_data = level_data['map'][0]

# Inicializácia Pygame
pygame.init()

# Nastavenie obrazovky
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))

# Rozmery mapy
rows = len(map_data)
cols = len(map_data[0])

# Vypočítanie veľkosti bloku
block_width = screen_width // cols
block_height = screen_height // rows
for i in dekoralist:
    dekoracie.append(dekoracia(nazov=i[0],osa_x=i[1],osa_y=i[2],velkost_x=block_width,velkost_y=block_height))
def draw_dec():
    global dekoracie
    if dekoracie:
        for i in dekoracie:
            dec_obrazok = pygame.image.load('decorations/' + i.nazov)
            dec_obrazok = pygame.transform.scale(dec_obrazok, (i.velkost_x, i.velkost_y))
            screen.blit(dec_obrazok, (i.osa_x, i.osa_y))

# Načítanie obrázkov a zmena ich veľkosti
img = pygame.image.load('bloky/img.png')
img = pygame.transform.scale(img, (block_width, block_height))

img1 = pygame.image.load('bloky/img_1.png')
img1 = pygame.transform.scale(img1, (block_width, block_height))

img2 = pygame.image.load('bloky/door.png')
img2 = pygame.transform.scale(img2, (block_width, block_height))
img3 = pygame.image.load('bloky/trap.png')
img3 = pygame.transform.scale(img3, (block_width, block_height))

# Nastavenia klienta
server_address = ('localhost', 12345)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Hráčova pozícia
playeris = player(block_width, block_height)
player2 = player(block_width, block_height)
for y, row in enumerate(map_data):
    for x, char in enumerate(row):
        if char == 'U':
            playeris.player_x = x * block_width
            playeris.player_y = y * block_height+5
            break
    else:
        continue
    break

for y, row in enumerate(map_data):
    for x, char in enumerate(row):
        if char == 'Z':
            player2.player_x = x * block_width
            player2.player_y = y * block_height+5
            break
    else:
        continue
    break

player_jump = False
jump_count = 10
gravity = 1
skak=True

# Funkcia na vykreslenie mapy
def draw_map():
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

# Funkcia na detekciu kolízií
def check_collision(player_rect):
    global MAPP
    for y, row in enumerate(map_data):
        for x, char in enumerate(row):
            if char == 'S':
                block_rect = pygame.Rect(x * block_width, y * block_height, block_width, block_height)
                if player_rect.colliderect(block_rect):
                    return True
            elif char == 'D':
                print("koneeeeeeeec")
                MAPP='idemre.json'
            elif char == 'T':
                print("skaaaaaaaaap")
                MAPP = 'map_data.json'
    return False

# Hlavná slučka
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE and not player_jump:
                player_jump = True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        playeris.player_x -= playeris.player_speed
        if check_collision(pygame.Rect(playeris.player_x, playeris.player_y, playeris.player_width, playeris.player_height)):
            playeris.player_x += playeris.player_speed
    if keys[pygame.K_RIGHT]:
        playeris.player_x += playeris.player_speed
        if check_collision(pygame.Rect(playeris.player_x, playeris.player_y, playeris.player_width, playeris.player_height)):
            playeris.player_x -= playeris.player_speed
    if not check_collision(pygame.Rect(playeris.player_x, playeris.player_y + playeris.player_speed, playeris.player_width, playeris.player_height)):
        playeris.player_y += playeris.player_speed


    # Kontrola, aby sa hráč nepresunul mimo obrazovky
    if playeris.player_x < 0:
        playeris.player_x = 0
    elif playeris.player_x + playeris.player_width > screen_width:
        playeris.player_x = screen_width - playeris.player_width

    if player_jump:
        if jump_count >= -10:
            neg = 0.1
            if jump_count <= 0:
                neg = -0.1
            playeris.player_y -= (jump_count ** 2) * 0.5 * neg  # Zmena: Ešte pomalšie skoky
            if check_collision(pygame.Rect(playeris.player_x, playeris.player_y, playeris.player_width, playeris.player_height)) and skak==True :
                playeris.player_y += (jump_count ** 2) * 0.5 * neg
                jump_count=0
                skak=False
                neg = -0.1
            if skak==False:
                neg = -0.1
                if check_collision(pygame.Rect(playeris.player_x, playeris.player_y, playeris.player_width, playeris.player_height)):
                    player_jump = False
                    playeris.zaokruhli(block_height)
                    skak = True
                    neg = 0.1
                    jump_count = 10

            jump_count -= 0.1
        if jump_count  <= -10:
            player_jump = False
            playeris.zaokruhli(block_height)
            skak=True
            neg = 0.1
            jump_count = 10
    # Kontrola, aby sa hráč nepresunul mimo mapy
    if playeris.player_y < 0:
        playeris.player_y = 0
    elif playeris.player_y + playeris.player_height > screen_height:
        playeris.player_y = screen_height - playeris.player_height

    player_position = str(playeris.player_x)+"."+str(playeris.player_y)
    # Odošleme pozíciu modrej kocky na server
    client_socket.sendto(player_position.encode(), server_address)

    # Prijatie údajov od servera o pozícii červenej kocky
    data, _ = client_socket.recvfrom(1024)
    player2_position = data.decode()
    player2_position=str(player2_position).split(".")
    player2.player_x=int(player2_position[0])
    player2.player_y=int(player2_position[1])

    screen.fill((0, 0, 0))
    draw_map()
    draw_dec()
    screen.blit(playeris.player_img, (playeris.player_x, playeris.player_y))
    screen.blit(player2.player_img, (player2.player_x, player2.player_y))
    pygame.display.flip()

# Ukončenie Pygame
pygame.quit()
sys.exit()
