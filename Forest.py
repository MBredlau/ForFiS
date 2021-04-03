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

import matplotlib
import matplotlib.animation as animation
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import tkinter as tk

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
                self.forest[i,j] = rand_state
        
    def init_centrum(self, rows, columns):
        for i in range(0,rows):
            for j in range(0,columns):
                if (i == rows / 2 and j == columns / 2) or (i == (rows - 1) / 2 and j == (columns - 1) / 2):
                    self.forest[i, j] = 2
                else: 
                    self.forest[i, j] = 1
                
    def __init__(self, rows, columns, initmode):
        #self.forest = np.empty((rows, columns)), dtype=object)
        self.forest = np.zeros((rows,columns))
        self.forest_new = np.zeros((rows,columns))
        self.actions = np.zeros((rows,columns))
        
        #a = fig.add_subplot(111)
        #self.fenster = tk.Tk()
        #self.fenster.title("Forest Fire Simulation")
        
        #self.start_button = tk.Button(self.fenster, text="Start", command=self.start_simulation)
        #self.start_button.pack()
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
        #self.a.clear()
        cmap = colors.ListedColormap(['green', 'red', 'black'])
        bounds=[0.9,1.9,2.9,4]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        self.a.imshow(self.forest[:,:], interpolation='nearest', cmap=cmap, norm=norm) # origin = 'higher'
        self.fig.canvas.draw()
         
# Fire model calculates the new fire distribution on the forest for each timestep
class Fire_model(Forest):
            
    def __init__(self, rows, columns, initmode):
        super().__init__(rows, columns, initmode)
        self.prob_transit = np.zeros((rows, columns))
        
    def transition(self):
        self.forest_new[:] = self.forest[:]
        for row in range(0,self.rows):
            #print(self.forest)
            for column in range(0,self.columns):
                if self.forest[row, column] == 1: # healthy
                    fire_neighbors = self.get_number_neighbors_on_fire(row, column)
                    self.prob_transit[row, column] += 1 - self.likelihood ** fire_neighbors
                    #self.transit_healthy(row, column)
                if self.forest[row, column] == 2: # on fire
                    self.prob_transit[row, column] += self.beta - self.actions[row, column] * self.delta_beta
                    #self.transit_fire(row, column)
                prob = random.randint(0,100)
                if (self.prob_transit[row, column] * 100) > prob:
                    self.forest_new[row, column] += 1
                    self.prob_transit[row, column] = 0
        self.forest[:] = self.forest_new[:]
        
    def get_number_neighbors_on_fire(self, row, column):
        if column == 0 and row == 0:  
            #print(self.forest[row : row + 2, column : column + 2])
            #print(np.count_nonzero(self.forest[row : row + 2, column : column + 2] == 2))
            return np.count_nonzero(self.forest[row : row + 2, column : column + 2] == 2)
        if column == 0:
            #print(self.forest[row - 1: row + 2, column : column + 2])
            #print(np.count_nonzero(self.forest[row - 1: row + 2, column : column + 2] == 2))
            return np.count_nonzero(self.forest[row - 1: row + 2, column : column + 2] == 2)
        if row == 0:
            #print(self.forest[row : row + 2, column - 1 : column + 2])
            #print(np.count_nonzero(self.forest[row : row + 2, column - 1 : column + 2] == 2))
            return np.count_nonzero(self.forest[row : row + 2, column - 1 : column + 2] == 2)
        #print(self.forest[row - 1 : row + 2, column - 1 : column + 2])
        #print(np.count_nonzero(self.forest[row - 1 : row + 2, column - 1 : column + 2] == 2))
        return np.count_nonzero(self.forest[row - 1 : row + 2, column - 1 : column + 2] == 2)
    

       
    
class Agent_model():
    
    def __init__(self, rows, columns, initmode):
        super().__init__(rows, columns, initmode)
        
    def act(self):
        pass
        

