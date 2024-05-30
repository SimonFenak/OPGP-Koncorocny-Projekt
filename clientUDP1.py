import pygame
import socket
import ast

# Inicializácia Pygame
pygame.init()

# Nastavenia obrazovky
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])

# Pozícia modrej kocky
blue_cube_position = [100, 100]
red_cube_position = [500, 100]


# Nastavenia klienta
server_address = ('localhost', 12345)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Hlavný cyklus klienta
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        blue_cube_position[0] -= 5
    if keys[pygame.K_RIGHT]:
        blue_cube_position[0] += 5
    if keys[pygame.K_UP]:
        blue_cube_position[1] -= 5
    if keys[pygame.K_DOWN]:
        blue_cube_position[1] += 5

    # Odošleme pozíciu modrej kocky na server
    client_socket.sendto(str(blue_cube_position).encode(), server_address)

    # Prijatie údajov od servera o pozícii červenej kocky
    data, _ = client_socket.recvfrom(1024)
    red_cube_position = ast.literal_eval(data.decode())

    # Vykreslenie objektov
    screen.fill((255, 255, 255))  # Vyplnenie obrazovky bielou farbou
    pygame.draw.rect(screen, (0, 0, 255), (blue_cube_position[0], blue_cube_position[1], 50, 50))  # Vykreslenie modrej kocky
    pygame.draw.rect(screen, (255, 0, 0), (red_cube_position[0], red_cube_position[1], 50, 50))  # Vykreslenie červenej kocky
    pygame.display.flip()  # Aktualizácia obrazovky

    clock.tick(30)

pygame.quit()