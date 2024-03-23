import pygame
import math

pygame.init()
SCREEN_SIZE = S_WIDTH,S_HEIGHT = 1920, 1080
fps = 60
FONT20 = pygame.sysfont.SysFont("Arial", 20, bold=True)
FONT21 = pygame.sysfont.SysFont("Arial", 21, bold=True)

FONT25 = pygame.sysfont.SysFont("Arial", 25, bold=False)
FONT30 = pygame.sysfont.SysFont("Arial", 30, bold=False)

FONT_CALIBRI_50 = pygame.sysfont.SysFont("Calibri", 50, bold=False)
FONT_COMIC_32 = pygame.sysfont.SysFont("Comis Sans", 32, bold=False)
FONT_COMIC_27 = pygame.sysfont.SysFont("Comis Sans", 27, bold=True)
FONT_COMIC_20 = pygame.sysfont.SysFont("Comis Sans", 20, bold=True)
FONT_COMIC_12 = pygame.sysfont.SysFont("Comic Sans", 12, bold=True)
MINIMAP_TILE_WIDTH = 10
MINIMAP_TILE_HEIGHT = 10


TILE_COUNT_X = 21
TILE_COUNT_Y = 12
TILE_WIDTH = math.ceil(SCREEN_SIZE[0] / TILE_COUNT_X)
TILE_HEIGHT = math.ceil(SCREEN_SIZE[1] / TILE_COUNT_Y)