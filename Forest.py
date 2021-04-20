#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 19:03:58 2021

@author: marvin
"""
import numpy as np
from matplotlib import colors
import random
from hexalattice.hexalattice import *
import matplotlib
matplotlib.use("TkAgg")


# Forest gets initialized with a specified fire distribution
class Forest:
    
    def init_random(self, rows, columns):
        for i in range(0, rows):
            for j in range(0, columns):
                rand_state = random.randint(1, 3)
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
        
    def init_centre(self, rows, columns):
        for i in range(0, rows):
            for j in range(0, columns):
                if (i == rows / 2 and j == columns / 2) or (i == (rows - 1) / 2 and j == (columns - 1) / 2):
                    self.forest[i, j] = 2
                else:
                    self.forest[i, j] = 1

    def init_hexa(self, rows, columns):
        for i in range(0, rows):
            for j in range(0, columns):
                if (i % 2) and not (j % 2):
                    if (i == (rows / 2) - 1 and j == columns / 2 or (i == (rows / 2) - 1 and j == (columns - 1) / 2)):# or (i == (rows / 2) - 1 and j == columns / 2 or (i == (rows / 2) - 1 and j == (columns - 1) / 2)):
                        self.forest[i, j] = 2
                    else:
                        self.forest[i, j] = 1
                if (j % 2) and not (i % 2):
                        self.forest[i, j] = 1

    def __init__(self, rows, columns, initmode='hexa'):
        #self.forest = np.empty((rows, columns)), dtype=object)
        self.forest = np.zeros((rows, columns))
        self.forest_new = np.zeros((rows, columns))
        self.actions = np.zeros((rows, columns))
        #self.num_healthy = 0
        #self.num_fire = 0
        #self.num_burnt = 0
        if initmode == 'random':
            self.init_random(rows, columns)
        elif initmode == 'centre':
            self.init_centre(rows, columns)
        elif initmode == 'hexa':
            self.init_hexa(rows, columns)
        else: # default
            self.init_random(rows, columns)

    def plot_rectangular(self):
        cmap = colors.ListedColormap(['white', 'green', 'red', 'black'])
        bounds = [-1, 0.9, 1.9, 2.9, 4]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        self.a.imshow(self.forest[:, :], interpolation='nearest', cmap=cmap, norm=norm)  # origin = 'higher'
        self.fig.canvas.draw()

    def plot_hex(self):
        # hex_centers, _ = create_hex_grid(nx=self.rows,
        #                                 ny=self.columns,
        #                                 do_plot=False)
        hex_centers, _ = create_hex_grid(nx=2*np.count_nonzero(self.forest[1,:])+1,
                                         ny=2*np.count_nonzero(self.forest[:,1])+1,
                                         do_plot=False)
        x_hex_coords = hex_centers[:, 0]
        y_hex_coords = hex_centers[:, 1]
        color = np.zeros([x_hex_coords.shape[0], 3])
        index = 0
        for i in range(int((self.rows % 2 + self.rows) / 2)):
            for j in range(self.columns):
                print(self.forest[i, j])
                print(index)
                if 1.1 > self.forest[2 * i, j] > 0.9:
                    # color[i * self.columns + j, :] = [0.1, 0.7, 0.2]  # green
                    color[index, :] = [0.1, 0.7, 0.2]  # green
                    index += 1
                    continue
                if 2.1 > self.forest[2 * i, j] > 1.9:
                    color[index, :] = [0.7, 0.1, 0.1]  # red
                    index += 1
                    continue
                if 3.1 > self.forest[2 * i, j] > 2.9:
                    color[index, :] = [0, 0, 0]  # black
                    index += 1
                    continue
                if 1.1 > self.forest[2 * i + 1, j] > 0.9:
                    # color[i * self.columns + j, :] = [0.1, 0.7, 0.2]  # green
                    color[index, :] = [0.1, 0.7, 0.2]  # green
                    index += 1
                    continue
                if 2.1 > self.forest[2 * i + 1, j] > 1.9:
                    color[index, :] = [0.7, 0.1, 0.1]  # red
                    index += 1
                    continue
                if 3.1 > self.forest[2 * i + 1, j] > 2.9:
                    color[index, :] = [0, 0, 0]  # black
                    index += 1
                    continue
                # else:
                #    color[i * self.columns + j, :] = [1, 1, 1]  # white
        self.a.cla()
        plot_single_lattice_custom_colors(x_hex_coords, y_hex_coords,
                                          face_color=color,
                                          edge_color=color,
                                          min_diam=0.9,
                                          plotting_gap=0.02,
                                          rotate_deg=0,
                                          h_ax=self.a)
        # self.a.scatter(3, 4, color='b')

        self.fig.canvas.draw()

    def plot(self):
        hex_centers, _ = create_hex_grid(nx=self.rows,
                                         ny=self.columns,
                                         do_plot=False)
        x_hex_coords = hex_centers[:, 0]
        y_hex_coords = hex_centers[:, 1]
        color = np.zeros([x_hex_coords.shape[0], 3])
        for i in range(self.rows):
            for j in range(self.columns):
                if 1.1 > self.forest[i, j] > 0.9:
                    color[i * self.columns + j, :] = [0.1, 0.7, 0.2]  # green
                    continue
                if 2.1 > self.forest[i, j] > 1.9:
                    color[i * self.columns + j, :] = [0.7, 0.1, 0.1]  # red
                    continue
                if 3.1 > self.forest[i, j] > 2.9:
                    color[i * self.columns + j, :] = [0, 0, 0]  # black
                    continue
                else:
                    color[i * self.columns + j, :] = [1, 1, 1]  # white
        self.a.cla()
        plot_single_lattice_custom_colors(x_hex_coords, y_hex_coords,
                                          face_color=color,
                                          edge_color=color,
                                          min_diam=0.9,
                                          plotting_gap=0.02,
                                          rotate_deg=0,
                                          h_ax=self.a)
        # self.a.scatter(3, 4, color='b')

        self.fig.canvas.draw()


# Fire model calculates the new fire distribution on the forest for each timestep
class FireModel(Forest):
            
    def __init__(self, rows, columns, initmode='centre'):
        super().__init__(rows, columns, initmode)
        self.prob_transit = np.zeros((rows, columns))
        
    def transition(self):
        self.forest_new[:] = self.forest[:]
        for row in range(0, self.rows):
            for column in range(0, self.columns):
                if self.forest[row, column] == 1:  # healthy
                    fire_neighbors = self.get_number_neighbors_on_fire(row, column)
                    self.prob_transit[row, column] += 1 - self.likelihood ** fire_neighbors
                if self.forest[row, column] == 2:  # on fire
                    self.prob_transit[row, column] += self.beta - self.actions[row, column] * self.delta_beta
                prob = random.randint(0, 100)
                if (self.prob_transit[row, column] * 100) > prob:
                    self.forest_new[row, column] += 1
                    self.prob_transit[row, column] = 0
        self.forest[:] = self.forest_new[:]

    def get_number_neighbors_with_value(self, row, column, value):
        if column == 0 and row == 0:
            return np.count_nonzero(self.forest[row: row + 2, column: column + 2] == value) + (self.forest[row + 2, column] == value)
        if row >= self.rows - 2:
            return np.count_nonzero(self.forest[row - 1: row + 2, column - 1: column + 2] == value) + (self.forest[row - 2, column] == value)
        if column == 0:
            return np.count_nonzero(self.forest[row - 1: row + 2, column: column + 2] == value) + (self.forest[row + 2, column] == value) + (self.forest[row - 2, column] == value)
        if row == 0:
            return np.count_nonzero(self.forest[row: row + 2, column - 1: column + 2] == value) + (self.forest[row + 2, column] == value)
        return np.count_nonzero(self.forest[row - 1: row + 2, column - 1: column + 2] == value) + (self.forest[row + 2, column] == value) + (self.forest[row - 2, column] == value)

    def get_number_neighbors_on_fire(self, row, column):
        return self.get_number_neighbors_with_value(row, column, 2)
        '''
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
        '''


class AgentModel():
    
    def __init__(self, rows, columns, initmode):
        super().__init__(rows, columns, initmode)
        
    def act(self):
        pass
