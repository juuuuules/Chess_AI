import pygame

import os

pygame.init()

screen = pygame.display.set_mode((500, 500))

screen.fill((255, 255, 255))

while True:

    screen.fill((255, 255, 0))

    n = 0

    for file in os.scandir("../images"):
        if file.is_file():
            image = pygame.image.load(file.path)

            screen.blit(image, (n, n))
        n += 40

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.update()