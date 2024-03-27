import pygame
from settings import TILE_WIDTH, TILE_HEIGHT
from class_dialogue import Dialogue_window  # main text,answers
from functions import json_read
from random import choice

class Object():
    def __init__(self, pos, type_):
        self.type_ = type_
        self.rect = pygame.Rect(pos, (TILE_WIDTH, TILE_HEIGHT))
        self.setup()
        self.player = None
    def draw(self, screen,trader):
        self.dialogue_window.draw(screen)
        if self.dialogue_window.continue_:
            a = 0
            if self.dialogue_window.info.get("name") == "Mystery":
                info = choice(self.dialogue_window.info.get("mysteries"))
                self.dialogue_window = Dialogue_window(info)
            if self.dialogue_window.info.get("name") == "Nameplate":
                info = choice(self.dialogue_window.info.get("news_text"))
                info = {"main_text":info,
                        "answers":["Уйти"]}
                self.dialogue_window = Dialogue_window(info)
            if self.dialogue_window.info.get("name") == "Trader":
                if self.dialogue_window.continue_ == True:
                    trader.active = True
            if self.dialogue_window.get_reward:
                self.player.coins += self.dialogue_window.info.get("reward")
                text = f"Ответ правильный. Вот ваша награда {self.dialogue_window.info.get('reward')} монет."
                info = {"main_text": text,
                        "answers": ["Уйти"]}
                self.dialogue_window = Dialogue_window(info)
            elif self.dialogue_window.get_reward == False:
                info = {"main_text": "Ответ неправильный :(",
                        "answers": ["Уйти"]}
                self.dialogue_window = Dialogue_window(info)


    def setup(self):
        info = json_read("dialogue_info.json")
        info = info.get(self.type_)
        self.dialogue_window = Dialogue_window(info)

