import pygame
from settings import FONT_COMIC_27


class Button:
    def __init__(self, x, y, text, width=None, height=None, ):
        self.font = pygame.sysfont.SysFont("Arial", 20, True)
        self.ifpushed = False
        self.setup(x, y, text, width, height)

    def draw(self, screen):
        if not self.ifpushed:
            pygame.draw.rect(screen, self.color, self.rect)
        else:
            pygame.draw.rect(screen, self.color2, self.rect)
        screen.blit(self.text, self.text_rect)

    def setup(self, x, y, text, width, height, ):
        self.text = text
        self.text = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = text.get_rect()
        if width and height:
            self.width = width
            self.height = height
        else:
            self.width = self.text_rect.width + 20
            self.height = self.text_rect.height + 10

        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.text_rect.center = self.rect.center
        self.color = (255, 0, 0)
        self.color2 = (150, 0, 0)

    def update(self, screen):
        pass

    def switcher(self):
        self.ifpushed = not self.ifpushed


class Button_animates:
    def __init__(self, text, width, height, pos, elevation, top_passive_color='#475F77', text_color='#FFFFFF',
                 bottom_passive_color='#354B5E', active_color='#D73B4B', auto_text_width=False):
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.text = text
        self.text_color = text_color
        self.bottom_color = bottom_passive_color  # Цвет нижней части кнопки
        self.active_color = active_color
        self.passive_color = top_passive_color
        self.text_surf = FONT_COMIC_27.render(text, True, text_color)  # Текст кнопки

        if not auto_text_width:
            pos = pos[0] - width / 2, pos[1] - height / 2
            self.original_y_pos = pos[1]
            self.border_radius = 12
        else:
            self.border_radius = 4
            width, height = self.text_surf.get_size()
            width, height = width + 10, height + 5
            self.original_y_pos = pos[1]
        # Верхний прямоугольник кнопки
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = top_passive_color  # Цвет верхней части кнопки
        if not auto_text_width:
            self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        else:
            self.text_rect = self.text_surf.get_rect(left=self.top_rect.left + 5)
        # Нижний прямоугольник для создания визуального эффекта нажатия
        self.bottom_rect = pygame.Rect(pos, (width, elevation))

    def draw(self, screen):
        # Обновление позиции и размеров прямоугольников
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        # Отрисовка верхнего и нижнего прямоугольников и текста
        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=self.border_radius)
        screen.blit(self.text_surf, self.text_rect)
        result = self.check_click()
        return result

    def check_click(self):
        # Проверка, наведена ли мышь на кнопку
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.active_color  # Изменение цвета верхней части кнопки при наведении
            # (False, False, False)
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0  # Уменьшение визуального эффекта нажатия
                self.pressed = True

            else:
                if self.pressed:
                    self.dynamic_elevation = self.elevation
                    self.pressed = False
                    return True  # Обработка события нажатия кнопки
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = self.passive_color  # Возврат цвета верхней части кнопки в исходное состояние
        return False
