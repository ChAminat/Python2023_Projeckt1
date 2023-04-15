import pygame
import pygame_gui
import sys
from copy import deepcopy
from random import choice, randrange

pygame.init()
FONT_SIZE = 20
katakana = [chr(int('0x30a0', 16) + i) for i in range(96)]
font1 = pygame.font.Font('font/ms mincho.ttf', FONT_SIZE)  # , bold=True
green_katakana = [font1.render(char, True, (40, randrange(160, 256), 40)) for char in katakana]
lightgreen_katakana = [font1.render(char, True, pygame.Color('lightgreen')) for char in katakana]

class Symbol:
    def __init__(self, x, y, speed):
        self.x, self.y = x, y
        self.speed = speed
        self.value = choice(green_katakana)
        self.interval = randrange(5, 30)

    def draw(self, color, window, surface):
        frames = pygame.time.get_ticks()
        if not frames % self.interval:
            self.value = choice(green_katakana if color == 'green' else lightgreen_katakana)
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

    def draw_start_screen(self):
        surface = pygame.Surface(self.window.res)
        surface.set_alpha(0)

        symbol_columns = [SymbolColumn(x, randrange(-self.window.height_of_play_widow, 0))
                          for x in range(0, self.window.width_of_play_widow, FONT_SIZE)]

        alpha_value = 0
        time_delta = pygame.time.Clock().tick(50) / 1000.0
        manager = pygame_gui.UIManager((800, 600))
        main_font = pygame.font.Font('font/font.ttf', self.window.field.tile_size + 30)
        note_font = pygame.font.Font('font/font.ttf', self.window.field.tile_size + 5)
        title_tetris = main_font.render('TETRIS', True, pygame.Color('darkorange'))
        title_tetris1 = note_font.render('matrix edition', True, pygame.Color('darkorange'))

        start = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 470), (190, 50)),
            text='Старт',
            manager=manager
        )

        difficulty = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
            options_list=['Easy', 'Medium', 'Hard'], starting_option='Easy',
            relative_rect=pygame.Rect((25, 200), (120, 50)), manager=manager,
        )

        rulls = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((180, 280), (120, 50)),
            text='Правила',
            manager=manager
        )
        reco = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((335, 360), (120, 50)),
            text='Рекорды',
            manager=manager
        )

        dif = 'Easy'
        while True:
            self.window.sc.blit(surface, (0, 0))
            surface.fill(pygame.Color('black'))

            [symbol_column.draw(self.window, surface) for symbol_column in symbol_columns]
            if not pygame.time.get_ticks() % 20 and alpha_value < 90:
                alpha_value += 6
                surface.set_alpha(alpha_value)

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
                manager.process_events(event)
            manager.update(time_delta)
            manager.draw_ui(self.window.sc)
            pygame.display.update()
            self.window.sc.blit(title_tetris,
                                (self.window.res[0] // 2 - pygame.font.Font.size(main_font, "TETRIS")[0] // 2, 50))
            self.window.sc.blit(title_tetris1,
                           (self.window.res[0] // 2 - pygame.font.Font.size(main_font,
                                                                            "matrix edition")[0] // 2 + 90, 120))
            pygame.time.Clock().tick(50)

    def start(self):
        return self.draw_start_screen()
