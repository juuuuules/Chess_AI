import pygame

import os

pygame.init()

screen = pygame.display.set_mode((500, 500))

screen.fill((255, 255, 255))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    image = pygame.image.load("../images/bB.png")
    image = pygame.transform.scale(image, (500, 500))

    screen.blit(image, (0, 0))

    pygame.display.update()

