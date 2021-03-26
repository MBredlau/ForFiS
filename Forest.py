#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 19:03:58 2021

@author: marvin
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import random

# Forest gets initialized with a specified fire distribution
class Forest():
    
    def init_random(self, rows, columns):
        for i in range(0,rows):
            for j in range(0,columns):
                rand_state = random.randint(1,3)
                """
                if rand_state == 1:
                    state = "Healthy"
                    self.num_healthy += 1
                if rand_state == 2:
                    state = 'On Fire'
                    self.num_fire += 1
                if rand_state == 3:
                    state = 'Burnt'
                    self.num_burnt += 1
                    """
                self.forest[i,j,0] = rand_state
        
    def init_centrum(self, rows, columns):
        for i in range(0,rows):
            for j in range(0,columns):
                if i == rows / 2 and j == columns / 2:
                    self.forest[i, j, 0] = 2
                else: 
                    self.forest[i, j, 0] = 1
                
    def __init__(self, rows, columns, initmode):
        #self.forest = np.empty((rows, columns)), dtype=object)
        self.forest = np.zeros((rows,columns,2))
        self.forest_new = np.zeros((rows,columns,2))
        #self.num_healthy = 0
        #self.num_fire = 0
        #self.num_burnt = 0
        if initmode == 'random':
            self.init_random(rows, columns)
        elif initmode == 'centrum':
            self.init_centrum(rows, columns)
        else: # default
            self.init_random(rows, columns)
            
    def plot(self):
        cmap = colors.ListedColormap(['green', 'red', 'black'])
        bounds=[0.9,1.9,2.9,4]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        plt.imshow(self.forest[:,:,0], interpolation='nearest', cmap=cmap, norm=norm) # origin = 'higher'
        plt.show()
         
# Fire model calculates the new fire distribution on the forest for each timestep
class Fire_model(Forest):
            
    def __init__(self, rows, columns, initmode):
        super().__init__(rows, columns, initmode)
        
    def transition(self):
        self.forest_new[:] = self.forest[:]
        for row in range(0,self.rows):
            #print(self.forest)
            for column in range(0,self.columns):
                if self.forest[row, column, 0] == 1: # healthy
                    self.transit_healthy(row, column)
                if self.forest[row, column, 0] == 2: # on fire
                    self.transit_fire(row, column)
        self.forest[:] = self.forest_new[:]
        
    def transit_healthy(self, row, column):
        #print(row, column)#, self.get_number_neighbors_on_fire(row, column))
        fire_neighbors = self.get_number_neighbors_on_fire(row, column)
        if fire_neighbors:
            prob_healthy = 1 - self.likelihood ** fire_neighbors
        else:
            prob_healthy = 1
        
        if (prob_healthy * 100) < random.randint(0,100):
            self.forest_new[row, column] = 2
        
    def transit_fire(self, row, column):
        prob_fire = self.beta - self.forest[row, column, 1] * self.delta_beta
        if prob_fire:
            self.forest_new[row, column, 0] = 2
        else:
            self.forest_new[row, column, 0] = 3
        
    def get_number_neighbors_on_fire(self, row, column):
        if column == 0 and row == 0:  
            #print(self.forest[row : row + 2, column : column + 2])
            #print(np.count_nonzero(self.forest[row : row + 2, column : column + 2] == 2))
            return np.count_nonzero(self.forest[row : row + 2, column : column + 2, 0] == 2)
        if column == 0:
            #print(self.forest[row - 1: row + 2, column : column + 2])
            #print(np.count_nonzero(self.forest[row - 1: row + 2, column : column + 2] == 2))
            return np.count_nonzero(self.forest[row - 1: row + 2, column : column + 2, 0] == 2)
        if row == 0:
            #print(self.forest[row : row + 2, column - 1 : column + 2])
            #print(np.count_nonzero(self.forest[row : row + 2, column - 1 : column + 2] == 2))
            return np.count_nonzero(self.forest[row : row + 2, column - 1 : column + 2, 0] == 2)
        #print(self.forest[row - 1 : row + 2, column - 1 : column + 2])
        #print(np.count_nonzero(self.forest[row - 1 : row + 2, column - 1 : column + 2] == 2))
        return np.count_nonzero(self.forest[row - 1 : row + 2, column - 1 : column + 2, 0] == 2)
    

       
    
class Agent_model():
    
    def __init__(self, rows, columns, initmode):
        super().__init__(rows, columns, initmode)
        
    def act(self):
        print('nichts')
        

