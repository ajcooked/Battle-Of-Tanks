# Author: Dalagon, Toledo, Ramos, Artillo, Paitan
# Date:12/19/2025

import pygame
import random

pygame.init()

screen = pygame.display.set_mode((1080, 800))

# Gameloop
running = True
while running:
    
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()