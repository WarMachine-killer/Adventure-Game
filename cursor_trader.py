import pygame
import sys
from settings import S_WIDTH, S_HEIGHT
import random
from settings import FONT_COMIC_32,FONT_CALIBRI_50
from functions import json_read
import math

pygame.init()


class Trader_menu:
    def __init__(self):
        math_width = (S_WIDTH - S_WIDTH / 8)
        math_height = (S_HEIGHT - S_WIDTH / 8)
        math_head = (S_WIDTH / 8)
        self.main_rect = pygame.Rect(0, 0, math_width, math_height)
        self.main_rect.center = (S_WIDTH / 2, S_HEIGHT / 2)
        self.head = Interactive_face(math_head)
        self.sub_rect = pygame.Rect(0, 0, (math_width / 2 - 20), (math_height - 40))
        self.sub_rect.left = self.main_rect.left + 20
        self.sub_rect.top = self.main_rect.top + 20
        self.balance_rect = pygame.Rect((0,0),(math_width/6,math_height/8))
        self.balance_rect.topright = self.main_rect.topright
        self.balance_rect.right = self.main_rect.right - 20
        self.balance_rect.top = self.main_rect.top + 20
        self.info = {
            "name": "Название",
            "price": "Цена",
            "value": "Значение",
            "trader_have": "Наличие",
            "description": "Описание",
            "items": None,
            "hitbox": None
        }
        self.rows_name = Trader_menu_row(self.sub_rect.topleft, self.info, None)
        self.weapons = json_read("weapons.json")
        y = self.sub_rect.top + 40
        for index, weapon in enumerate(self.weapons):
            weapon = Trader_menu_row((self.sub_rect.left, y), weapon, None)
            y += 45
            self.weapons[index] = weapon
        self.player_balance = 10000
        self.can_be_bought = True
        self.bought_endtimer = 0
        self.coin_image = pygame.image.load("images/trader/goblicoin.png")
        self.coin_image = pygame.transform.smoothscale(self.coin_image,(self.coin_image.get_width()/2,self.coin_image.get_height()/2))
        self.coin_rect = self.coin_image.get_rect(x=self.balance_rect.x + 15,centery=self.balance_rect.centery)

    def draw(self, screen):
        self.bought_endtimer += clock.get_time()
        pygame.draw.rect(screen, (100, 100, 100), self.main_rect, border_radius=20)
        self.head.draw(screen)
        self.draw_balance(screen)
        pygame.draw.rect(screen, (80, 80, 80), self.sub_rect, border_radius=10)
        self.rows_name.draw(screen)
        for weapon in self.weapons:
            weapon.draw(screen)
        for prompt in self.weapons[::-1]:
            if prompt.name != "Название":
                x, y = pygame.mouse.get_pos()
                if prompt.extra_glow and prompt.start_glow + 500 < pygame.time.get_ticks():
                    prompt.extra_glow = False
                    prompt.start_glow_bull = True
                if prompt.rect.collidepoint(x, y):
                    prompt.glow = True
                    click = pygame.mouse.get_pressed()
                    prompt.prompt.draw(screen, (x, y))
                    self.head.mouth_type = "smiling"
                    if click[0] and self.bought_endtimer in range(500, 1000):
                        if self.player_balance >= prompt.price and prompt.trader_have >= 1 and not prompt.extra_glow:
                            prompt.extra_glow = True
                            self.head.mouth_type = "exciting"
                            self.player_balance -= prompt.price
                            prompt.trader_have -= 1
                            self.bought_endtimer = 0
                if prompt.extra_glow:
                    self.head.mouth_type = "exciting"

        if self.bought_endtimer >= 1000:
            self.bought_endtimer = 500

    def draw_balance(self,screen):
        pygame.draw.rect(screen,(80, 80, 80),self.balance_rect,border_radius=10)
        screen.blit(self.coin_image,self.coin_rect)
        self.draw_balance_text(screen)
    def draw_balance_text(self,screen):
        text_image = FONT_CALIBRI_50.render(str(self.player_balance), True, (255, 215, 0))
        text_rect = text_image.get_rect(x=self.balance_rect.centerx,centery=self.balance_rect.centery)
        screen.blit(text_image,text_rect)

