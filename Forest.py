#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 19:03:58 2021

@author: marvin
"""
import numpy as np
from matplotlib import colors
import random
import math
from hexalattice.hexalattice import *
import matplotlib
matplotlib.use("TkAgg")


# static methods
def euclidean_distance(row1, col1, row2, col2):
    return math.sqrt((row1 - row2) ** 2 + (col1 - col2) ** 2)


# Forest gets initialized with a specified fire distribution
class Forest:

    def __init__(self, initmode='centre'):
        # self.forest = np.empty((rows, columns)), dtype=object)
        self.forest = np.zeros((self.rows, self.columns))
        self.forest_new = np.zeros((self.rows, self.columns))
        if self.number_agents:
            self.agents = []
            self.actions = np.zeros((self.rows, self.columns))
            for i in range(self.number_agents):
                self.agents.append((1 + i, 1))
                '''
                # set agents on random positions
                agent_set = False
                while not agent_set:
                    row = random.randint(0, self.rows - 1)
                    col = random.randint(0, self.columns - 1)
                    if not self.agents[row][col]:
                        self.agents[row][col] = 1
                        agent_set = True
                '''
        if initmode == 'random':
            self.init_random()
        elif initmode == 'centre':
            self.init_centre()
        else:  # default, if input is wrong
            print("init mode unknown")
            self.init_random()

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
                self.forest[i, j] = 1
        if self.rows % 2:  # rows odd
            self.source_row = int((self.rows - 1) / 2)
            if self.columns % 2:  # columns odd
                self.source_column = int(self.columns / 2)
            else:
                self.source_column = int(self.columns / 2) - 1
        else:
            self.source_row = int(self.rows / 2)
            if self.columns % 2:
                self.source_column = int((self.columns - 1) / 2)
            else:
                self.source_column = int(self.columns / 2)
        self.forest[self.source_row, self.source_column] = 2

    def plot_rectangular(self):
        cmap = colors.ListedColormap(['white', 'green', 'red', 'black'])
        bounds = [-1, 0.9, 1.9, 2.9, 4]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        self.a.imshow(self.forest[:, :], interpolation='nearest', cmap=cmap, norm=norm)  # origin = 'higher'
        self.fig.canvas.draw()

    def plot(self):
        forest = []
        for i in range(self.rows):
            forest.append([])
            for j in range(self.columns):
                if self.forest[i, j]:
                    forest[i].append(self.forest[i, j])
        hex_centers, _ = create_hex_grid(nx=len(forest[0]),
                                         ny=len(forest),
                                         do_plot=False)
        x_hex_cords = hex_centers[:, 0]
        y_hex_cords = hex_centers[:, 1]
        color = np.zeros([x_hex_cords.shape[0], 3])
        for i in range(len(forest)):
            for j in range(len(forest[0])):
                if (i, j) in self.agents:  # if agent is here (regardless of action)
                    color[i * self.columns + j, :] = [0, 0, 1]  # blue
                    continue
                if 1.1 > forest[i][j] > 0.9:
                    color[i * len(forest[0]) + j, :] = [0.1, 0.7, 0.1]  # green
                    continue
                if 2.1 > forest[i][j] > 1.9:
                    color[i * len(forest[0]) + j, :] = [1, 0, 0]  # red
                    continue
                if 3.1 > forest[i][j] > 2.9:
                    color[i * len(forest[0]) + j, :] = [0, 0, 0]  # black
                    continue
                if 4.1 > forest[i][j] > 3.9:
                    color[i * len(forest[0]) + j, :] = [1, 1, 0]  # yellow
                    continue
                else:
                    color[i * len(forest[0]) + j, :] = [1, 1, 1]  # white

        self.a.cla()
        plot_single_lattice_custom_colors(x_hex_cords, y_hex_cords,
                                          face_color=color,
                                          edge_color=color,
                                          min_diam=0.9,
                                          plotting_gap=0.02,
                                          rotate_deg=0,
                                          h_ax=self.a)
        self.fig.canvas.draw()


# Fire model calculates the new fire distribution on the forest for each time step
class FireModel(Forest):

    def __init__(self, initmode='centre'):
        super().__init__(initmode)
        self.prob_transit = np.zeros((self.rows, self.columns))
        
    def transition(self):
        self.forest_new[:] = self.forest[:]
        for row in range(0, self.rows):
            for column in range(0, self.columns):
                if self.forest[row, column] == 1:  # healthy
                    positions = self.get_neighbor_indices(row, column)
                    fire_neighbors = self.count_trees_on_fire(positions)
                    if fire_neighbors:
                        self.prob_transit[row, column] += 1 - self.likelihood ** fire_neighbors
                    else:
                        self.prob_transit[row, column] = 0
                if self.forest[row, column] == 2:  # on fire
                    self.prob_transit[row, column] += 1 - self.beta + self.actions[row, column] * self.delta_beta
                prob = random.randint(0, 100)
                if (self.prob_transit[row, column] * 100) > prob:
                    if self.actions[row, column]:
                        self.forest_new[row, column] = 4
                    else:
                        self.forest_new[row, column] += 1
                    self.prob_transit[row, column] = 0
        self.forest[:] = self.forest_new[:]

    def get_number_neighbors_with_value(self, row, column, value):
        if column == 0 and row == 0:
            return int(self.forest[row, column + 1] == value) + int(self.forest[
                row + 1, column] == value) + int(self.forest[row + 1, column + 1] == value)
        if row == 0 and column < self.columns - 1:
            return int(self.forest[row, column + 1] == value) + int(self.forest[row, column - 1] == value) + int(self.forest[
                row + 1, column] == value) + int(self.forest[row + 1, column + 1] == value)
        if column == 0 and row < self.rows - 1:
            return int(self.forest[row - 1, column] == value) + int(self.forest[row - 1, column + 1] == value) + int(self.forest[
                row, column + 1] == value) + int(self.forest[row + 1, column] == value) + int(self.forest[row + 1, column + 1] == value)
        if column == self.columns - 1 and row == self.rows - 1:
            return int(self.forest[row - 1, column] == value) + int(self.forest[row, column - 1] == value)
        if column == self.columns - 1:
            return int(self.forest[row - 1, column] == value) + int(self.forest[row, column - 1] == value) + int(self.forest[row + 1, column] == value)
        if row == self.rows - 1:
            return int(self.forest[row - 1, column] == value) + int(self.forest[row - 1, column + 1] == value) + int(self.forest[
                row, column + 1] == value) + int(self.forest[row, column - 1] == value)
        return int(self.forest[row - 1, column] == value) + int(self.forest[row - 1, column + 1] == value) + int(self.forest[
            row, column + 1] == value) + int(self.forest[row, column - 1] == value) + int(self.forest[row + 1, column] == value) + int(self.forest[
                row + 1, column + 1] == value)

    def count_trees_on_fire(self, positions):
        trees_on_fire = 0
        for index in range(len(positions)):
            (row, col) = positions[index]
            if self.forest[row, col] == 2:
                trees_on_fire += 1
        return trees_on_fire

    def get_number_neighbors_on_fire(self, row, column):
        return self.get_number_neighbors_with_value(row, column, 2)

    def get_neighbor_indices(self, row, column):
        position = []
        if column > 0:
            position.append((row, column - 1))
        if column < self.columns - 1:
            position.append((row, column + 1))

        if not row % 2:  # if row is even
            if row < self.rows - 1:
                position.append((row + 1, column))
                if column > 0:
                    position.append((row + 1, column - 1))
            if row > 0:
                position.append((row - 1, column))
                if column > 0:
                    position.append((row - 1, column - 1))

        if row % 2:  # if row is odd
            if row < self.rows - 1:
                position.append((row + 1, column))
                if column < self.columns - 1:
                    position.append((row + 1, column + 1))
            if row > 0:
                position.append((row - 1, column))
                if column < self.columns - 1:
                    position.append((row - 1, column + 1))

        return position

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


class AgentModel(Forest):
    
    def __init__(self, initmode):
        super().__init__(initmode)
        self.memory = np.zeros(self.number_agents)

    def get_possible_moves(self, row, column):
        return self.get_neighbor_indices(row, column)

    def move(self, row, column, agent_index):
        lowest = 1000
        next_row = row
        next_col = column
        position = self.get_possible_moves(row, column)
        for neighbor_row, neighbor_col in position:
            if self.mode == "Haksar":
                cost = self.calc_cost_haksar(neighbor_row, neighbor_col, agent_index)
            elif self.mode == "Heuristik":
                cost = self.calc_cost_function(neighbor_row, neighbor_col)
            else:
                print("Agent Mode unknown")
                pass
            if cost <= lowest:
                lowest = cost
                next_row = neighbor_row
                next_col = neighbor_col
        self.agents[agent_index] = (next_row, next_col)

    def calc_cost_function(self, row, column):
        if (row, column) in self.agents:
            return 1001
        if self.forest[row, column] == 2:
            return 0
        return euclidean_distance(row, column, self.source_row, self.source_column)

    def calc_cost_haksar(self, row, column, agent_index):
        if (row, column) in self.agents:  # avoid place of other agents
            return 1001
        if not self.memory[agent_index]:  # if no fire seen, go to fire source
            return euclidean_distance(row, column, self.source_row, self.source_column)
        (base_row, base_col) = self.agents[agent_index]
        position = np.array([base_row, base_col])
        rotation_vector = (self.source_row, self.source_column) - position
        norm = np.linalg.norm(rotation_vector, 2)
        if norm != 0:
            rotation_vector = rotation_vector / norm
        rotation_vector = np.array([- rotation_vector[1], rotation_vector[0]])
        if euclidean_distance(row - base_row, column - base_col, - rotation_vector[1], rotation_vector[0]) <= math.sqrt(2) and euclidean_distance(row - base_row, column - base_col, rotation_vector[0], rotation_vector[1]) <= math.sqrt(2):
            if self.forest[row, column] == 2:  # if sees fire to the "left", go there
                return 0
            if self.forest[row, column] == 3:  # if burnt go there, but less important than fire. And got away from source to reach fire front again
                return 0.1
        positions = self.get_neighbor_indices(row, column)
        fire_neighbors = self.count_trees_on_fire(positions)
        if not fire_neighbors:
            return euclidean_distance(row, column, self.source_row, self.source_column)
        return euclidean_distance(row - base_row, column - base_col, rotation_vector[0], rotation_vector[1])

    def apply_control_actions(self, row, col):
        if self.forest[row, col] == 2:
            self.actions[row, col] += 1

    def memorize(self, row, col, agent_index):
        if self.forest[row, col] == 2 or self.forest[row, col] == 3:
            self.memory[agent_index] = 1

    def act(self):
        agent_index = 0
        for (row, column) in self.agents:
            self.apply_control_actions(row, column)
            self.memorize(row, column, agent_index)
            self.move(row, column, agent_index)
            agent_index += 1


'''
## TODO ##
apply actions -> tree gets extinguished and can't ignite neighbor trees anymore. Currently it is extinguished after igniting the neighbors
restructure code and rely on clean code! (for master branch)
option to simulate without GUI. Live Terminal Output and log file
Wind und Fire spreading
optimize the way to distinguish between different modes: methods, that call the different methods based on the mode
'''