import random
import sys
from class_dialogue import *
from map import *
from settings import *
import pygame
from buttons import *
from player import *
from save_load_map import *
from functions import *
from enemies import Enemy
from event_objects import Object
from tile import Tile
from map import temp
from cursor_trader import Trader_menu
class Main:
    def __init__(self):
        self.current_window = Main_menu(True)
        self.width, self.height = SCREEN_SIZE
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.fps = fps
        self.clock = CLOCK
        self.player = Player(self.width / 2, self.height / 2, 20, 20)
        self.tile_width = MINIMAP_TILE_WIDTH
        self.tile_height = MINIMAP_TILE_HEIGHT
        self.setup()

    def setup(self):
        info = load_map()
        if isinstance(info, dict):
            self.x, self.y = info["x_on_map"], info["y_on_map"]
            self.map = info["map"]
            self.room_num = info["room_num"]
            self.current_window = Main_menu(True)
        else:
            self.x = random.randint(0, self.tile_width - 1)
            self.y = random.randint(0, self.tile_height - 1)
            self.map = [[[None, None]] * self.tile_width for num in range(self.tile_height)]
            self.map[self.y][self.x] = [None, temp]
            self.room_num = 0
            self.current_window = Main_menu(False)

    def screen_show(self):
        self.screen.fill((0, 0, 0))
        if self.current_window.class_type == "Battle":
            self.obstacles = self.current_window.local_objects
            self.current_window.draw(self.screen)
            self.player.draw(self.screen)
        if self.current_window.class_type == "Main_menu":
            result = self.current_window.draw(self.screen)
            if result == "Продолжить":
                self.change_window()
            elif result == "Начать приключение":
                self.x = random.randint(0, self.tile_width - 1)
                self.y = random.randint(0, self.tile_height - 1)
                self.map = [[[None, None]] * self.tile_width for num in range(self.tile_height)]
                self.map[self.y][self.x] = [None, temp]
                self.room_num = 0
                self.change_window()
            elif result == "Выйти из игры":
                pygame.quit()
                sys.exit()

    def change_window(self, side=None):
        rooms = ["Отдых", "Боёвка", "Родник", "Торговец", "Загадка", "Табличка"]
        new_room = random.choice(rooms)
        new_map_room = {"Отдых": random.choice(REST_ROOMS),
                        "Боёвка": random.choice(FIGHT_ROOMS),
                        "Родник": random.choice(SOURCE_ROOMS),
                        "Торговец": random.choice(TRADER_ROOMS),
                        "Загадка": random.choice(MYSTERY_ROOMS),
                        "Табличка": random.choice(NAMEPLATE_ROOMS)}
        if side == "right":
            self.x += 1
        elif side == "left":
            self.x -= 1
        elif side == "up":
            self.y -= 1
        elif side == "down":
            self.y += 1
        self.x, self.y = check_room_existing(self.x, self.y, self.tile_width, self.tile_height)
        self.check_or_swap_room(new_room, new_map_room[new_room])
        print(*self.map, sep="\n")
        print()

    def check_or_swap_room(self, new_room, map):
        next_room = self.map[self.y][self.x][0]
        if next_room == None:
            self.map[self.y][self.x] = new_room, map
            self.room_num += 1
            self.current_window = Battle(new_room, self.room_num, self.map, self.x, self.y,
                                         (self.tile_width, self.tile_height), map,self.player,used=False)
        else:
            map = self.map[self.y][self.x][1]
            self.current_window = Battle(next_room, self.room_num, self.map, self.x, self.y,
                                         (self.tile_width, self.tile_height), map,self.player,used=True)

    # self.current_window = Battle(random.choice(rooms))

    def update(self):
        self.screen_show()
        if isinstance(self.current_window, Battle):
            self.obstacles = self.current_window.local_objects
            self.player.move(self.obstacles)
            self.current_window.update_enemy(self.player.rect)
            self.current_window.update_events(self.player)
            self.current_window.items_updated(self.screen, self.player)
        self.need_to_change_room()

    def need_to_change_room(self):
        gap = TILE_WIDTH + 5
        if self.player.rect.centerx > self.width:
            self.player.rect.centerx = gap
            self.change_window("right")
        elif self.player.rect.centerx < 0:
            self.player.rect.centerx = self.width - gap
            self.change_window("left")
        elif self.player.rect.centery > self.height:
            self.player.rect.centery = gap
            self.change_window("down")
        elif self.player.rect.centery < 0:
            self.player.rect.centery = self.height - gap
            self.change_window("up")


