import pygame
import os

pygame.init()

size_window = (1024, 700)
size_tower1 = (50, 100)
size_tower2 = (60, 110)
size_tower3 = (80, 130)
size_tower4 = (110, 160)
size_mob = (60, 60)
size_miniboss = (90, 90)
size_boss = (120, 120)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

path = [
    (0, 216),
    (680, 216),
    (680, 116),
    (930, 116),
    (930, 390),
    (740, 390),
    (740, 480),
    (95, 480),
    (95, 700)
]

FPS = 60

abs_path = os.path.dirname(os.path.abspath(__file__))
image_folder = os.path.join(abs_path, "image")

background_image = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, "background.png")), size_window)
menu_background_image = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, "menu_background.png")), size_window)

start_button_image = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, "start_button.png")), (250, 80))
exit_button_image = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, "exit_button.png")), (250, 80))
leave_button_image = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, "leave_button.png")), (100, 50))

mob_image = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, "mob.png")), size_mob)
miniboss_image = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, "mob.png")), size_miniboss)
boss_image = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, "mob.png")), size_boss)

tower_image_1 = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, "tower1.png")), size_tower1)
tower_image_2 = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, "tower2.png")), size_tower2)
tower_image_3 = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, "tower3.png")), size_tower3)
tower_image_4 = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, "tower3.png")), size_tower4)

tower_images = {
    1: tower_image_1,
    2: tower_image_2,
    3: tower_image_3,
    4: tower_image_4
}