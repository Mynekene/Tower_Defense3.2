from data import *
import math

class Bullet:
    def __init__(self, x, y, target, damage=10, speed=8):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.speed = speed
        self.radius = 5
        dx = target.x - x
        dy = target.y - y
        distance = math.hypot(dx, dy)
        self.dx = dx / distance
        self.dy = dy / distance

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def draw(self, window):
        pygame.draw.circle(window, (255, 255, 0), (int(self.x), int(self.y)), self.radius)

    def has_hit_target(self):
        return math.hypot(self.x - self.target.x, self.y - self.target.y) < self.radius + self.target.radius

class Tower:
    def __init__(self, x, y, tower_type):
        self.x = x
        self.y = y
        self.type = tower_type
        self.timer = 0
        self.bullets = []
        self.price = {1: 50, 2: 200, 3: 800, 4: 3200}[tower_type]
        self.damage = {1: 10, 2: 15, 3: 25, 4: 50}[tower_type]
        self.cooldown = {1: 40, 2: 30, 3: 25, 4: 50}[tower_type]
        self.range = {1: 150, 2: 300, 3: 400, 4: 300}[tower_type]

    def attack(self, mobs):
        if self.timer > 0:
            self.timer -= 1
        else:
            for mob in mobs:
                dist = math.hypot(mob.x - self.x, mob.y - self.y)
                if dist <= self.range:
                    self.bullets.append(Bullet(self.x, self.y, mob, self.damage))
                    self.timer = self.cooldown
                    break

    def update_bullets(self, mobs):
        new_bullets = []
        for bullet in self.bullets:
            bullet.move()
            if bullet.target in mobs and bullet.has_hit_target():
                bullet.target.hp -= bullet.damage
            else:
                new_bullets.append(bullet)
        self.bullets = new_bullets

    def draw(self, window):
        image = tower_images[self.type]
        rect = image.get_rect(center=(self.x, self.y))
        window.blit(image, rect)
        for bullet in self.bullets:
            bullet.draw(window)

class Mob:
    def __init__(self, path, wave, mob_type):
        self.path = path
        self.current_point = 0
        self.x, self.y = path[0]
        self.mob_type = mob_type
        self.radius = 30
        if mob_type == "normal":
            self.hp = 50 + wave * 5
            self.speed = 1
        elif mob_type == "miniboss":
            self.hp = 200 + wave * 10
            self.speed = 0.75
        elif mob_type == "boss":
            self.hp = 500 + wave * 20
            self.speed = 0.5

    def move(self):
        if self.current_point + 1 >= len(self.path):
            return
        tx, ty = self.path[self.current_point + 1]
        dx = tx - self.x
        dy = ty - self.y
        distance = math.hypot(dx, dy)
        if distance < self.speed:
            self.x = tx
            self.y = ty
            self.current_point += 1
        else:
            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed

    def draw(self, window):
        if self.mob_type == "normal":
            img = mob_image
            max_hp = 50
        elif self.mob_type == "miniboss":
            img = miniboss_image
            max_hp = 200
        elif self.mob_type == "boss":
            img = boss_image
            max_hp = 500
        rect = img.get_rect(center=(self.x, self.y))
        window.blit(img, rect)
        bar_width = 50
        bar_height = 6
        hp_ratio = self.hp / max_hp
        bar_x = self.x - bar_width // 2
        bar_y = self.y - rect.height // 2 - 10
        pygame.draw.rect(window, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(window, (0, 255, 0), (bar_x, bar_y, int(bar_width * hp_ratio), bar_height))
