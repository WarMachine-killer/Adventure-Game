import pygame


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
        self.bg_inventory = pygame.Rect(120, 540-330, 660, 660)
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
        self.coins = 0

    def draw(self, screen, ):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.show_inventory:
            pygame.draw.rect(screen, (200, 200, 200), self.bg_inventory,border_radius=40)
            self.draw_inventory_items(screen)
            print(self.coins)

    def draw_inventory_items(self, screen):
        for item in self.inventory.values():
            if not isinstance(item, tuple):
                item.draw(screen)

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
    def move(self, obstacles):
        self.rect.centerx += self.speedx
        self.collide(obstacles, self.speedx, 0)
        self.rect.centery += self.speedy
        self.collide(obstacles, 0, self.speedy)

    def collide(self, obstacles, x_vel, y_vel):
        for object_ in obstacles:
            for wall_ in object_:
                wall = wall_.rect
                if self.rect.colliderect(wall):
                    if not wall_.interactive:
                        if x_vel > 0:
                            self.rect.right = wall.left
                        if x_vel < 0:
                            self.rect.left = wall.right
                        if y_vel > 0:
                            self.rect.bottom = wall.top
                        if y_vel < 0:
                            self.rect.top = wall.bottom

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

