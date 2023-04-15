import pygame
import pygame_gui

pygame.init()

class RullScreen:
    volume = 0.02
    sound2 = pygame.mixer.Sound('sounds/end.mp3')

    def __init__(self, window):
        self.window = window

    def draw_rull_screen(self):
        self.window.bg = pygame.image.load('img/bg8.jpg').convert()
        self.window.bg = pygame.transform.scale(self.window.bg, self.window.res)
        screen = pygame.Surface(self.window.res)
        screen.blit(self.window.bg, (0, 0))
        intro_text = ["Правила", "",
                      "Стандартный тетрис в прямоугольной области 10 Х 20",
                      "В полёте игрок может поворачивать фигурку на 90° и двигать",
                      "её по горизонтали:",
                      "поворот - пробел, движение - стрелками право/лево.",
                      "Также можно сбрасывать фигурку, то есть ускорять её падение:",
                      "стрелка вниз.",
                      "Если заполнился горизонтальный ряд из 10 клеток, он пропадает",
                      "Дополнительно показывается следующая после текущей фигурка",
                      "Темп игры постепенно ускоряется", "", "Настройка", "фоновая музыка", "игровые звуки"]

        font0 = pygame.font.Font('font/font.ttf', 12)
        font1 = pygame.font.Font('font/font.ttf', 30)
        text_coord = 20
        for line in intro_text:
            font = font1 if line == intro_text[0] or line == intro_text[12] else font0
            string_rendered = font.render(line, 1, pygame.Color('darkorange'))
            intro_rect = string_rendered.get_rect()
            text_coord += 1
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        self.manager2 = pygame_gui.UIManager((800, 600))
        self.window.sc.blit(screen, (0, 0))

        self.slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(
            relative_rect=pygame.Rect((250, 370), (200, 15)),
            start_value=self.volume, manager=self.manager2, value_range=(0, 1)
        )

        self.slider2 = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(
            relative_rect=pygame.Rect((250, 395), (200, 15)),
            start_value=self.volume, manager=self.manager2, value_range=(0, 1)
        )

        self.sound2.set_volume(0.02)

        pygame.display.flip()

    def logic(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return self.volume
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                        if event.ui_element == self.slider:
                            pygame.mixer.music.set_volume(event.value)
                        elif event.ui_element == self.slider2:
                            self.sound2.set_volume(event.value)
                self.manager2.process_events(event)
            self.manager2.update(pygame.time.Clock().tick(60) / 1000.0)
            self.manager2.draw_ui(self.window.sc)
            pygame.display.update()

    def start(self):
        self.draw_rull_screen()
        self.logic()