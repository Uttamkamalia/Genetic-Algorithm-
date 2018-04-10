import pygame
import random
import time
import math
import neu_net
import numpy as np
import blueprint as bp


####genetic variables####

POP_SIZE = 10

network = neu_net.NeuralNet()
trainedGen = []
fitness_List = []
chromosomes = []
TARGET_FITNESS = 0

training_counter = 0
TRAIN =False


#########################


unit_block = 20
display_width =  30*unit_block
display_height = 30*unit_block

control_keys = np.array([1,0,0,0])

clock = pygame.time.Clock()
score = 0
fitness_factor = 0
early_dis = 0
best_slope = 0


# must code for game to initiate
pygame.init()
game_window = pygame.display.set_mode((display_height,display_width))
pygame.display.set_caption("NEW SNAKE GAME:::"+str(score))


pygame.display.update()


#game colour variables

blue = (0,0,255)
red = (255,0,0)
green = (0,255,0)
white = (255,255,255)
black = (0,0,0)



# Game vriables

def get_slope(x1,x2,y1,y2):
    up = y2-y1
    down = x2-x1
    if up == 0:
        return 0
    elif down == 0 :
        if y2>y1:
            return 10000000
        elif y1>=y2:
            return -10000000
    else:
        return up/down

def map_chromo(w1,w2,input_list):
    final = []

    for part in w1.tolist():
        for i in part:
            final.append(i)

    for part in w2.tolist():
        for i in part:
            final.append(i)

    #for i in y:
     #   final.append(i)

    final = final+input_list

    return final


def map_from_list(list_orig):
    lista = list_orig
    #dist = list1[0]
    #list1 = list1[1:]
    #length = list1[0]
    #list1 = list1[1:]
    count = 0
    w1 = []
    w2 = []
    output = []
    dim = network.get_dimen()
    #print("dims:::",dim,"   gese dim:::",len(lista))
    for i in range(0,dim[0]):
        temp=[]
        for j in range(0,dim[1]):
            count+=1
           # print("index for w1::: ",dim[1]*i + j)
            temp.append(lista[dim[1]*i + j])
        w1.append(temp)

    lista = lista[count:]

    for i in range(0, dim[2]):
        temp = []
        for j in range(0, dim[3]):
            count += 1
            #print("index for w2::: ", dim[3] * i + j)
            temp.append(lista[dim[3] * i + j])
        w2.append(temp)
    lista = lista[count:]

    w1 = np.array(w1)
    w2 = np.array(w2)

    output = [w1,w2]
    #print(output)
    return output










def snake(snakeList,head_size):

    for XY in snakeList[:-1]:
        pygame.draw.circle(game_window,green,(int(XY[0]),int(XY[1])),int(head_size))

def apple(pos,apple_size):
    #print("apple::::",(pos[0],pos[1]))
    pygame.draw.circle(game_window,red,(int(pos[0]),int(pos[1])),int(apple_size))
    #print("printed")

