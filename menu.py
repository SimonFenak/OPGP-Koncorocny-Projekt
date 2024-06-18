import pygame
import sys
import serverUDP
#import test1
#import test2

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PrisonBreak")

# Set up font
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (108, 144, 139)
BLUE = (0, 0, 0)

# Load images
background_image = pygame.image.load('obrazky/prison_background.jpeg')  # Image of a prison
button_image = pygame.image.load('obrazky/button.png')  # Image for buttons

# Resize images
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
button_image = pygame.transform.scale(button_image, (200, 50))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_text_with_outline(text, font, text_color, outline_color, surface, x, y):
    # Render the outline by drawing text with an offset
    outline_offset = 2
    for dx in [-outline_offset, outline_offset]:
        for dy in [-outline_offset, outline_offset]:
            draw_text(text, font, outline_color, surface, x + dx, y + dy)
    # Draw the main text
    draw_text(text, font, text_color, surface, x, y)

def settings_menu():
    while True:
        win.blit(background_image, (0, 0))

        draw_text_with_outline('Settings', font, GREEN, BLUE, win, WIDTH // 2, HEIGHT // 4)

        # Draw buttons
        mx, my = pygame.mouse.get_pos()

        back_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
        sounds_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)

        win.blit(button_image, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
        win.blit(button_image, (WIDTH // 2 - 100, HEIGHT // 2 - 25))

        draw_text('Back', small_font, WHITE, win, WIDTH // 2, HEIGHT // 2 + 75)
        draw_text('Zvuky', small_font, WHITE, win, WIDTH // 2, HEIGHT // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.collidepoint((mx, my)):
                    return  # Go back to the main menu
                if sounds_button.collidepoint((mx, my)):
                    # Add functionality for the Zvuky button here
                    print("Zvuky button clicked")

        pygame.display.update()


def sub_menu():
    while True:
        win.blit(background_image, (0, 0))

        draw_text_with_outline('PrisonBreak', font, GREEN, BLUE, win, WIDTH // 2, HEIGHT // 4)

        # Draw buttons
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
        button_2 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
        button_3 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 125, 200, 50)

        win.blit(button_image, (WIDTH // 2 - 100, HEIGHT // 2 - 25))
        win.blit(button_image, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
        win.blit(button_image, (WIDTH // 2 - 100, HEIGHT // 2 + 125))

        draw_text('Start Player1', small_font, WHITE, win, WIDTH // 2, HEIGHT // 2)
        draw_text('Start Player 2', small_font, WHITE, win, WIDTH // 2, HEIGHT // 2 + 75)
        draw_text('Quit', small_font, WHITE, win, WIDTH // 2, HEIGHT // 2 + 150)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_1.collidepoint((mx, my)):
                    test1.main()
                if button_2.collidepoint((mx, my)):
                    test2.main()
                if button_3.collidepoint((mx, my)):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def main_menu():
    while True:
        win.blit(background_image, (0, 0))

        draw_text_with_outline('PrisonBreak', font, GREEN, BLUE, win, WIDTH // 2, HEIGHT // 4)

        # Draw buttons
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
        button_2 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
        button_3 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 125, 200, 50)

        win.blit(button_image, (WIDTH // 2 - 100, HEIGHT // 2 - 25))
        win.blit(button_image, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
        win.blit(button_image, (WIDTH // 2 - 100, HEIGHT // 2 + 125))

        draw_text('Start', small_font, WHITE, win, WIDTH // 2, HEIGHT // 2)
        draw_text('Settings', small_font, WHITE, win, WIDTH // 2, HEIGHT // 2 + 75)
        draw_text('Quit', small_font, WHITE, win, WIDTH // 2, HEIGHT // 2 + 150)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_1.collidepoint((mx, my)):
                    serverUDP.main()
                    #sub_menu()
                if button_2.collidepoint((mx, my)):
                    settings_menu()  # Open settings menu
                if button_3.collidepoint((mx, my)):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def game():
    # Placeholder for the game loop, currently just exits to menu
    main_menu()

main_menu()
