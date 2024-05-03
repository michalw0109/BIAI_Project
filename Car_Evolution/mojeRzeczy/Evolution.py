import MyNeuralNetwork as mnn

class Evolution:
    
    def __init__(self):
        
        self.populationSize = 50
        
        # what fraction of population survives, eg. 0.4 survives, makes another 0.4 with reproduction, 0.2 is new 
        self.survivalRate = 0.4
        
        self.population = []
        
    def createPopulation(self):
        for _ in range(0, self.populationSize):
            self.population.append(mnn.MyNeuralNetwork())
            
    def printPopulation(self):
        for i in range(0, self.populationSize):
            self.population[i].printNetwork()
            
    def nextGeneration(self):
        # sort the population
        self.population.sort(key=mnn.MyNeuralNetwork.sortKey, reverse=True)
        survivorsSize = self.populationSize * self.survivalRate
        
        # reproduce the best
        for i in range (0, survivorsSize):
            self.population[i + survivorsSize] = self.population[i].reproduce()
            
        # fill in the rest with new
        for i in range (0, self.populationSize - 2 * survivorsSize):
            self.population[i + 2 * survivorsSize] = mnn.MyNeuralNetwork()
            
    def test(self):
        newPopulation = Evolution()
        newPopulation.createPopulation()
        newPopulation.nextGeneration()
        newPopulation.printPopulation()
        
        
        
        
        

        