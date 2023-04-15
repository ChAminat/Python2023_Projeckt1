import pygame

class Field:
    FPS = 60
    def __init__(self, width=10, height=20, tile=30):
        self.width_per_cell = width
        self.height_per_cell = height
        self.tile_size = tile
        self.game_res = width * tile, height * tile
        self.grid = [pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                     for x in range(self.width_per_cell) for y in range(self.height_per_cell)]
        self.field_table = [[0 for i in range(self.width_per_cell)] for j in range(self.height_per_cell)]

    def check_borders(self, fig_x, fig_y):
        if fig_x < 0 or fig_x > self.width_per_cell - 1:
            return False
        elif fig_y > self.height_per_cell - 1 or self.field_table[fig_y][fig_x]:
            return False
        return True

    def get_record(self):
        try:
            with open('record') as f:
                return f.readline()
        except FileNotFoundError:
            with open('record', 'w') as f:
                f.write('0')

    def set_record(self, record, score):
        rec = max(int(record), score)
        with open('record', 'w') as f:
            f.write(str(rec))

    def save_score(self, score):
        with open('scores.txt', 'r') as s:
            lst = [i.strip() for i in s.readlines()]
            lst.append(str(score))
        with open('scores.txt', 'w') as s:
            s.write('\n'.join(lst))

    def check_lines(self, line, lines):
        anim_speed = 0
        for row in range(self.height_per_cell - 1, -1, -1):
            count = 0
            for i in range(self.width_per_cell):
                if self.field_table[row][i]:
                    count += 1
                self.field_table[line][i] = self.field_table[row][i]
            if count < self.width_per_cell:
                line -= 1
            else:
                anim_speed += 3
                lines += 1
        return line, lines, anim_speed