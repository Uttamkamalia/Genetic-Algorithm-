import pygame
import random
import time
import math
import neu_net
import numpy as np
import blueprint as bp

network = neu_net.NeuralNet()

unit_block = 20
display_width = 30 * unit_block
display_height = 30 * unit_block

control_keys = [1, 0, 0, 0]

clock = pygame.time.Clock()
score = 0

# must code for game to initiate
pygame.init()
game_window = pygame.display.set_mode((display_height, display_width))
pygame.display.set_caption("NEW SNAKE GAME:::" + str(score))

pygame.display.update()

# game colour variables

blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)


# Game vriables


def snake(snakeList, head_size):
    for XY in snakeList[:-1]:
        pygame.draw.circle(game_window, green, (int(XY[0]), int(XY[1])), int(head_size))


def apple(pos, apple_size):
    # print("apple::::",(pos[0],pos[1]))
    pygame.draw.circle(game_window, red, (int(pos[0]), int(pos[1])), int(apple_size))
    # print("printed")


def game():
    gameExit = False
    head_size = unit_block / 2
    apple_radius = head_size
    score = 0
    FPS = 5
    block_diff = unit_block
    lead_x = display_width / 2
    lead_y = display_height / 2

    x_change = 0
    y_change = 0
    snake_List = []
    snake_length = 1

    apple_x = round(
        random.randrange(apple_radius, display_width - apple_radius, apple_radius) / unit_block) * unit_block
    apple_y = round(
        random.randrange(apple_radius, display_height - apple_radius, apple_radius) / unit_block) * unit_block
    if apple_x == 0:
        apple_x = apple_radius
    if apple_y == 0:
        apple_y = apple_radius
    apple_pos = [apple_x, apple_y]
    game_window.fill(white)

    while not gameExit:

        pygame.display.set_caption("NEW SNAKE GAME:::" + str(score))
        game_window.fill(white)
        pygame.draw.circle(game_window, green, (int(lead_x), int(lead_y)), int(head_size))
        pygame.display.update()

        distance = math.sqrt((lead_x - apple_x) ** 2 + (lead_y - apple_y) ** 2)
        inputs = map_chromo(inp, w1, w2, y)

        population = bp.Population(10)
        population = bp.GeneticAlgo.evolve(population)

        control_keys = network.predict(distance)

        # Snake controls

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change = -block_diff
                    x_change = 0

                if event.key == pygame.K_DOWN:
                    y_change = block_diff
                    x_change = 0

                if event.key == pygame.K_LEFT:
                    x_change = -block_diff
                    y_change = 0

                if event.key == pygame.K_RIGHT:
                    x_change = block_diff
                    y_change = 0

        lead_x += x_change
        lead_y += y_change

        print("apple::", (apple_pos), "   snake::", [lead_x, lead_y])
        # Checking boundary crash
        if lead_x <= head_size or lead_x >= display_width - head_size or lead_y <= head_size or lead_y >= display_height - head_size:
            print("boundary")
            gameExit = True
            return

        # Creating snake head
        snake_Head = []
        snake_Head.append(lead_x)
        snake_Head.append(lead_y)

        # checking conflict between snake and its head

        if x_change != 0 or y_change != 0:
            for every_Seg in snake_List[:-1]:
                if every_Seg == snake_Head:
                    print("conflict", every_Seg, " ", snake_Head)
                    gameExit = True

        snake_List.append(snake_Head)

        # Maintaining snake length

        if len(snake_List) > snake_length:
            del snake_List[0]

        # display snake and apple



        snake(snake_List, head_size)
        apple(apple_pos, apple_radius)
        pygame.display.update()

        # Checking if the apple is eaten

        if lead_x == apple_x and lead_y == apple_y:
            print("apple eaten")
            # apple_x = round(random.randrange(0, display_width - apple_radius) / (2 * apple_radius)) * (2 * apple_radius)
            # apple_y = round(random.randrange(0, display_height - apple_radius) / (2 * apple_radius)) * (2 * apple_radius)

            apple_x = round(
                random.randrange(apple_radius, display_width - apple_radius, apple_radius) / unit_block) * unit_block
            apple_y = round(
                random.randrange(apple_radius, display_height - apple_radius, apple_radius) / unit_block) * unit_block
            if apple_x == 0:
                apple_x = apple_radius
            if apple_y == 0:
                apple_y = apple_radius
            apple_pos = [apple_x, apple_y]

            score += 1
            snake_length += 1
            FPS += 1

        clock.tick(FPS)


game()






