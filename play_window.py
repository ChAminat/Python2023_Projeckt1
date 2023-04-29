import pygame
import sys

class PlayWindow:
    def __init__(self, field, W=10, H=20, TILE=30):
        self.width_of_play_widow = W * TILE + 2 * (W * TILE) // 3
        self.height_of_play_widow = H * TILE + 30
        self.res = self.width_of_play_widow, self.height_of_play_widow
        self.field = field

    def draw_start_window(self):
        pygame.display.set_caption('TETRIS')
        self.sc = pygame.display.set_mode(self.res)  # основной экран
        self.game_sc = pygame.Surface(self.field.game_res)  # доп. экран

    def draw_play_window(self):
        self.bg = pygame.image.load('img/bg1.jpg').convert()  # фон всего поля
        self.bg = pygame.transform.scale(self.bg, self.res)
        self.game_bg = pygame.image.load('img/bg11.jpg').convert()  # игровое поле
        self.game_bg = pygame.transform.scale(self.game_bg, self.field.game_res)

    def draw_title(self, score, record):
        main_font = pygame.font.Font('font/font.ttf', self.field.tile_size + 15)
        font = pygame.font.Font('font/font.ttf', self.field.tile_size)

        x = self.res[0] - pygame.font.Font.size(main_font, "TETRIS")[0] - 20
        yh = self.res[0] - pygame.font.Font.size(main_font, "TETRIS")[1]
        title_tetris = main_font.render('TETRIS', True, pygame.Color('darkorange'))
        self.sc.blit(title_tetris, (x, 25))

        title_score = font.render('score:', True, pygame.Color('green'))
        self.sc.blit(title_score, (x + 10, yh))
        self.sc.blit(font.render(str(score), True, pygame.Color('white')),
                       (x + 25, yh + pygame.font.Font.size(font, "score:")[1]))

        title_record = font.render('record:', True, pygame.Color('purple'))
        self.sc.blit(title_record, (x + 10, yh + pygame.font.Font.size(font, "record:")[1] + 30))
        self.sc.blit(font.render(record, True, pygame.Color('gold')),
                       (x + 25, yh + pygame.font.Font.size(font, "score:")[1] * 2 + 30))

    def draw_grid(self, field):
        [pygame.draw.rect(self.game_sc, (25, 51, 0), i_rect, 1) for i_rect in self.field.grid]

    def set_music(self, volume):
        pygame.mixer.music.load('sounds/Zion.mp3')
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(volume)

    def start(self, volume):
        self.draw_start_window()
        self.draw_play_window()

    def terminate(self):
        pygame.quit()
        sys.exit