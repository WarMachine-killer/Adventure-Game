import pygame
import math

class Enemy:
    def __init__(self,pos,name):
        self.name = name
        self.rect = pygame.Rect(pos,(30,30))
        self.parameters(name)
        self.color = "orange"

    def parameters(self,name):
        if name == "Орк":
            self.hp = 200
            self.armor = 30
            self.dmg = 35
            self.dropped_gold = 90
            self.heal = False
            self.speed = 4
        elif name == "Демон":
            self.hp = 300
            self.armor = 20
            self.dmg = 35
            self.dropped_gold = 120
            self.heal = True
            self.speed = 4
        elif name == "Гоблин":
            self.hp = 140
            self.armor = 40
            self.dmg = 20
            self.dropped_gold = 50
            self.heal = False
            self.speed = 4
        elif name == "Стражники":
            self.hp = 220
            self.armor = 35
            self.dmg = 30
            self.dropped_gold = 100
            self.heal = False
            self.speed = 4

    def draw_enemy(self,screen):
        pygame.draw.rect(screen,self.color,self.rect)

    def move(self,player_pos,walls):
        speedx,speedy = self.trace(player_pos)
        self.rect.centerx += speedx
        self.collide(walls, speedx, 0)
        self.rect.centery += speedy
        self.collide(walls, 0, speedy)
    def trace(self,target):
        x1, y1 = self.rect.center
        x2, y2 = target

        dx = x2 - x1
        dy = y1 - y2
        if dx == 0:
            dx = 1
        if dy == 0:
            dy = 1
        r = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
        sin = dy / r
        cos = dx / r
        speedx = (cos * self.speed)
        speedy = (sin * self.speed)
        return speedx,-speedy

    def collide(self, obstacles, x_vel, y_vel):
        for object_ in obstacles:
            for wall in object_:
                wall = wall.rect
                if self.rect.colliderect(wall):
                    if x_vel > 0:
                        self.rect.right = wall.left
                    if x_vel < 0:
                        self.rect.left = wall.right
                    if y_vel > 0:
                        self.rect.bottom = wall.top
                    if y_vel < 0:
                        self.rect.top = wall.bottom