import random

import pygame
from settings import TILE_WIDTH, TILE_HEIGHT
from map import STATIC_OBJECTS


class Tile:
    def __init__(self, x, y, object_type, texture_random):
        info_tile = STATIC_OBJECTS.get(object_type)
        self.name = info_tile.get("name")
        self.color = info_tile.get("color")
        if not info_tile.get("image"):
            self.image = pygame.image.load(f"images/textures/{self.name}.png")
        else:
            self.image = texture_random
            self.image = pygame.image.load(f"images/{self.name}/{self.image}")
        self.interactive = info_tile.get("interactive")
        self.size = info_tile.get("size")
        self.rect = pygame.Rect(x, y, self.size[0], self.size[1])

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen,self.color,self.rect)