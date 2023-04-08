import pygame
import game
import menus

# Set caption and logo
pygame.display.set_caption("The Snake Game")
icon = pygame.image.load("snake.png")
pygame.display.set_icon(icon)

main_menu = menus.main_menu
snake_game = game.game

running = True
playing = False

pygame.init()

while running:
    playing = main_menu()
    playing = snake_game()

    