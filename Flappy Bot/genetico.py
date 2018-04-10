import random

TARGET_CHROM = [1,0,1,1,0,1,1,0,0,1]

POPULATION_SIZE = 10
NO_OF_ELITES = 2
TOURNAMENT_SELECTIONS = 5
MUTATE_RATIO = 4.5


class Chromosome:

    def __init__(self):
        self.genes = []
        self.fitness = 0

        for gene in range(0, len(TARGET_CHROM)):
            if random.random() >= 0.5:
                self.genes.append(1)
            else:
                self.genes.append(0)

    def get_genes(self):
        return self.genes

    def get_fitness(self):

        self.fitness = 0
        for gene in range(0,len(self.genes)):
            if self.genes[gene] == TARGET_CHROM[gene]:
                self.fitness +=1
        return self.fitness

    def __str__(self):
        return self.genes.__str__()



class Population:

    def __init__(self,size):
        self.chromosomes = []

        for chromo in range(0,size):
            self.chromosomes.append(Chromosome())

    def get_chromosomes(self,fit = False):

        self.chromosomes.sort(key=lambda x: x.get_fitness(),reverse=True)
        if fit==False:
            return self.chromosomes
        else :
            return self.chromosomes[0]

    def display_population(self,gener):
        print("----------------------------------------------------")
        print("Target Chromosome::: ", TARGET_CHROM)
        print("Fittest Chromosome of Generation-", gener, " ::: ", self.get_chromosomes(fit=True)," with fitness:: ", self.get_chromosomes(fit=True).get_fitness())
        print("----------------------------------------------------")

        for i in self.get_chromosomes():
            print("Chromosome ::: ", i, " with fitness:: ", i.get_fitness())


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
            chromos1 = GeneticAlgo.tournament(pop).get_chromosomes(fit=True)
            chromos2 = GeneticAlgo.tournament(pop).get_chromosomes(fit=True)
            cross_pop.get_chromosomes().append(GeneticAlgo.cross_chromosome(chromos1,chromos2))
        return cross_pop



    @staticmethod
    def mutate_pop(pop):

        for candid in range(NO_OF_ELITES,POPULATION_SIZE):
            GeneticAlgo.mutate_chromosome(pop.get_chromosomes()[candid])
        return pop



    @staticmethod
    def cross_chromosome(chromo1,chromo2):
        baby_chromo = Chromosome()
        for candid in range(len(TARGET_CHROM)):
            if random.random() <=0.5:
                baby_chromo.get_genes()[candid] = chromo1.get_genes()[candid]
            else:
                baby_chromo.get_genes()[candid] = chromo2.get_genes()[candid]

        return baby_chromo

    @staticmethod
    def mutate_chromosome(chromo):

        for candid in range(len(TARGET_CHROM)):
            if random.random() <=MUTATE_RATIO:
                if random.random() <= 0.5:
                    chromo.get_genes()[candid] = 1
                else:
                    chromo.get_genes()[candid] = 0


    @staticmethod
    def tournament(pop):
        select = Population(0)
        for candid in range(TOURNAMENT_SELECTIONS):
            select.get_chromosomes().append(pop.get_chromosomes()[random.randrange(0,POPULATION_SIZE)])
        select.get_chromosomes().sort(key = lambda x: x.get_fitness(),reverse = True )

        return select



population = Population(POPULATION_SIZE)

population.display_population(0)

generation =1

while population.get_chromosomes(fit=True).get_fitness() < len(TARGET_CHROM):

    population = GeneticAlgo.evolve(population)
    population.display_population(generation)
    generation+=1

