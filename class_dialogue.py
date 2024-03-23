import pygame
from settings import *
from buttons import Button_animates


class Dialogue_window:
    def __init__(self, info, type="main"):
        self.continue_ = False
        height_win = (S_HEIGHT - 60) / 3
        width_win = S_WIDTH / 5 * 3
        x, y = S_WIDTH / 2, 30 + height_win * 2
        self.main_rect = pygame.Rect(x, y, width_win, height_win)
        self.main_rect.centerx = x
        self.active = False
        self.main_color = (100, 100, 100)
        self.text_area_color = (150, 150, 150)
        self.text_color = (240, 240, 240)
        self.text_area_rect = pygame.Rect(self.main_rect.x + 10, self.main_rect.y + 10,
                                          self.main_rect.width - 20, (self.main_rect.height - 20) / 2)
        self.info = info
        self.text_images = self.prepare_text()
        self.buttons = self.creating_buttons()
        self.get_reward = None

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.main_color, self.main_rect)
            pygame.draw.rect(screen, self.text_area_color, self.text_area_rect)
            self.draw_text(screen)
            self.draw_buttons(screen)

    def draw_text(self, screen):
        y = 0
        for text_image in self.text_images:
            text_rect = text_image.get_rect(x=self.text_area_rect.x + 5, y=self.text_area_rect.y + 5 + y)
            y += text_rect.height + 5
            screen.blit(text_image, text_rect)

    def creating_buttons(self):
        buttons_ = []
        y = 0
        for text in self.info.get("answers"):
            button = Button_animates(text, 0, 0, (self.text_area_rect.left + 10, self.text_area_rect.bottom + 20 + y),
                                     6, auto_text_width=True)
            y += button.top_rect.height + 10
            buttons_.append(button)
        return buttons_

    def draw_buttons(self, screen):
        for button in self.buttons:
            if button.draw(screen):
                if button.text == "Уйти":
                    self.active = False
                if button.text in ("Продолжить", "Прочитать"):
                    self.continue_ = True
                if button.text == self.info.get("correct_answer"):
                    self.continue_ = True
                    self.get_reward = True
                elif button.text in self.info.get("answers"):
                    self.get_reward = False
                    self.continue_ = True

    def prepare_text(self):
        text_list = []
        text_image, croped_text = self.check_text_len(self.info.get("main_text"))
        text_list.append(text_image)
        while len(croped_text) != 0:
            print(croped_text)
            text_image, croped_text = self.check_text_len(" ".join(croped_text))
            text_list.append(text_image)
        return text_list

    def check_text_len(self, text, croped_text=None):
        if croped_text is None:
            croped_text = []
        text_image = FONT_COMIC_32.render(text, True, self.text_color)
        width = text_image.get_width()
        while width > self.text_area_rect.width - 10:
            text = text.split()
            croped_text.insert(0, text.pop(-1))
            text = " ".join(text)
            text_image = FONT_COMIC_32.render(text, True, self.text_color)
            width = text_image.get_width()
        return text_image, croped_text


class Trade_window(Dialogue_window):
    def __init__(self):
        super().__init__()
        self.weapons = {}


class Object_interesting:
    def __init__(self, pos, color):
        self.rect = pygame.Rect(pos, (TILE_WIDTH, TILE_HEIGHT))
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
