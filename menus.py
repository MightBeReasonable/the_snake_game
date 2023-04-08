import pygame
import sys
import os

# Set caption and logo
pygame.display.set_caption("The Snake Game")
icon = pygame.image.load("snake.png")
pygame.display.set_icon(icon)

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

running = True
playing = False

class Menu(object):
    def __init__(self):
        self.font_name = 'Ocean_Summer.ttf'
        self.x_cursor = 140
        self.y_cursor = 250
        self.offset_cursor = -100

    def draw_text(self, text, size, x, y, screen):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, (0, 255, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        screen.blit(text_surface, text_rect)
        return text_rect

class Cursor(object):
    def __init__(self, screen):
        self.font_name = 'Ocean_Summer.ttf'
        self.x_cursor = [140]
        self.y_cursor = [250]
        self.offset_cursor = -100
        self.screen = screen

    def draw_text(self, text, size, x, y, screen, color=(0, 255, 0)):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        screen.blit(text_surface, text_rect)
        return text_rect

    def draw_cursor(self, screen):
        x_cursor_previous = self.x_cursor[-1]
        y_cursor_previous = self.y_cursor[-1]

        cursor_rect = self.draw_text('>', 50, self.x_cursor[0], self.y_cursor[0], screen)

        previous_cursor_position = self.draw_text('>', 50, x_cursor_previous, y_cursor_previous, screen)
        
        if len(self.y_cursor) == 2 and self.y_cursor[0] != self.y_cursor[1]:
            pygame.draw.rect(self.screen, (0, 0, 0), previous_cursor_position, 0)

        return cursor_rect
    
    def handle_keys(self):
        events = pygame.event.get()
        if len(events) == 0:
            return
        elif len(events) != 0:
            event = events[-1]
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    new_y_cursor = self.y_cursor[0] - 70
                    if new_y_cursor <= 250:
                        new_y_cursor = 250
                    self.y_cursor.insert(0, new_y_cursor)
                    if len(self.y_cursor) > 2:
                        self.y_cursor.pop()

                elif event.key == pygame.K_DOWN:
                    new_y_cursor = self.y_cursor[0] + 70
                    if new_y_cursor > 390:
                        new_y_cursor = 390
                    self.y_cursor.insert(0, new_y_cursor)
                    if len(self.y_cursor) > 2:
                        self.y_cursor.pop()

                elif event.key == pygame.K_RETURN:
                    if self.y_cursor[0] == 250:
                        global playing
                        playing = True
                    elif self.y_cursor[0] == 320:
                        print("Options")
                    elif self.y_cursor[0] == 390:
                        pygame.quit()
                        sys.exit()


class MainMenu(Menu):
    def __init__(self, screen):
        super().__init__()
        self.title = "The Snake Game"
        self.options = ["New Game", "Options", "Quit"]
        self.y_position = 250
        self.options_text_size = 50
        self.screen = screen
    
    def draw_menu(self):
        # Draw title
        self.draw_text(self.title, 90, 240, 120, self.screen)

        # Draw options
        for option in self.options:
            self.draw_text(option, self.options_text_size, 240, self.y_position, self.screen)
            self.y_position += self.options_text_size+20

class PauseMenu(Menu):
    def __init__(self, screen):
        super().__init__()
        self.title = "Pause"
        self.options = ["Continue", "New Game", "Main Menu", "Quit"]
        self.y_position = 250
        self.options_text_size = 40
        self.screen = screen

    def draw_menu(self):
        # Draw title
        self.draw_text(self.title, 70, 240, 120, self.screen)

        # Draw options
        for option in self.options:
            self.draw_text(option, self.options_text_size, 240, self.y_position, self.screen)
            self.y_position += self.options_text_size+20

    pass

class GameEndMenu(Menu):
    pass

class Options(Menu):
    pass

def main_menu():
    global playing
    playing = False

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    screen.fill((0, 0, 0))
    cursor = Cursor(screen)
    cursor.draw_cursor(screen)

    while running:
        clock.tick(30)
        menu = MainMenu(screen)
        menu.draw_menu()
        cursor.handle_keys()
        cursor.draw_cursor(screen)

        pygame.display.update()
        if playing == True:
            return playing