def game_trials():
    global chromosomes
    global fitness_List
    global TARGET_FITNESS
    global TRAIN
   #  global training_counter
    global score
    global fitness_factor
    global early_dis
    global best_slope
    global TARGET_FITNESS


    gameExit = False
    head_size = unit_block / 2
    apple_radius = head_size
    score = 0
    fitness_factor = 0


    FPS = 5
    block_diff = unit_block
    lead_x = display_width/2
    lead_y = display_height/2

    x_change = 0
    y_change = 0
    snake_List = []
    snake_length = 3
    '''
    apple_x = round(
        random.randrange(apple_radius, display_width - apple_radius, apple_radius) / unit_block) * unit_block
    apple_y = round(
        random.randrange(apple_radius, display_height - apple_radius, apple_radius) / unit_block) * unit_block
    if apple_x == 0:
        apple_x = apple_radius
    if apple_y == 0:
        apple_y = apple_radius
    '''
    apple_x = 26*unit_block
    apple_y = 2*unit_block
    apple_pos = [apple_x, apple_y]
    game_window.fill(white)
    #if TRAIN:
        #print("training count::", training_counter, " candidates::", trainedGen[training_counter])

    while not gameExit:


        game_window.fill(white)
        pygame.draw.circle(game_window, green, (int(lead_x), int(lead_y)), int(head_size))
        pygame.display.update()

        #############################################################################################################3
        ###############################################################################################################
        distance = math.sqrt((lead_x - apple_x) ** 2 + (lead_y - apple_y) ** 2)
        slope = get_slope(lead_x,apple_x,lead_y,apple_y) + 5

        if distance < early_dis:
            fitness_factor += 1
            best_slope = slope

        early_dis = distance
        X_list = [lead_x,lead_y,apple_x,apple_y,(lead_x-apple_x),(lead_y-apple_y),slope,(display_width-lead_x),(display_height-lead_y)]
        X_state = np.array(X_list)

        #weigths = network.get_weights()
        weigths = np.load("snake_intell.npy")




        if TRAIN :
            #print("INSIDE GAME TRAINED GEN")
            #for i in trainedGen:
            #   print(i)

            #print("length of candidates::",len(candidates))
            #print("Canditates:",training_counter,":::: ",candidates)
            #candidate1 = map_from_list(candidates)
            weigths = trainedGen[training_counter]

        control_keys = network.predict(X_state, weigths[0], weigths[1])
        X_list = X_list+control_keys


        #print(control_keys)

        # Snake controls
        simple = control_keys.index(max(control_keys)) + 1
        direction=None
        if simple == 1:
            y_change = -block_diff
            x_change = 0
            direction = "UP"

        elif simple == 2:
            y_change = block_diff
            x_change = 0
            direction = "DOWN"

        elif simple == 3:
            x_change = -block_diff
            y_change = 0
            direction = "LEFT"

        elif simple == 4:
            x_change = block_diff
            y_change = 0
            direction = "RIGHT"
        '''
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

                '''

                    #######################################################################################################
                    ######################################################################################################

        lead_x += x_change
        lead_y += y_change

        pygame.display.set_caption(direction+" :: " + str(fitness_factor)+"  goals:: "+str(TARGET_FITNESS))
        if fitness_factor >150:
            inputs = map_chromo(network.get_weights()[0], network.get_weights()[1], X_list)
            chromosomes.append(inputs)
            fitness_List.append(score*25 + fitness_factor)
            print("fitness factor appeded:::",score*25 + fitness_factor)
            gameExit = True



        # print("apple::", (apple_pos), "   snake::", [lead_x, lead_y])
        # Checking boundary crash
        if lead_x <= head_size or lead_x >= display_width - head_size or lead_y <= head_size or lead_y >= display_height - head_size:
            # print("boundary")
            inputs = map_chromo(network.get_weights()[0], network.get_weights()[1], X_list)
            chromosomes.append(inputs)
            fitness_List.append(score*25 + fitness_factor)
            print("fitness factor appeded:::",score * 25 + fitness_factor)
            gameExit = True

        # Creating snake head
        snake_Head = []
        snake_Head.append(lead_x)
        snake_Head.append(lead_y)

        # checking conflict between snake and its head

        if x_change != 0 or y_change != 0:
            for every_Seg in snake_List[:-1]:
                if every_Seg == snake_Head:
                    # print("conflict", every_Seg, " ", snake_Head)
                    inputs = map_chromo( network.get_weights()[0], network.get_weights()[1],X_list)
                    chromosomes.append(inputs)
                    fitness_List.append(score*25 + fitness_factor)
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
            # print("apple eaten")
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
            #snake_length += 1
            TARGET_FITNESS +=1
            FPS += 1

        clock.tick(FPS)


def game():

    global chromosomes
    global fitness_List
    global TARGET_FITNESS
    global TRAIN
    global training_counter
    global score
    global trainedGen
    global TARGET_FITNESS
    global POP_SIZE


    counter = 0

    fitness_List =[]
    chromosomes = []
    #print("Target::",TARGET_FITNESS)
    while TARGET_FITNESS<=25:

        game_trials()

        #print("TRIALS:::",counter ," generations::",counter//5)
        counter +=1
        training_counter +=1
        training_counter %= 5


        if counter % POP_SIZE==0:
            local_Population = bp.Population(POP_SIZE)
            local_Population.set_population(POP_SIZE,chromosomes,fitness_List)

            local_Population = bp.GeneticAlgo.evolve(local_Population)
            #local_Population.display_population(counter / 5)

            trainedChromo = local_Population.get_chromosomes()
            print("Trained Gen:::",counter//POP_SIZE)

            temp =0
            trainedGen = []
            file = open("Training_data.txt","w")
            file.write("Train generation ::"+str(counter//10)+"\n")

            for i in trainedChromo:

                trainedGen.append(i.get_genes())

                candidate = map_from_list(trainedGen[temp])
                trainedGen[temp] = candidate
                print(temp,"th gene fitness = ", i.get_fitness())
                file.write(str(trainedGen[temp])+" with score::"+str(score))


                temp+=1

            file.write("\n\n")
            file.close()
            TRAIN = True
            fitness_List = []
            chromosomes = []
    final_weights = trainedGen[0]
    network.set_weights(final_weights[0],final_weights[1])
    file = open("Training_data.txt", "w")
    file.write("\n\ntraining data:::\n")
    file.write(str(final_weights))
    file.close()
    np.save("snake_intell.npy",final_weights)

    print("COMPLETE")



game()






