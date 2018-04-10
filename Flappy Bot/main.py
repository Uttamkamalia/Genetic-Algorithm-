import pygame,random,sys
import numpy as np
from pygame.locals import *


class Chromo:

    def __init__(self):
        self.w1_row = 3
        self.w1_col = 5
        self.w2_row = 5
        self.w2_col = 1

        self.genes=[2*np.random.random((self.w1_row,self.w1_col)) - 1 , 2 * np.random.random((self.w2_row, self.w2_col)) - 1]
        self.fitness = 0

    def get_genes(self):
        return self.genes
    def get_fitness(self):
        return self.fitness
    def set_genes(self,gene):
        self.genes = gene
    def set_fitness(self,x):
        self.fitness = x




class game:

    def __init__(self):

        self.display_width = 400
        self.display_height = 400
        self.bird_size = 30
        self.pipe_width = 50
        self.pipe_height = 400
        self.fps = 1000
        self.pipe_speed = 4
        self.bird_speed = 10
        self.bird_x = 100
        self.bird_y = 200
        self.pipe_x = self.display_width
        self.pipe_y = random.randint(-350,-100)

        self.pipe2_y = self.pipe_height + self.pipe_y + self.bird_size+50
        self.y_change = 0
        self.block = 5
        self.score = 0
        self.game_counter = 0
        self.screen = pygame.display.set_mode((self.display_width,self.display_height))

        self.bird1 = pygame.transform.scale(pygame.image.load('assets/birdd.png'), (self.bird_size, self.bird_size))
        self.bird2 = pygame.transform.scale(pygame.image.load('assets/birdh.png'), (self.bird_size, self.bird_size))
        self.bird3 = pygame.transform.scale(pygame.image.load('assets/birdu.png'), (self.bird_size, self.bird_size))
        self.dpipe = pygame.transform.scale(pygame.image.load('assets/upipe.png'), (self.pipe_width, self.pipe_height))
        self.upipe = pygame.transform.scale(pygame.image.load('assets/dpipe.png'), (self.pipe_width, self.pipe_height))
        self.back_ground = pygame.transform.scale(pygame.image.load('assets/back.png'), (self.display_width, self.display_height))

        self.birds = [self.bird1,self.bird2,self.bird3]
        self.gameExit = False
        self.dead = False
        self.clock = pygame.time.Clock()

        # BOTS
        self.pop_size = 10
        self.bots = [Chromo() for _ in range(self.pop_size)]
        self.elite_num = 2
        self.mutate_ratio = 0.8
        self.global_score=0
        self.curr_bot_fit = 0


    def mate(self,par1,par2):
         temp = Chromo()
         baby = temp.get_genes()
         for i in range(3):
             for j in range(5):
                if np.random.random() <= 0.5:
                    baby[0][i][j] = par1[0][i][j]
                else :
                    baby[0][i][j] = par2[0][i][j]

         for i in range(5):
             for j in range(1):
                if np.random.random() <= 0.5:
                    baby[1][i][j] = par1[1][i][j]
                else :
                    baby[1][i][j] = par2[1][i][j]
         temp.set_genes(baby)
         return temp

    def mating(self):
        self.bots.sort(key=lambda x:x.get_fitness(),reverse= True)
        temp = [self.bots[i] for i in range(self.elite_num)]
        for candid in range(self.elite_num,self.pop_size):

            baby = self.mate(temp[0].get_genes(),temp[1].get_genes())
            temp.append(baby)
        self.bots = temp

    def get_mutate(self,candid):
        baby = candid.get_genes()
        for i in range(3):
            for j in range(5):
                if np.random.random() <= self.mutate_ratio:
                    baby[0][i][j] += random.uniform(-0.5,0.5)

        for i in range(5):
            for j in range(1):
                if np.random.random() <= self.mutate_ratio:
                    baby[1][i][j] += random.uniform(-0.5,0.5)

        candid.set_genes(baby)
        return candid

    def mutate(self):
        mutated = [self.bots[i] for i in range(self.elite_num)]
        for candid in range(self.elite_num,self.pop_size):
            mutated.append(self.get_mutate(self.bots[candid]))
        self.bots = mutated

    def evole(self):
        self.mating()
        self.mutate()



    def sigmoid(self,x):
        return 1/(1+ np.exp(-x))

    def predict(self,input,wgt1,wgt2):

        a1 = self.sigmoid(np.dot(input,wgt1))
        return self.sigmoid(np.dot(a1,wgt2)).tolist()





    def game_exit(self):
        self.dead = True
        self.global_score = self.score
        self.score = 0
        self.bird_x = 100
        self.bird_y = 200

        self.pipe_x = self.display_width
        self.pipe_speed = 0
        #self.fps = 10
        self.pipe_speed = 5
        self.bird_speed = 10



    def bird_object(self):


        dpipe_rect = pygame.Rect(int(self.pipe_x),int(self.pipe_y),int(self.dpipe.get_width()),int(self.dpipe.get_height()))
        upipe_rect = pygame.Rect(self.pipe_x, self.pipe2_y, int(self.upipe.get_width()), int(self.upipe.get_height()))
        bird_rect = pygame.Rect(self.bird_x, self.bird_y, int(self.bird1.get_width()), int(self.bird1.get_height()))

        if self.bird_y < 0 or self.bird_y > (self.display_height - self.bird_size - 5):
            self.game_exit()

        if dpipe_rect.colliderect(bird_rect) or upipe_rect.colliderect(bird_rect):
            self.game_exit()

        self.bird_y += self.y_change
        self.y_change = 0
        self.screen.blit(self.birds[self.game_counter % len(self.birds)],(self.bird_x,self.bird_y))

    def pipe_object(self):

        if self.pipe_x <= -5 :
            self.pipe_x = self.display_width
            self.pipe_y = random.randint(-350, -100)
            self.pipe2_y = self.pipe_height + self.pipe_y + self.bird_size + 50
            self.score +=1

        self.screen.blit(self.upipe,(self.pipe_x,self.pipe_y))
        self.screen.blit(self.dpipe,(self.pipe_x,self.pipe2_y))

        self.pipe_x -= self.pipe_speed

    def run(self,player = None):
        incrmnt = False
        self.dead = False
        self.curr_bot_fit = 0
        max_fitnes = 0
        self.game_counter = 0


        while not self.dead:

            self.screen.blit(self.back_ground, (0, 0))
            #pygame.display.set_caption("Birdie...          Score : " + str(self.score))

            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    sys.exit()
                '''
                if events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_UP:
                        self.y_change = -self.bird_speed

                    if events.key == pygame.K_DOWN:
                        self.y_change = self.bird_speed
                '''
            temp = abs(self.bird_y - (self.pipe_y + (self.pipe_height + self.bird_size + 50)/2 )) + self.score
            if temp==0:
                temp =1
            factor = 400/temp
            if factor > max_fitnes:
                max_fitnes = factor
                self.curr_bot_fit +=1


                self.curr_bot_fit -=1

            if player != None:
                inputs = np.array([self.bird_y, self.pipe_x, self.pipe_y])
                weights = player.get_genes()
                decision = self.predict(inputs, weights[0], weights[1])[0]

                if decision >=0.5:
                    self.y_change = -self.bird_speed
                    pygame.display.set_caption("Birdie...  UP         Score : " + str(self.score))

                else:
                    self.y_change = self.bird_speed
                    pygame.display.set_caption("Birdie...  DOWN       Score : " + str(self.score))

            self.bird_object()
            self.pipe_object()
            pygame.display.update()
            self.clock.tick(self.fps)
            '''
            if self.score % 5 == 0 and self.score != 0 and not incrmnt:
                incrmnt = True
                #self.fps += 1
                #self.bird_speed += 2
            if self.score % 5 != 0:
                incrmnt = False
                '''
            self.game_counter += 1



        return [self.global_score,self.game_counter + self.curr_bot_fit]

    def train_bot(self):
        gen = 1
        while self.global_score <=5:
            count = 1
            for candid in self.bots:
                score,fit = self.run(candid)
                candid.set_fitness(fit+(score)*10)
                print("Gen: ",gen,"     bot: ",count,"  fitness: ",fit+score,"   score: ",score)
                count += 1

            gen += 1
            print("\n")

            self.evole()
        self.bots.sort(key=lambda x: x.get_fitness(), reverse=True)

        np.save("flappy.npy",self.bots[0].get_genes())
        print("Training complete...")



game().train_bot()


