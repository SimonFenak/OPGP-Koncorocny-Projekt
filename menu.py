import pygame
import sys

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


def main_menu():
    while True:
        win.blit(background_image, (0, 0))

        draw_text_with_outline('PrisonBreak', font, GREEN, BLUE, win, WIDTH // 2, HEIGHT // 4)

        # Draw buttons
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
        button_2 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 75, 200, 50)

        win.blit(button_image, (WIDTH // 2 - 100, HEIGHT // 2 - 25))
        win.blit(button_image, (WIDTH // 2 - 100, HEIGHT // 2 + 75))

        draw_text('Start', small_font, WHITE, win, WIDTH // 2, HEIGHT // 2)
        draw_text('Quit', small_font, WHITE, win, WIDTH // 2, HEIGHT // 2 + 100)

        if button_1.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0]:
                game()
        if button_2.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0]:
                pygame.quit()
                sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def game():
    # Placeholder for the game loop, currently just exits to menu
    main_menu()


main_menu()