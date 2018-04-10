import pygame
from pygame.locals import *
screen = pygame.display.set_mode((400,400))
img1 = pygame.transform.scale(pygame.image.load('assets/birdd.png'),(30,50))
img2 = pygame.transform.scale(pygame.image.load('assets/birdh.png'),(30,50))
img3 = pygame.transform.scale(pygame.image.load('assets/birdu.png'),(30,50))
pipeUp =  pygame.transform.scale(pygame.image.load('assets/upipe.png'),(30,200))
pipeDown =  pygame.transform.scale(pygame.image.load('assets/dpipe.png'),(30,250))
clock = pygame.time.Clock()
back = pygame.transform.scale(pygame.image.load('assets/back.png'),(400,400))



birds = [img1,img2,img3]
gamePlay = True

bird_x = 100
bird_y = 300
x_change = 0
y_change = 0

pipe_x = 370




motion = []
for i in range(300,0,-5):
    motion.append(i)

for i in range(0,300,5):
    motion.append(i)

print(motion)
i =0
while gamePlay:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gamePlay = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                y_change = -10

            if event.key == pygame.K_DOWN:
                y_change = 10

    bird_y += y_change
    print(y_change, "  ", bird_y)
    y_change = 0

    if pipe_x <=0:
        pipe_x = 370


    screen.blit(back, (0, 0))
    #screen.blit(birds[i%3],(100,motion[int(i%len(motion))]))
    screen.blit(birds[i % 3], (bird_x,bird_y))
    screen.blit(pipeUp,(pipe_x,300))
    screen.blit(pipeDown,(pipe_x,0))
    pipe_x -=10


    clock.tick(10)
    pygame.display.update()
    i = i+1



