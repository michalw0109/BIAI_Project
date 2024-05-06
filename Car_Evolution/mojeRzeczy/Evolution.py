from mojeRzeczy import MyNeuralNetwork as mnn
import numpy as np

class Evolution:
    
    def __init__(self):
        
        self.populationSize = 50
        
        # what fraction of population survives, eg. 0.4 survives, makes another 0.4 with reproduction, 0.2 is new 
        self.survivalRate = 0.4

        self.generationsList = [0]

        self.bestFitnessList = [0.0]

        # clear data each time program is run
        with open("graphData.txt", "w"):
            pass
        
        # open graph data file to append it with each generation's fitness
        self.graphDataFileAppend = open("graphData.txt", "a")
        
        self.population = []
        
    def createPopulation(self):
        for _ in range(0, self.populationSize):
            self.population.append(mnn.MyNeuralNetwork())
            
    def printPopulation(self):
        for i in range(0, self.populationSize):
            print(" ")
            print("network nr. ", i + 1)
            print(" ")
            self.population[i].printNetwork()
            
    def nextGeneration(self):
        # sort the population
        self.population.sort(key=mnn.MyNeuralNetwork.sortKey, reverse=True)

        best = self.population[0].fitness
        print("BESTFITNESS = "+str(best))
        self.graphDataFileAppend.write(str(best)+"\n")
        self.bestFitnessList.extend([best])
        self.generationsList.extend([len(self.generationsList)])

        survivorsSize = int(self.populationSize * self.survivalRate)
        
        # reproduce the best
        for i in range (0, survivorsSize):
            self.population[i + survivorsSize] = self.population[i].reproduce()
            
        # fill in the rest with new
        for i in range (0, self.populationSize - 2 * survivorsSize):
            self.population[i + 2 * survivorsSize] = mnn.MyNeuralNetwork()
            
        # reset the fitness
        for i in range (0, self.populationSize):
            self.population[i].fitness = 0
            
    def test(self):
        newPopulation = Evolution()
        newPopulation.createPopulation()
        newPopulation.nextGeneration()
        newPopulation.printPopulation()
        
        
        
        
        

        