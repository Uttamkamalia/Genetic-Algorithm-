import random




CHROMO_LENGTH = 104

POPULATION_SIZE = 10
NO_OF_ELITES = 2
TOURNAMENT_SELECTIONS = 5
MUTATE_RATIO = 0.60


class Chromosome:

    def __init__(self,chromo,fitness):
        global CHROMO_LENGTH
        self.genes = chromo
        self.fitness = fitness
        self.chromo_length = len(self.genes)






    def get_genes(self):
        return self.genes

    def get_fitness(self):
        return self.fitness

    def __str__(self):
        return self.genes.__str__()



class Population:

    def __init__(self,size):
        self.chromosomes = []
        self.size = size



    def set_population(self,size,inputs,fitness):
        for chromo in range(0,POPULATION_SIZE):
           # print("INSERTION ",chromo," :: fitness: ",fitness[chromo],"  gene::",inputs[chromo])
            self.chromosomes.append(Chromosome(inputs[chromo],fitness[chromo]))


    def get_chromosomes(self,fit = False):

        self.chromosomes.sort(key= lambda x:x.get_fitness(),reverse=True)
        if fit==False:
            return self.chromosomes
        else :
            return self.chromosomes[0]



    def display_population(self,gener):
        print("----------------------------------------------------")
        print("generation::: ",gener)
        print("Fittest Chromosome with score::", self.get_chromosomes(fit=True).get_fitness(), " :::>> ", self.get_chromosomes(fit=True)," with size:: ")
        print("----------------------------------------------------")

        for i in self.get_chromosomes():
            print("Chromosome ::: ", i, " with fitness:: ", i.get_fitness())
        print()


class GeneticAlgo:

    @staticmethod
    def evolve(pop):
        return GeneticAlgo.mutate_pop(GeneticAlgo.crossover_pop(pop))

    @staticmethod
    def crossover_pop(pop):

        cross_pop = Population(0)

        for candid in range(NO_OF_ELITES):
            cross_pop.get_chromosomes().append(pop.get_chromosomes()[candid])

        for candid in range(NO_OF_ELITES,POPULATION_SIZE):
            listo = pop.get_chromosomes()
            chromos1 = listo[0]
            chromos2 = listo[1]
           # chromos1 = GeneticAlgo.tournament(pop).get_chromosomes(fit=True)
           # chromos2 = GeneticAlgo.tournament(pop).get_chromosomes(fit=True)
            chromos3 = GeneticAlgo.cross_chromosome(chromos1,chromos2)
            cross_pop.get_chromosomes().append(chromos3)
        #cross_pop.display_population("CROSS POPULATION:::")
        return cross_pop



    @staticmethod
    def mutate_pop(pop):

        for candid in range(NO_OF_ELITES,POPULATION_SIZE):
            GeneticAlgo.mutate_chromosome(pop.get_chromosomes()[candid])
        #pop.display_population("MUTATE POPULATION:::")
        return pop



    @staticmethod
    def cross_chromosome(chromo1,chromo2):
        global CHROMO_LENGTH
        baby_chromo = Chromosome([],0)

        for candid in range(CHROMO_LENGTH):
            if random.random() <=0.5:
                baby_chromo.get_genes().append(chromo1.get_genes()[candid])
            else:
                baby_chromo.get_genes().append(chromo2.get_genes()[candid])
           # print(" inside cross chromo  :::chromo at:",candid," :::",baby_chromo.get_genes()[candid])

        return baby_chromo

    @staticmethod
    def mutate_chromosome(chromo):
        global CHROMO_LENGTH
        for candid in range(CHROMO_LENGTH):
            if random.random() <=MUTATE_RATIO:
                if random.random() <= 0.5:
                    chromo.get_genes()[candid] = random.randrange(0,5)
                else:
                    chromo.get_genes()[candid] = random.randrange(-5,0)


    @staticmethod
    def tournament(pop):
        select = Population(0)
        #select = pop
        for candid in range(TOURNAMENT_SELECTIONS):
            #select.get_chromosomes().append(pop.get_chromosomes()[random.randrange(0,POPULATION_SIZE)])
            select.get_chromosomes().append(pop.get_chromosomes()[candid])
        select.get_chromosomes().sort(key = lambda x: x.get_fitness(),reverse = True )

        return select


'''
population = Population(POPULATION_SIZE)

population.display_population(0)

generation =1

while population.get_chromosomes(fit=True).get_fitness() < len(TARGET_CHROM):

    population = GeneticAlgo.evolve(population)
    population.display_population(generation)
    generation+=1

'''