import numpy as np


class MyNeuralNetwork:
    
    def __init__ (self):
        
        
        ### reproduction parameters ###
        #_____________________________#
                                    
        # create new link during simulation
        self.probOfNewConnection = 0.2

        # delete a connection during simulation
        self.probOfDelConnection = 0.2

        # create new neuron with one weight
        self.probOfNewNeuron = 0.05

        # delete a hidden neuron
        self.probOfDelNeuron = 0.01
        
        # standard deviation of values added to weights when creating offspring
        self.reproductionStdDev = 0.5

        # value std dev is multiplied by on ever iteration
        self.stdDevMult = 0.7
        
        #_____________________________#

        ###    network parameters   ###
        #_____________________________#
                                    
        # non zero weight at start - linking input and output
        self.probOfStartConnection = 0.5
        
        # number of tries for creating new neuron at start
        self.startingMutationMagnitude = 10
        
        # standard deviation of normal distr for weights
        self.startingStdDev = 1
        
        # structure of network
        self.nrOfInputs = 5
        self.nrOfHiddenLayers = 3
        self.nrOfOutputs = 4
        
        # number of layers in network, input layer not included
        self.networkSize = self.nrOfHiddenLayers + 1

        # array of sizes of layers (number of neurons for given layer)
        self.layerSizes = np.zeros(self.nrOfHiddenLayers + 2, dtype = int)

        # array of numbers of weights in each neuron for given layer
        self.layerWeightsSizes = np.zeros(self.nrOfHiddenLayers + 2, dtype = int)

        #_____________________________#
        
        # core structure of the network
        self.neuralNetwork = []
        
        # network score
        self.fitness = 0
        
        #_____________________________#

        
        # make list of layer sizes
        self.layerSizes[0] = self.nrOfInputs
        self.layerSizes[self.layerSizes.size - 1] = self.nrOfOutputs
        
        # make a list of number of weights in neurons for every layer
        for i in range(1, self.layerWeightsSizes.size):
            self.layerWeightsSizes[i] += 1
            for j in range(0, i):
                self.layerWeightsSizes[i] += self.layerSizes[j]
                
        # make whole network structure for weights
        for i in range(1, self.layerSizes.size):
            self.neuralNetwork.append(np.zeros((self.layerSizes[i], self.layerWeightsSizes[i])).T)
            
        # check for some new neuron mutations
        for i in range(0, self.startingMutationMagnitude):
            if np.random.random() < self.probOfNewNeuron:
                self.addNeuron(int(np.random.random() * self.nrOfHiddenLayers) + 1)
            
        # get the neurons random weights
        for layer in range(0, self.networkSize):
            for neuron in range(0, self.layerSizes[layer + 1]):
                for weight in range(0, self.layerWeightsSizes[layer + 1]):
                    if np.random.random() < self.probOfStartConnection:
                        self.neuralNetwork[layer][weight][neuron] = np.random.normal(0, self.startingStdDev)

    def activationFunction(self, x):
        return 1 / (1 + np.exp(-x))

    def activationFunction2(self, x):
        return 2 * x

    def printNetwork(self):
        for i in range(0, self.networkSize):
            print(self.neuralNetwork[i])
            print(" ")
            
    def compute(self, input):
        input.insert(0, 1)
        for i in range(0, self.networkSize - 1):
            output = self.activationFunction(np.dot(input, self.neuralNetwork[i]))
            print(input, " ", output)
            input.extend(output)
        output = self.activationFunction(np.dot(input, self.neuralNetwork[self.networkSize - 1]))
        return output
            
    def addNeuron(self, layerNr):
        newLayerSizes = self.layerSizes.copy()
        
        # update list of layer sizes
        newLayerSizes[layerNr] += 1
        
        # make a list of number of weights in neurons for every layer
        newLayerWeightsSizes = np.zeros(newLayerSizes.size, dtype = int)
        for i in range(1, newLayerWeightsSizes.size):
            newLayerWeightsSizes[i] += 1
            for j in range(0, i):
                newLayerWeightsSizes[i] += newLayerSizes[j]
        
        # make whole network structure for weights
        newNeuralNetwork = []
        for i in range(1, newLayerSizes.size):
            newNeuralNetwork.append(np.zeros((newLayerSizes[i], newLayerWeightsSizes[i])).T)

        # get the neurons random weights
        for layer in range(0, self.networkSize):
            for neuron in range(0, self.layerSizes[layer + 1]):
                newNeuron = 0
                for weight in range(0, self.layerWeightsSizes[layer + 1]):
                    if weight == self.layerWeightsSizes[layerNr+1]:
                        newNeuron = 1
                    newNeuralNetwork[layer][weight + newNeuron][neuron] = self.neuralNetwork[layer][weight][neuron]
                    
        # copy results
        self.layerSizes = newLayerSizes
        self.layerWeightsSizes = newLayerWeightsSizes
        self.neuralNetwork = newNeuralNetwork
        

    def networkCopy(self):
        newNetwork = []
        for i in range(1, self.networkSize + 1):
            newNetwork.append(np.zeros((self.layerSizes[i], self.layerWeightsSizes[i])).T)
        for layer in range(0, self.networkSize):
            for neuron in range(0, self.layerSizes[layer + 1]):
                for weight in range(0, self.layerWeightsSizes[layer + 1]):
                    newNetwork[layer][weight][neuron] = self.neuralNetwork[layer][weight][neuron]        
        return newNetwork

    def copy(self):
        newNeuralNetwork = MyNeuralNetwork()
        newNeuralNetwork.probOfNewConnection = self.probOfNewConnection
        newNeuralNetwork.probOfDelConnection = self.probOfDelConnection
        newNeuralNetwork.probOfNewNeuron = self.probOfNewNeuron
        newNeuralNetwork.probOfDelNeuron = self.probOfDelNeuron
        newNeuralNetwork.startingStdDev = self.startingStdDev
        newNeuralNetwork.stdDevMult = self.stdDevMult
        newNeuralNetwork.probOfStartConnection = self.probOfStartConnection
        newNeuralNetwork.nrOfInputs = self.nrOfInputs
        newNeuralNetwork.nrOfHiddenLayers = self.nrOfHiddenLayers
        newNeuralNetwork.nrOfOutputs = self.nrOfOutputs
        newNeuralNetwork.networkSize = self.networkSize
        newNeuralNetwork.layerSizes = self.layerSizes.copy()
        newNeuralNetwork.layerWeightsSizes = self.layerWeightsSizes.copy()
        newNeuralNetwork.neuralNetwork = self.networkCopy()
        return newNeuralNetwork
        
    def reproduce(self):
        # copy the parent
        child = self.copy()
        
        # check new neuron mutation
        if np.random.random() < self.probOfNewNeuron:
            child.addNeuron(int(np.random.random() * child.nrOfHiddenLayers) + 1)
        
        # change the weights, make or delete connections
        for layer in range(0, child.networkSize):
            for neuron in range(0, child.layerSizes[layer + 1]):
                for weight in range(0, child.layerWeightsSizes[layer + 1]):
                    if(child.neuralNetwork[layer][weight][neuron] != 0):
                        if np.random.random() < self.probOfDelConnection:
                            child.neuralNetwork[layer][weight][neuron] = 0
                        else:
                            child.neuralNetwork[layer][weight][neuron] += np.random.normal(0, self.reproductionStdDev)
                    else:
                        if np.random.random() < self.probOfNewConnection:
                            child.neuralNetwork[layer][weight][neuron] = np.random.normal(0, self.reproductionStdDev)
        
        # update new std dev for reproduction
        self.reproductionStdDev *= self.stdDevMult
        return child
    
    def test(self):
        np.random.seed(1)

        newNetwork = MyNeuralNetwork()

        # some print
        print(newNetwork.layerSizes)
        print(newNetwork.layerWeightsSizes)
        newNetwork.printNetwork()

        # reproducing
        children = []
        for i in range(0,10):
            children.append(newNetwork.reproduce())
        for i in range(0,10):
            children[i].printNetwork()
            
    def sortKey(self):
        return self.fitness
    
    
    



