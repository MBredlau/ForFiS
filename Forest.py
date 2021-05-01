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
    
    def init_random(self):
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                rand_state = random.randint(1, 3)
                """
                self.num_healthy = 0
                self.num_fire = 0
                self.num_burnt = 0
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
                self.forest[i, j] = rand_state
        
    def init_centre(self):
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                if (i == self.rows / 2 and j == self.columns / 2) or (i == (self.rows - 1) / 2 and j == (self.columns - 1) / 2):
                    self.forest[i, j] = 2
                else:
                    self.forest[i, j] = 1

    def init_hexa(self):
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                if (not (i % 2) and not (j % 2)) or ((j % 2) and (i % 2)):
                    self.forest[i, j] = 1
                if self.forest[i, j]:
                    if (i == self.rows / 2 or i == (self.rows - 1) / 2) and (
                            j == self.columns / 2 or j == self.columns / 2 - 1):  # or (i == (rows / 2) - 1 and j == columns / 2 or (i == (rows / 2) - 1 and j == (columns - 1) / 2)):
                        self.forest[i, j] = 2

    def __init__(self, initmode='hexa'):
        #self.forest = np.empty((rows, columns)), dtype=object)

        if initmode == 'random':
            self.init_arrays()
            self.init_random()
        elif initmode == 'centre':
            self.init_arrays()
            self.init_centre()
        elif initmode == 'hexa':
            self.columns *= 2
            self.init_arrays()
            self.init_hexa()
        else:  # default, if input is wrong
            self.init_arrays()
            self.init_random()

    def init_arrays(self):
        self.forest = np.zeros((self.rows, self.columns))
        self.forest_new = np.zeros((self.rows, self.columns))
        self.actions = np.zeros((self.rows, self.columns))

    def plot_rectangular(self):
        cmap = colors.ListedColormap(['white', 'green', 'red', 'black'])
        bounds = [-1, 0.9, 1.9, 2.9, 4]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        self.a.imshow(self.forest[:, :], interpolation='nearest', cmap=cmap, norm=norm)  # origin = 'higher'
        self.fig.canvas.draw()

    def plot_hex(self):
        forest = []
        for i in range(self.rows):
            forest.append([])
            for j in range(self.columns):
                if self.forest[i, j]:
                    forest[i].append(self.forest[i, j])
        hex_centers, _ = create_hex_grid(nx=len(forest[0]),
                                         ny=len(forest),
                                         do_plot=False)
        x_hex_coords = hex_centers[:, 0]
        y_hex_coords = hex_centers[:, 1]
        color = np.zeros([x_hex_coords.shape[0], 3])
        for i in range(len(forest)):
            for j in range(len(forest[0])):
                if 1.1 > forest[i][j] > 0.9:
                    color[i * len(forest[0]) + j, :] = [0.1, 0.7, 0.2]  # green
                    continue
                if 2.1 > forest[i][j] > 1.9:
                    color[i * len(forest[0]) + j, :] = [0.7, 0.1, 0.1]  # red
                    continue
                if 3.1 > forest[i][j] > 2.9:
                    color[i * len(forest[0]) + j, :] = [0, 0, 0]  # black
                    continue
                else:
                    color[i * len(forest[0]) + j, :] = [1, 1, 1]  # white

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

    def __init__(self, initmode='centre'):
        super().__init__(initmode)
        self.prob_transit = np.zeros((self.rows, self.columns))
        
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
        if column == 0 and row == 0:  # should never be reached
            return np.count_nonzero(self.forest[row: row + 2, column: column + 2] == value) + (self.forest[row, column + 2] == value)
        if column >= self.columns - 2:
            return np.count_nonzero(self.forest[row - 1: row + 2, column - 1] == value) + (self.forest[row, column - 2] == value)
        if column == 0:
            return np.count_nonzero(self.forest[row - 1: row + 2, column: column + 2] == value) + (self.forest[row, column + 2] == value) #+ (self.forest[row, column - 2] == value)
        if row == 0:
            return np.count_nonzero(self.forest[row: row + 2, column - 1: column + 2] == value) + (self.forest[row, column + 2] == value)
        return np.count_nonzero(self.forest[row - 1: row + 2, column - 1: column + 2] == value) + (self.forest[row, column + 2] == value) + (self.forest[row, column - 2] == value)

    def get_number_neighbors_on_fire(self, row, column):
        return self.get_number_neighbors_with_value(row, column, 2)

    def get_number_on_fire_rectangular(self, row, column):
        if column == 0 and row == 0:
            # print(self.forest[row : row + 2, column : column + 2])
            # print(np.count_nonzero(self.forest[row : row + 2, column : column + 2] == 2))
            return np.count_nonzero(self.forest[row: row + 2, column: column + 2] == 2)
        if column == 0:
            # print(self.forest[row - 1: row + 2, column : column + 2])
            # print(np.count_nonzero(self.forest[row - 1: row + 2, column : column + 2] == 2))
            return np.count_nonzero(self.forest[row - 1: row + 2, column: column + 2] == 2)
        if row == 0:
            # print(self.forest[row : row + 2, column - 1 : column + 2])
            # print(np.count_nonzero(self.forest[row : row + 2, column - 1 : column + 2] == 2))
            return np.count_nonzero(self.forest[row: row + 2, column - 1: column + 2] == 2)
            # print(self.forest[row - 1 : row + 2, column - 1 : column + 2])
            # print(np.count_nonzero(self.forest[row - 1 : row + 2, column - 1 : column + 2] == 2))
        return np.count_nonzero(self.forest[row - 1: row + 2, column - 1: column + 2] == 2)

class AgentModel():
    
    def __init__(self, initmode):
        super().__init__(initmode)

    def get_camera_data(self, row, column):
        camera = np.zeros((3, 3))
        for i in range(3):
            for j in range(3):
                camera[i, j] = self.forest[row + i - 1, column + j - 1]
        print(camera)

    def act(self):
        self.get_camera_data(3, 4)
        pass
