import pygame
import pygame_gui
import sys
from copy import deepcopy
from random import choice, randrange

FONT_SIZE = 20
MAX_ALPHA_VALUE = 90
GROWTH_RATE = 6
START_KATAKANA_CHAR_POS = int('0x30a0', 16)
SIZE_OF_ALPHABET = 96

pygame.init()
KATAKANA = [chr(START_KATAKANA_CHAR_POS + i) for i in range(SIZE_OF_ALPHABET)]
FONT1 = pygame.font.Font('font/MS Mincho.ttf', FONT_SIZE)
GREEN_KATAKANA = [FONT1.render(char, True, (40, randrange(160, 256), 40)) for char in KATAKANA]
LIGHTGREEN_KATAKANA = [FONT1.render(char, True, pygame.Color('lightgreen')) for char in KATAKANA]

class Symbol:
    def __init__(self, x, y, speed):
        self.x, self.y = x, y
        self.speed = speed
        self.value = choice(GREEN_KATAKANA)
        self.interval = randrange(5, 30)

    def draw(self, color, window, surface):
        frames = pygame.time.get_ticks()
        if not frames % self.interval:
            self.value = choice(GREEN_KATAKANA if color == 'green' else LIGHTGREEN_KATAKANA)
        self.y = self.y + self.speed if self.y < window.height_of_play_widow else -FONT_SIZE
        surface.blit(self.value, (self.x, self.y))


class SymbolColumn:
    def __init__(self, x, y):
        self.column_height = randrange(8, 24)
        self.speed = randrange(3, 7)
        self.symbols = [Symbol(x, i, self.speed) for i in range(y, y - FONT_SIZE * self.column_height, -FONT_SIZE)]

    def draw(self, window, surface):
        [symbol.draw('green' if i else 'lightgreen', window, surface) for i, symbol in enumerate(self.symbols)]


class StartScreen:
    def __init__(self, window):
        self.window = window
        self.surface = pygame.Surface(self.window.res)
        pygame.init()

    def update_screen(self):
        time_delta = pygame.time.Clock().tick(50) / 10000.0
        self.manager.update(time_delta)
        self.manager.draw_ui(self.window.sc)
        pygame.display.update()
        self.window.sc.blit(self.title_tetris,
                            (self.window.res[0] // 2 - pygame.font.Font.size(self.main_font, "TETRIS")[0] // 2, 50))
        self.window.sc.blit(self.title_tetris1,
                            (self.window.res[0] // 2 - pygame.font.Font.size(self.main_font,
                                                                             "matrix edition")[0] // 2 + 90, 120))
        pygame.time.Clock().tick(50)

    def draw_start_screen(self):
        self.surface.set_alpha(0)
        symbol_columns = [SymbolColumn(x, randrange(-self.window.height_of_play_widow, 0))
                          for x in range(0, self.window.width_of_play_widow, FONT_SIZE)]

        alpha_value = 0
        self.manager = pygame_gui.UIManager((800, 600))
        self.main_font = pygame.font.Font('font/font.ttf', self.window.field.tile_size + 30)
        self.note_font = pygame.font.Font('font/font.ttf', self.window.field.tile_size + 5)
        self.title_tetris = self.main_font.render('TETRIS', True, pygame.Color('darkorange'))
        self.title_tetris1 = self.note_font.render('matrix edition', True, pygame.Color('darkorange'))

        start = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 470), (190, 50)),
            text='Старт',
            manager=self.manager
        )

        difficulty = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
            options_list=['Easy', 'Medium', 'Hard'], starting_option='Easy',
            relative_rect=pygame.Rect((25, 200), (120, 50)), manager=self.manager,
        )

        rulls = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((180, 280), (120, 50)),
            text='Правила',
            manager=self.manager
        )
        reco = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((335, 360), (120, 50)),
            text='Рекорды',
            manager=self.manager
        )

        dif = 'Easy'
        while True:
            self.window.sc.blit(self.surface, (0, 0))
            self.surface.fill(pygame.Color('black'))

            [symbol_column.draw(self.window, self.surface) for symbol_column in symbol_columns]
            if not pygame.time.get_ticks() % 20 and alpha_value < MAX_ALPHA_VALUE:
                alpha_value += GROWTH_RATE
                self.surface.set_alpha(alpha_value)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.window.terminate()
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                        dif = event.text
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == start:
                            return 1, dif
                        elif event.ui_element == rulls:
                            return 2, dif
                        elif event.ui_element == reco:
                            return 3, dif
                self.manager.process_events(event)

            self.update_screen()

    def start(self):
        return self.draw_start_screen()