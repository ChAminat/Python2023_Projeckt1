import pygame
from copy import deepcopy
from random import choice, randrange

class Figures:
    figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                   [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                   [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                   [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                   [(0, 0), (0, -1), (0, 1), (-1, -1)],
                   [(0, 0), (0, -1), (0, 1), (1, -1)],
                   [(0, 0), (0, -1), (0, 1), (-1, 0)]]

    def __init__(self, field, anim_count=0, anim_speed=60, anim_limit=2000):
        self.anim_count = anim_count
        self.anim_speed = anim_speed
        self.anim_limit = anim_limit
        self.figures = [[pygame.Rect(x + field.width_per_cell // 2, y + 1, 1, 1) for x, y in fig_pos]
                        for fig_pos in self.figures_pos]
        self.figure_rect = pygame.Rect(0, 0, field.tile_size - 2, field.tile_size - 2)

    def nex_fig(self):
        return deepcopy(choice(self.figures))

    def new_fig(self):
        return deepcopy(choice(self.figures))

    def get_color(self):
        return (randrange(30, 256), randrange(30, 256), randrange(30, 256))

    def draw_figure(self, figure, field, window, color, flag=0):
        for i in range(4):
            self.figure_rect.x = figure[i].x * field.tile_size + (field.game_res[0] - 60) * flag
            self.figure_rect.y = figure[i].y * field.tile_size + (field.game_res[1] // 4) * flag
            pygame.draw.rect(window.sc if flag else window.game_sc, color, self.figure_rect)

    def draw_field(self, field, window):
        for y, raw in enumerate(field.field_table):
            for x, col in enumerate(raw):
                if col:
                    self.figure_rect.x, self.figure_rect.y = x * field.tile_size, y * field.tile_size
                    pygame.draw.rect(window.game_sc, col, self.figure_rect)