class Main_menu:
    def __init__(self, buttons_num):
        self.class_type = "Main_menu"
        self.buttons_num = buttons_num
        self.active = True
        self.continue_ = {
            "text": "Продолжить",
            "pos": (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2 - 200)
        }
        self.new_game = {
            "text": "Начать приключение",
            "pos": (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2 - 100)
        }
        self.achievements = {
            "text": "Достижения",
            "pos": (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)
        }
        self.settings = {
            "text": "Настройки",
            "pos": (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2 + 100)
        }
        self.exit = {
            "text": "Выйти из игры",
            "pos": (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2 + 200)
        }
        if self.buttons_num:
            self.buttons = [self.continue_, self.new_game, self.achievements, self.settings, self.exit]
        else:
            self.buttons = [self.new_game, self.achievements, self.settings, self.exit]
        self.setup()

    def setup(self):
        self.buttons_rect = []
        for button in self.buttons:
            button = Button_animates(button["text"], 220, 80, button["pos"], elevation=6)
            self.buttons_rect.append(button)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for button in self.buttons_rect:
            if button.draw(screen):
                return button.text


class Battle:
    def __init__(self, type_, room, map, x, y, size_of_map, local_map, used,player):
        self.trader_menu = Trader_menu(player.coins)
        self.class_type = "Battle"
        self.start_timer = pygame.time.get_ticks()
        self.enemy_hits = 0
        self.used = used
        self.enemies = []
        self.items_list = []
        self.events = []
        self.local_map = local_map
        self.active_minimap = False
        self.type_ = type_
        self.map = map
        self.x = x
        self.y = y
        self.tile_width, self.tile_height = size_of_map
        self.room = room
        self.color = self.room_type(self.type_)
        self.setup_room_text()
        self.main_minimap_rect = pygame.Rect(0, 0, SCREEN_SIZE[0] / 3, SCREEN_SIZE[1] / 3)
        self.main_minimap_rect.topleft = SCREEN_SIZE[0] - 100, SCREEN_SIZE[1] - 100
        self.local_objects = self.setup_local_map(local_map)


    def draw(self, screen):
        screen.fill(self.color)
        self.draw_local_map(screen)
        pygame.draw.rect(screen, (88, 62, 38), self.text_bg)
        screen.blit(self.text, self.text_rect)
        self.draw_enemies(screen)
        self.draw_events(screen)
        self.trader_menu.draw(screen)
        if self.active_minimap:
            scale = 2
            size = ((20 * scale) * self.tile_width) + ((10 * scale) * self.tile_height - 1)
            self.main_minimap_rect.width = size
            self.main_minimap_rect.height = size
            self.main_minimap_rect.center = SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2
            rects, colors = self.setup_minimap(self.main_minimap_rect.x, self.main_minimap_rect.y, scale=scale,
                                               tray=True)
            self.draw_minimap(rects, colors, screen)
        else:
            size = (20 * 3) + (10 * 2)
            self.main_minimap_rect.width = size
            self.main_minimap_rect.height = size
            self.main_minimap_rect.topleft = SCREEN_SIZE[0] - 100, SCREEN_SIZE[1] - 100
            rects, colors = self.setup_minimap(self.main_minimap_rect.x, self.main_minimap_rect.y)
            self.draw_minimap(rects, colors, screen)

    def draw_enemies(self, screen):
        for enemy in self.enemies:
            enemy.draw_enemy(screen)

    def draw_events(self, screen):
        for event in self.events:
            event.draw(screen,self.trader_menu)

    def update_events(self, player):
        for event in self.events:
            if event.dialogue_window.active == False:
                if event.rect.colliderect(
                        player.rect):
                    event.dialogue_window.active = True
                    event.player = player

    def update_enemy(self, player_rect):
        for enemy in self.enemies[:]:
            enemy.move(player_rect.center, self.local_objects)
            if player_rect.colliderect(enemy.rect):
                self.enemies.remove(enemy)
        if self.type_ == "Боёвка":
            current_timer = pygame.time.get_ticks()
            print(self.start_timer + 60000, current_timer, self.enemy_hits, len(self.enemies), self.used)
            if len(self.enemies) == 0:
                if not self.used:
                    self.room_open()
            elif self.start_timer + 60000 < current_timer and self.enemy_hits <= 0:
                if not self.used:
                    self.room_open()

    def items_updated(self, screen, player):
        for item in self.items_list:
            item.draw(screen)
        player.pickup_item(self.items_list)
        player.drop_item(self.items_list)

    def room_open(self):
        self.used = True
        walls = [(0, 9), (0, 10), (0, 11), (-1, 9), (-1, 10), (-1, 11), (5, 0), (5, -1), (6, 0), (6, -1)]
        for wall in walls:
            y_wall, x_wall = wall
            self.local_map[y_wall][x_wall] = " "

        self.local_objects = self.setup_local_map(self.local_map)

    def setup_minimap(self, x, y, scale=1, tray=False):
        size = 20 * scale
        gap = 10 * scale

        rects_list = []
        colors_list = []

        if tray:
            for row in range(self.tile_width):
                for column in range(self.tile_height):
                    rect = pygame.Rect(x + size * row + gap * row, y + size * column + gap * column, size, size)
                    rects_list.append(rect)

                    room_type = self.room_type(self.map[column - 1][row - 1][0])
                    colors_list.append(room_type)
            room_x, room_y = check_room_existing(self.x + 1, self.y + 1, self.tile_width, self.tile_height)
            x = x + (size * room_x) + (gap * room_x)
            y = y + (size * room_y) + (gap * room_y)
            player_rect = pygame.Rect(x + 10, y + 10, 20, 20)
            rects_list.append(player_rect)
            colors_list.append((50, 50, 50))
        else:
            top = pygame.Rect(x + size + gap, y, size, size)
            bottom = pygame.Rect(x + size + gap, y + size * 2 + gap * 2, size, size)
            left = pygame.Rect(x, y + size + gap, size, size)
            right = pygame.Rect(x + size * 2 + gap * 2, y + size + gap, size, size)
            middle = pygame.Rect(x + size + gap, y + size + gap, size, size)

            x_left, x_right = self.x - 1, self.x + 1
            y_up, y_down = self.y - 1, self.y + 1

            x_left, y_up = check_room_existing(x_left, y_up, self.tile_width, self.tile_height)
            x_right, y_down = check_room_existing(x_right, y_down, self.tile_width, self.tile_height)
            rects_list.extend([top, bottom, left, right, middle])
            colors_list.extend([self.room_type(self.map[y_up][self.x][0]),
                                self.room_type(self.map[y_down][self.x][0]),
                                self.room_type(self.map[self.y][x_left][0]),
                                self.room_type(self.map[self.y][x_right][0]),
                                self.room_type(self.map[self.y][self.x][0]), ])

        return rects_list, colors_list

    def draw_minimap(self, rects, colors, screen):
        for index in range(len(rects)):
            pygame.draw.rect(screen, colors[index], rects[index])

    def room_type(self, type_):
        if type_ == "Отдых":
            return (0, 255, 0)
        elif type_ == "Боёвка":
            return (255, 0, 0)
        elif type_ == "Родник":
            return (0, 0, 255)
        elif type_ == "Торговец":
            return (255, 255, 0)
        elif type_ == "Загадка":
            return (150, 0, 255)
        elif type_ == "Табличка":
            return (100, 100, 100)
        else:
            return (0, 0, 0)

    def setup_room_text(self):
        text = f"Room: {self.room}"
        self.text = FONT20.render(text, True, (255, 215, 0))
        self.text_rect = self.text.get_rect()
        self.text_rect.topright = SCREEN_SIZE[0] - 10, 10
        self.text_bg = self.text_rect.copy()
        self.text_bg.width += 5
        self.text_bg.height += 5
        self.text_bg.center = self.text_rect.center

    def update(self):
        pass

    def setup(self):
        pass

    def setup_local_map(self, map):
        x = 0
        y = 0
        # if self.type_ == "Боёвка":
        #     if not self.used:
        #         walls = [(0, 9), (0, 10), (0, 11), (-1, 9), (-1, 10), (-1, 11), (5, 0), (5, -1), (6, 0), (6, -1)]
        #         for wall in walls:
        #             y_wall, x_wall = wall
        #             map[y_wall][x_wall] = "W"

        objects = []
        texture_random = random.choice(["1.png", "2.png", "3.png"])
        for row in map:
            temp = []
            for column in row:
                if self.used:
                    if column in ["E", "Q", "T", "r", "K", ]:
                        column = " "

                if column == "E":
                    self.enemies.append(Enemy((x, y), "Орк"))
                if column in ["Q", "T", "r", "K", "N"]:
                    self.events.append(Object((x, y), column))
                object_ = Tile(x, y, column, texture_random)
                if not object_.color:
                    x += TILE_WIDTH
                    continue
                temp.append(object_)
                x += TILE_WIDTH
            y += TILE_HEIGHT
            x = 0
            objects.append(temp)
        return objects

    def draw_local_map(self, screen):
        for row_index, row in enumerate(self.local_objects):
            for column_index, column in enumerate(row):
                column.draw(screen)

class Window_map:
    def __init__(self, current_window):
        self.rooms = None
        self.color = (100, 100, 100)

    def draw(self, screen):
        screen.fill(self.color)
