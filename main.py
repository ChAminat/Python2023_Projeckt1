import pygame
import pygame_gui
import sys
from copy import deepcopy
from random import choice, randrange
from field import Field
from play_window import PlayWindow
from figures import Figures
from rull_screen import RullScreen
from reco_screen import RecoScreen
from start_screen import StartScreen

pygame.init()
clock = pygame.time.Clock()

class Game():
    score, lines = 0, 0
    scores = {0: 0, 1: 10, 2: 30, 3: 70, 4: 150}
    score_to_save = 0

    def __init__(self):
        self.field = Field()
        self.window = PlayWindow(self.field)
        self.figures_inf = Figures(self.field)
        self.start_screen = StartScreen(self.window)
        self.rull_screen = RullScreen(self.window)
        self.reco_screen = RecoScreen(self.window)

    def game_over(self):
        pygame.mixer.music.pause()
        self.rull_screen.sound2.play()
        self.field.set_record(self.record, self.score)
        self.score_to_save = self.score
        self.field.save_score(self.score_to_save)
        self.field.field_table = [[0 for i in range(self.field.width_per_cell)]
                                  for i in range(self.field.height_per_cell)]
        self.figures_inf.anim_count, self.figures_inf.anim_speed, self.figures_inf.anim_limit = 0, 60, 2000
        self.score, self.score_to_save = 0, 0
        for i_rect in self.field.grid:
            pygame.draw.rect(self.window.game_sc, self.figures_inf.get_color(), i_rect)
            self.window.sc.blit(self.window.game_sc, (0, self.window.res[1] - self.field.game_res[1]))
            pygame.display.flip()
            clock.tick(90)
        pygame.mixer.music.unpause()

    def quit(self):
        self.figure, self.next_figure = deepcopy(choice(self.figures_inf.figures)), deepcopy(
            choice(self.figures_inf.figures))
        self.field.set_record(self.record, self.score)
        self.field.field_table = [[0 for i in range(self.field.width_per_cell)] for i in
                                  range(self.field.height_per_cell)]
        self.score_to_save = self.score
        self.field.save_score(str(self.score_to_save))

        self.figures_inf.anim_count, self.figures_inf.anim_speed, self.figures_inf.anim_limit = 0, 60, 2000
        self.score, self.score_to_save = 0, 0
        for i_rect in self.field.grid:
            self.window.sc.blit(self.window.game_sc, (0, self.window.res[1] - self.field.game_res[1]))
            pygame.display.flip()

    def moving_x(self, dx):
        self.figure_old = deepcopy(self.figure)
        for i in range(4):
            self.figure[i].x += dx
            if not self.field.check_borders(self.figure[i].x, self.figure[i].y):
                self.figure = deepcopy(self.figure_old)
                break

    def moving_y(self):
        self.figures_inf.anim_count += self.figures_inf.anim_speed
        if self.figures_inf.anim_count > self.figures_inf.anim_limit:
            self.figures_inf.anim_count = 0
            self.figure_old = deepcopy(self.figure)
            for i in range(4):
                self.figure[i].y += 1
                if not self.field.check_borders(self.figure[i].x, self.figure[i].y):
                    for i in range(4):
                        self.field.field_table[self.figure_old[i].y][self.figure_old[i].x] = self.color
                    self.figure, self.color = self.next_figure, self.next_color
                    self.next_figure, self.next_color = deepcopy(
                        choice(self.figures_inf.figures)), self.figures_inf.get_color()
                    self.figures_inf.anim_limit = 2000
                    break

    def rotate(self):
        center = self.figure[0]
        for i in range(4):
            x = self.figure[i].y - center.y
            y = self.figure[i].x - center.x
            self.figure[i].x = center.x - x
            self.figure[i].y = center.y + y
            if not self.field.check_borders(self.figure[i].x, self.figure[i].y):
                self.figure = deepcopy(self.figure_old)
                break

    def procedure(self):
        self.record = self.field.get_record()
        dx, rotate = 0, False

        self.window.sc.blit(self.window.bg, (0, 0))
        self.window.sc.blit(self.window.game_sc, (0, self.window.res[1] - self.field.game_res[1]))
        self.window.game_sc.blit(self.window.game_bg, (0, 0))

        # delay for full lines
        for i in range(self.lines):
            pygame.time.wait(200)

        # control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1
                elif event.key == pygame.K_DOWN:
                    self.figures_inf.anim_limit = 100
                elif event.key == pygame.K_SPACE:
                    rotate = True

        self.moving_x(dx)
        self.moving_y()

        # rotate
        self.figure_old = deepcopy(self.figure)
        if rotate:
            self.rotate()

        # check lines
        line, self.lines = self.field.height_per_cell - 1, 0
        line, self.lines, anim_change = self.field.check_lines(line, self.lines)
        self.figures_inf.anim_speed += anim_change

        self.score += self.scores[self.lines]  # compute score
        self.window.draw_grid(self.field)  # draw grid
        self.figures_inf.draw_figure(self.figure, self.field, self.window, self.color)  # draw moving figure
        self.figures_inf.draw_figure(self.next_figure, self.field, self.window, self.next_color, 1)  # draw next figure
        self.figures_inf.draw_field(self.field, self.window)  # draw field
        self.window.draw_title(self.score, self.record)  # draw titles

        # game over
        for i in range(self.field.width_per_cell):
            if self.field.field_table[0][i]:
                self.game_over()

        pygame.display.update()
        pygame.display.flip()
        clock.tick(self.field.FPS)
        return True

    def start(self):
        self.figure, self.next_figure = self.figures_inf.new_fig(), self.figures_inf.new_fig()
        self.color, self.next_color = self.figures_inf.get_color(), self.figures_inf.get_color()

        while True:
            self.window.start(self.rull_screen.volume1)
            running = True
            koef, dif = self.start_screen.start()
            while running:
                if koef == 1:
                    if dif == 'Medium':
                        self.figures_inf.anim_speed = 120
                    elif dif == 'Hard':
                        self.figures_inf.anim_speed = 200
                    running = self.procedure()
                elif koef == 2:
                    self.rull_screen.start()
                    break
                elif koef == 3:
                    self.reco_screen.start()
                    break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.window.terminate()


if __name__ == "__main__":
    new_game = Game()
    new_game.start()