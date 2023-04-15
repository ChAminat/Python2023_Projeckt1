import pygame
import pygame_gui

class RecoScreen:
    def __init__(self, window):
        self.window = window

    def get_reco_info(self):
        with open('scores.txt', 'r') as s:
            lst = [i.strip() for i in s.readlines()]
        if len(lst) < 5:
            lst.extend(['0'] * (5 - len(lst)))

        lst = sorted(list(map(int, lst)), reverse=True)
        fir = self.window.field.get_record()
        sec, thir, four, fif = lst[1], lst[2], lst[3], lst[4]
        intro_text = ["Рекорды", f"1.   {fir}", f"2.   {sec}", f"3.   {thir}", f"4.   {four}", f"5.   {fif}"]
        return intro_text

    def draw_reco_screen(self):
        self.window.bg = pygame.image.load('img/bg8.jpg').convert()
        self.window.bg = pygame.transform.scale(self.window.bg, self.window.res)
        screen3 = pygame.Surface(self.window.res)
        screen3.blit(self.window.bg, (0, 0))

        intro_text = self.get_reco_info()
        font0 = pygame.font.Font('font/font.ttf', 25)
        font1 = pygame.font.Font('font/font.ttf', 30)
        text_coord = 20
        for line in intro_text:
            font = font1 if line == intro_text[0] else font0
            string_rendered = font.render(line, 1, pygame.Color('darkorange'))
            intro_rect = string_rendered.get_rect()
            text_coord += 20
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen3.blit(string_rendered, intro_rect)

        self.window.sc.blit(screen3, (0, 0))

        pygame.display.flip()

    def logic(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
            pygame.display.flip()

    def start(self):
        self.draw_reco_screen()
        self.logic()