class Trader_menu_row:
    def __init__(self, pos, info, item_inv):
        self.x, self.y = pos
        self.rect = pygame.Rect(pos, (800, 30))
        self.rect.y += 15
        self.rect.x += 10
        self.glow = False
        self.extra_glow = False
        self.name = info["name"]
        self.price = info["price"]
        self.description = info["description"]
        print(info)
        if info.get('items') == "potion":
            self.trader_have = random.randint(1, 3)
        else:
            self.trader_have = 1
        self.hitbox = info["hitbox"]
        self.value = info["value"]
        if self.name != "Название":
            self.prompt = Interactive_desc(info["hitbox"], self.description)
        self.start_glow = 0
        self.start_glow_bull = True

    def draw_text(self, text, text_rect, pos, screen):
        text_rect.left = pos[0]
        text_rect.centery = pos[1]
        screen.blit(text, text_rect)

    def draw(self, screen):
        if self.name == "Название":
            trader_have = "Количество"
        else:
            trader_have = self.trader_have
        pos_list = [20,
                    330,
                    520,
                    671]
        text_list = [self.name, self.value, self.price, trader_have]
        gap = 30
        self.draw_bg(screen)
        for index, text in enumerate(text_list):
            text = (FONT_COMIC_32.render(str(text), True, (255, 215, 0)))
            text_rect = text.get_rect()
            self.draw_text(text, text_rect, (self.x + pos_list[index], self.y + gap), screen)

    def draw_bg(self, screen):
        if not self.glow:
            pygame.draw.rect(screen, (70, 70, 70), self.rect, border_radius=7)
        else:
            pygame.draw.rect(screen, (75, 75, 75), self.rect, border_radius=7)
        if self.extra_glow:
            pygame.draw.rect(screen, (100, 100, 75), self.rect, border_radius=7)
            if self.start_glow_bull:
                print("Таймер начался")
                self.start_glow = pygame.time.get_ticks()
                self.start_glow_bull = False
        self.glow = False


class Interactive_face:
    def __init__(self, math_head):
        self.head_rect = pygame.Rect(0, 0, math_head * 1.3, math_head * 1.3)
        self.head_rect.center = (S_WIDTH / 2 + math_head * 2, S_HEIGHT / 2)
        self.eye_rect = pygame.Rect((0, 0), (120, 100))
        self.eye_rect.center = self.head_rect.center
        self.mouth_rect = pygame.Rect((0, 0), (120, 156))
        self.black = (0, 0, 0)
        self.mouth_type = "normal"

    def draw(self, screen):
        self.update()
        pygame.draw.circle(screen, yellow, self.head_rect.center, self.head_rect.width / 1.3)
        if self.mouth_type == "exciting":
            pygame.draw.circle(screen, self.black, (self.eye_rect.centerx, self.eye_rect.centery + 130), 50, 5)
        elif self.mouth_type == "smiling":
            pygame.draw.circle(screen, self.black, (self.eye_rect.centerx, self.eye_rect.centery + 90), 60, 5)
            pygame.draw.rect(screen, yellow, self.mouth_rect)
        elif self.mouth_type == "normal":
            pygame.draw.line(screen, self.black, (self.eye_rect.left - 20, self.eye_rect.bottom + 40),
                             (self.eye_rect.right + 20, self.eye_rect.bottom + 40), width=5)
        self.mouth_type = "normal"
        pygame.draw.line(screen, self.black, (self.eye_rect.topleft), (self.eye_rect.bottomleft), 5)
        pygame.draw.line(screen, self.black, (self.eye_rect.topright), (self.eye_rect.bottomright), 5)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.eye_rect.center = mouse_pos
        if self.eye_rect.left <= self.head_rect.left:
            self.eye_rect.left = self.head_rect.left
        if self.eye_rect.right >= self.head_rect.right:
            self.eye_rect.right = self.head_rect.right
        if self.eye_rect.top <= self.head_rect.top:
            self.eye_rect.top = self.head_rect.top
        if self.eye_rect.bottom >= self.head_rect.bottom:
            self.eye_rect.bottom = self.head_rect.bottom
        self.mouth_rect.center = self.eye_rect.center


class Interactive_desc:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.text_color = (0, 0, 0)
        self.main_rect = pygame.Rect((0, 0), (400, 160))
        self.image = pygame.image.load(f"images/weapons/{self.name}")
        self.scale = 0.5
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * self.scale,
                                                         self.image.get_height() * self.scale))
        self.image_rect = self.image.get_rect()
        self.text_images = self.prepare_text(self.description)

    def draw(self, screen, pos):
        self.main_rect.topleft = pos
        self.image_rect.topleft = self.main_rect.topleft
        pygame.draw.rect(screen, (70, 70, 70), self.main_rect, border_radius=15)
        screen.blit(self.image, self.image_rect)
        self.draw_text(pos, screen)

    def draw_text(self, pos, screen):
        y = 0
        for text_image in self.text_images:
            text_rect = text_image.get_rect(x=pos[0] + self.image.get_width(), y=pos[1] + 5 + y)
            y += text_rect.height + 5
            screen.blit(text_image, text_rect)

    def prepare_text(self, texts):
        text_list = []
        text_image, croped_text = self.check_text_len(texts)
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
        while width > self.main_rect.width - self.image.get_width() - 10:
            text = text.split()
            croped_text.insert(0, text.pop(-1))
            text = " ".join(text)
            text_image = FONT_COMIC_32.render(text, True, self.text_color)
            width = text_image.get_width()
        return text_image, croped_text


