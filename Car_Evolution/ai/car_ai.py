# ------------------ IMPORTS ------------------


from render.car import Car, Action
import pygame
from mojeRzeczy.Evolution import Evolution
import numpy as np


# ------------------ CLASSES ------------------

class CarAI:

    TOTAL_GENERATIONS = 0
    TIME_LIMIT = 15

    #zmieniamy konstruktor by miec srodek okna
    def __init__(self, _myEvoEngine, start_position: list, screen_dim: list):
        CarAI.TOTAL_GENERATIONS += 1
        
        self.myEvoEngine = _myEvoEngine

        self.cars = []
        
        self.best_fitness = 0

        

        # We create a neural network for every given genome
        for _ in range(0, self.myEvoEngine.populationSize):
            self.cars.append(Car(start_position,screen_dim))

        self.remaining_cars = len(self.cars)
        

    def compute(self, track: pygame.Surface) -> None:
        """Compute the next move of every car and update their fitness

        Args:
            genomes (neat.DefaultGenome): The neat genomes
            track (pygame.Surface): The track on which the car is being drawn
            width (int): The width of the window
        """
        
        for i in range(0, self.myEvoEngine.populationSize):
            
            input = self.cars[i].get_data()
            # Activate the neural network and get the output from the car_data (input)
            output = self.myEvoEngine.population[i].compute(input)
            
            self.dataModelDiscrete(output, i)
            

      
                
            

        # Refresh cars sprites, number of cars which are still alive and update their fitness
        self.remaining_cars = sum(1 for car in self.cars if car.alive)

        # We draw the car if it is still alive
        # We also update the fitness of every car by giving them the reward they got for their last move
        for i, car in enumerate(self.cars):
            if car.alive:
                car.update_sprite(track)
                self.myEvoEngine.population[i].fitness += car.get_reward()
                if self.myEvoEngine.population[i].fitness > self.best_fitness:
                    self.best_fitness = self.myEvoEngine.population[i].fitness
    
    
    
    def dataModelContinuous(self, output, i):
        output -= output.min()
        if output.sum() != 0:
            output /= output.sum()
            

        self.cars[i].turn_left(output[0])
        self.cars[i].turn_right(output[1])
        self.cars[i].accelerate(output[2])
        self.cars[i].brake(output[3])
        
    def dataModelHalfContinuous(self, output, i):
        minLR = min(output[0], output[1])
        minAB = min(output[2], output[3])
        output[0] -= minLR
        output[1] -= minLR
        output[2] -= minAB
        output[3] -= minAB
        if(output[0] + output[1] != 0):
            output[0] /= output[0] + output[1]
            output[1] /= output[0] + output[1]
        if(output[2] + output[3] != 0):
            output[2] /= output[2] + output[3]
            output[3] /= output[2] + output[3]            

        self.cars[i].turn_left(output[0])
        self.cars[i].turn_right(output[1])
        self.cars[i].accelerate(output[2])
        self.cars[i].brake(output[3])

    def dataModelDiscrete(self, output, i):
        choice = self.maxIndex(output)
        # 0: Left
        if choice == Action.TURN_LEFT:
            self.cars[i].turn_left(1)

            # 1: Right
        elif choice == Action.TURN_RIGHT:
            self.cars[i].turn_right(1)

            # 2: Accelerate
        elif choice == Action.ACCELERATE:
            self.cars[i].accelerate(1)

            # 3: Brake
        elif choice == Action.BRAKE:
            self.cars[i].brake(1)
             
    def dataModelHalfDiscrete(self, output, i):
         
        choiceLR = self.twoMaxIndex(output[0], output[1])
        choiceAB = self.twoMaxIndex(output[2], output[3])
        
        # 0: Left
        if choiceLR == Action.TURN_LEFT:
            self.cars[i].turn_left(1)

            # 1: Right
        elif choiceLR == Action.TURN_RIGHT:
            self.cars[i].turn_right(1)

            # 2: Accelerate
        if choiceAB + 2 == Action.ACCELERATE:
            self.cars[i].accelerate(1)

            # 3: Brake
        elif choiceAB + 2 == Action.BRAKE:
            self.cars[i].brake(1)
    
    def maxIndex(self, arr):
        maxVal = arr[0]
        maxIndex = 0
        for i in range(1, arr.size):
            if arr[i] > maxVal:
                maxVal = arr[i]
                maxIndex = i
        return maxIndex
    
    def twoMaxIndex(self, a, b):
        if a > b:
            return 0
        else:
            return 1