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
score, lines = 0, 0
scores = {0: 0, 1: 10, 2: 30, 3: 70, 4: 150}
score_to_save = 0

if __name__ == "__main__":
    field = Field()
    window = PlayWindow(field)
    figures_inf = Figures(field)
    start_screen = StartScreen(window)
    rull_screen = RullScreen(window)
    reco_screen = RecoScreen(window)

    figure, next_figure = figures_inf.new_fig(), figures_inf.new_fig()
    color, next_color = figures_inf.get_color(), figures_inf.get_color()

    while True:
        window.start()
        running = True
        koef, dif = start_screen.start()
        while running:
            if koef == 1:
                if dif == 'Medium':
                    figures_inf.anim_speed = 120
                elif dif == 'Hard':
                    figures_inf.anim_speed = 200

                record = field.get_record()
                dx, rotate = 0, False

                window.sc.blit(window.bg, (0, 0))
                window.sc.blit(window.game_sc, (0, window.res[1] - field.game_res[1]))
                window.game_sc.blit(window.game_bg, (0, 0))

                # delay for full lines
                for i in range(lines):
                    pygame.time.wait(200)

                # control
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        figure, next_figure = deepcopy(choice(figures_inf.figures)), deepcopy(choice(figures_inf.figures))
                        field.set_record(record, score)
                        field.field_table = [[0 for i in range(field.width_per_cell)] for i in range(field.height_per_cell)]
                        score_to_save = score
                        field.save_score(str(score_to_save))

                        figures_inf.anim_count, figures_inf.anim_speed, figures_inf.anim_limit = 0, 60, 2000
                        score, score_to_save = 0, 0
                        for i_rect in field.grid:
                            window.sc.blit(window.game_sc, (0, window.res[1] - field.game_res[1]))
                            pygame.display.flip()
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_DOWN:
                            figures_inf.anim_limit = 100
                        elif event.key == pygame.K_SPACE:
                            rotate = True

                # move x
                figure_old = deepcopy(figure)
                for i in range(4):
                    figure[i].x += dx
                    if not field.check_borders(figure[i].x, figure[i].y):
                        figure = deepcopy(figure_old)
                        break

                # move y
                figures_inf.anim_count += figures_inf.anim_speed
                if figures_inf.anim_count > figures_inf.anim_limit:
                    figures_inf.anim_count = 0
                    figure_old = deepcopy(figure)
                    for i in range(4):
                        figure[i].y += 1
                        if not field.check_borders(figure[i].x, figure[i].y):
                            for i in range(4):
                                field.field_table[figure_old[i].y][figure_old[i].x] = color
                            figure, color = next_figure, next_color
                            next_figure, next_color = deepcopy(choice(figures_inf.figures)), figures_inf.get_color()
                            figures_inf.anim_limit = 2000
                            break

                # rotate
                center = figure[0]
                figure_old = deepcopy(figure)
                if rotate:
                    for i in range(4):
                        x = figure[i].y - center.y
                        y = figure[i].x - center.x
                        figure[i].x = center.x - x
                        figure[i].y = center.y + y
                        if not field.check_borders(figure[i].x, figure[i].y):
                            figure = deepcopy(figure_old)
                            break

                # check lines
                line, lines = field.height_per_cell - 1, 0
                line, lines, anim_change = field.check_lines(line, lines)
                figures_inf.anim_speed += anim_change


                score += scores[lines] # compute score
                window.draw_grid(field)  # draw grid
                figures_inf.draw_figure(figure, field, window, color) # draw moving figure
                figures_inf.draw_figure(next_figure, field, window, next_color, 1) # draw next figure
                figures_inf.draw_field(field, window) # draw field
                window.draw_title(score, record) # draw titles

                # game over
                for i in range(field.width_per_cell):
                    if field.field_table[0][i]:
                        pygame.mixer.music.pause()
                        rull_screen.sound2.play() #correct!
                        field.set_record(record, score)
                        score_to_save = score
                        field.save_score(score_to_save)
                        field.field_table = [[0 for i in range(field.width_per_cell)]
                                             for i in range(field.height_per_cell)]
                        figures_inf.anim_count, figures_inf.anim_speed, figures_inf.anim_limit = 0, 60, 2000
                        score, score_to_save = 0, 0
                        for i_rect in field.grid:
                            pygame.draw.rect(window.game_sc, figures_inf.get_color(), i_rect)
                            window.sc.blit(window.game_sc, (0, window.res[1] - field.game_res[1]))
                            pygame.display.flip()
                            clock.tick(90)
                        pygame.mixer.music.unpause()

                pygame.display.update()
                pygame.display.flip()
                clock.tick(field.FPS)
            elif koef == 2:
                rull_screen.start()
                break
            elif koef == 3:
                reco_screen.start()
                break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.terminate()