class Item:
    def __init__(self, info, x, y):
        self.can_use = info["can_use"]
        self.name = info["name"]
        self.price = info["price"]
        self.description = info["description"]
        self.exclusive = info["exclusive"]
        self.hitbox = info["hitbox"]
        self.value = info["value"]
        if "random" in info:
            self.random = info["random"]
        self.in_inventory = False
        image = pygame.image.load("images/" + self.hitbox)
        self.in_inventory_image = image.copy()
        image_width, image_height = self.in_inventory_image.get_size()
        scale = 0.5
        self.on_ground_image = pygame.transform.scale(image.copy(),
                                                      (image_width * scale, image_height * scale))
        self.rect = self.on_ground_image.get_rect(centerx=x, centery=y)

    def draw(self, screen):
        if self.in_inventory:
            screen.blit(self.in_inventory_image, self.rect)
        else:
            screen.blit(self.on_ground_image, self.rect)

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.draw_frame(screen)

    def update_rect(self, temp=False):
        if temp:
            self.rect = self.on_ground_image.get_rect(x=self.rect.x, y=self.rect.y)
        else:
            self.rect = self.in_inventory_image.get_rect(x=self.rect.x, y=self.rect.y)

    def __repr__(self):
        return self.name

    def draw_frame(self, screen):
        pygame.draw.rect(screen, "green", self.rect, 5)


class Player:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (123, 15, 86)
        self.speed = 5
        self.speedx = 0
        self.speedy = 0
        wall_gap = 20
        gap = 10
        self.show_inventory = False
        self.translator = False
        self.teleporter = False  # первые 3 секунды игроку показывается текст куда телепортироваться, а потом он должен нажать на определённую комнату
        self.bg_inventory = pygame.Rect(120, 120, 660, 660)
        self.inventory = {1: (wall_gap + 0 + self.bg_inventory.x, wall_gap + 0 + self.bg_inventory.y),
                          2: (wall_gap + 200 + self.bg_inventory.x + gap, wall_gap + 0 + self.bg_inventory.y),
                          3: (wall_gap + 400 + self.bg_inventory.x + gap * 2, wall_gap + 0 + self.bg_inventory.y),
                          4: (wall_gap + 0 + self.bg_inventory.x, wall_gap + 200 + self.bg_inventory.y + gap),
                          5: (wall_gap + 200 + self.bg_inventory.x + gap, wall_gap + 200 + self.bg_inventory.y + gap),
                          6: (
                              wall_gap + 400 + self.bg_inventory.x + gap * 2,
                              wall_gap + 200 + self.bg_inventory.y + gap),
                          7: (wall_gap + 0 + self.bg_inventory.x, wall_gap + 400 + self.bg_inventory.y + gap * 2),
                          8: (
                              wall_gap + 200 + self.bg_inventory.x + gap,
                              wall_gap + 400 + self.bg_inventory.y + gap * 2),
                          9: (wall_gap + 400 + self.bg_inventory.x + gap * 2,
                              wall_gap + 400 + self.bg_inventory.y + gap * 2),
                          }

    def draw(self, screen, ):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.show_inventory:
            pygame.draw.rect(screen, (200, 200, 200), self.bg_inventory)
            self.draw_inventory_items(screen)

    def draw_inventory_items(self, screen):
        for item in self.inventory.values():
            if not isinstance(item, tuple):
                item.draw(screen)

    def move(self, obstacles):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy

    def pickup_item(self, item_list):
        for item in item_list:
            if self.rect.colliderect(item.main_rect):
                empty_place, num = self.check_empty_places()
                if empty_place:
                    item.in_inventory = True
                    x, y = self.inventory[num][0], self.inventory[num][1]
                    item.update_rect()
                    item.main_rect.x, item.main_rect.y = x, y
                    self.inventory[num] = item
                    item_list.remove(item)

    def drop_item(self, item_list):
        if self.show_inventory:
            for key, item in self.inventory.items():
                if not isinstance(item, tuple):
                    mouse_pos = pygame.mouse.get_pos()
                    if item.rect.collidepoint(mouse_pos):
                        keys = pygame.key.get_pressed()
                        print(keys[pygame.K_r])
                        if keys[pygame.K_r]:
                            x, y = self.rect.right + 50, self.rect.top - 50
                            inv_x, inv_y = item.rect.x, item.rect.y
                            item.update_rect(True)
                            item.in_inventory = False
                            item.rect.x, item.rect.y = x, y
                            new_item = self.inventory[key]
                            self.inventory[key] = inv_x, inv_y
                            item_list.append(new_item)

    def check_empty_places(self):
        for num, item in self.inventory.items():
            if isinstance(item, tuple):
                return True, num
        return False, None

if __name__ == '__main__':
    w, h = (1920, 1080)
    screensize = w, h
    color = (200, 55, 86)
    yellow = (240, 240, 0)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(screensize)
    menu = Trader_menu()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(color)
        menu.draw(screen)
        pygame.display.flip()
        clock.tick(60)
