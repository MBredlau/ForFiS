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
                # adapt start positions of agents here
        else:
            self.agents = []
            self.actions = np.zeros((self.rows, self.columns))
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

    def plot(self, grid):
        if grid == "hexagonal":
            self.plot_hexagonal()
        elif grid == "rectangular":
            self.plot_rectangular()
        else:
            self.plot_hexagonal()
            print("Grid is set to unknown mode. Hexagonal grid chosen by default.")

    def plot_rectangular(self):
        cmap = colors.ListedColormap(['white', 'green', 'red', 'black'])
        bounds = [-1, 0.9, 1.9, 2.9, 4]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        self.a.imshow(self.forest[:, :], interpolation='nearest', cmap=cmap, norm=norm)  # origin = 'higher'
        self.fig.canvas.draw()

    def plot_hexagonal(self):
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
                if self.number_agents:
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
                        if np.linalg.norm(self.wind) == 0:
                            self.prob_transit[row, column] += 1 - self.alpha_0 ** fire_neighbors
                        else:
                            test_vector = np.array([1, 1])
                            product_alpha = 1
                            for neighbor in positions:
                                product_alpha *= (self.alpha_0 * np.linalg.norm(self.wind)/(1-(1-self.alpha_0/self.alpha_wind)*np.dot(self.wind, test_vector)))**fire_neighbors#self.vector)) ** fire_neighbors... vector kriegt neighbors
                            self.prob_transit[row, column] += 1 - product_alpha
                    else:
                        self.prob_transit[row, column] = 0
                if self.forest[row, column] == 2:  # on fire
                    self.prob_transit[row, column] += self.beta
                prob = random.randint(0, 100)
                if (self.prob_transit[row, column] * 100) > prob:
                    if not self.number_agents:
                        self.forest_new[row, column] += 1
                    else:
                        if self.actions[row, column]:
                            self.forest_new[row, column] = 4
                        else:
                            self.forest_new[row, column] += 1
                    self.prob_transit[row, column] = 0
        self.forest[:] = self.forest_new[:]
        if self.gedächtnislos == True:
            self.prob_transit[:] = 0

    def count_trees_on_fire(self, positions):
        trees_on_fire = 0
        for index in range(len(positions)):
            (row, col) = positions[index]
            if self.forest[row, col] == 2:
                trees_on_fire += 1
        return trees_on_fire

    def calc_stats(self):
        trees = self.columns * self.rows
        healthy_trees = np.count_nonzero(self.forest[:, :] == 1) / trees
        trees_onfire = np.count_nonzero(self.forest[:, :] == 2) / trees
        burnt_trees = np.count_nonzero(self.forest[:, :] == 3) / trees
        extinguished_trees = np.count_nonzero(self.forest[:, :] == 4) / trees
        return healthy_trees, trees_onfire, burnt_trees, extinguished_trees

    def calc_metric(self, time):
        healthy, onfire, burnt, extinguished = self.calc_stats()
        return self.weights[0] * healthy * 100 + self.weights[1] * extinguished * 100 - self.weights[2] * time

    def get_neighbor_indices(self, row, column):
        position = []
        if self.grid == "rectangular":
            if column == 0 and row == 0:
                position.append((row, column + 1))
                position.append((row + 1, column))
                position.append((row + 1, column + 1))
                return position
            if column == 0:
                if row > self.rows - 2:
                    position.append((row - 1, column))
                    position.append((row - 1, column + 1))
                    position.append((row, column + 1))
                    return position
                position.append((row - 1, column))
                position.append((row - 1, column + 1))
                position.append((row, column + 1))
                position.append((row + 1, column))
                position.append((row + 1, column + 1))
                return position
            if row == 0:
                if column > self.columns - 2:
                    position.append((row, column - 1))
                    position.append((row + 1, column - 1))
                    position.append((row + 1, column))
                    return position
                position.append((row, column - 1))
                position.append((row, column + 1))
                position.append((row + 1, column - 1))
                position.append((row + 1, column))
                position.append((row + 1, column + 1))
                return position
            if row > self.rows - 2 and column > self.columns - 2:
                position.append((row - 1, column - 1))
                position.append((row - 1, column))
                position.append((row, column - 1))
                return position
            if column > self.columns - 2:
                position.append((row - 1, column - 1))
                position.append((row - 1, column))
                position.append((row, column - 1))
                position.append((row + 1, column - 1))
                position.append((row + 1, column))
                return position
            if row > self.rows - 2:
                position.append((row - 1, column - 1))
                position.append((row - 1, column))
                position.append((row - 1, column + 1))
                position.append((row, column - 1))
                position.append((row, column + 1))
                return position
            position.append((row - 1, column - 1))
            position.append((row - 1, column))
            position.append((row - 1, column + 1))
            position.append((row, column - 1))
            position.append((row, column + 1))
            position.append((row + 1, column - 1))
            position.append((row + 1, column))
            position.append((row + 1, column + 1))
            return position
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


class AgentModel(Forest):
    
    def __init__(self, initmode):
        self.retardant = 100
        super().__init__(initmode)
        self.memory = np.zeros(self.number_agents)

    def get_possible_moves(self, row, column):
        return self.get_neighbor_indices(row, column)

    def move(self, row, column, agent_index):
        lowest = 1000
        next_row = row
        next_col = column
        possible_moves = self.get_possible_moves(row, column)
        for neighbor_row, neighbor_col in possible_moves:
            if self.mode == "Haksar":
                cost = self.calc_cost_haksar(neighbor_row, neighbor_col, agent_index)
            elif self.mode == "Heuristic":
                cost = self.calc_cost_heuristic(neighbor_row, neighbor_col)
            elif self.mode == "user":
                cost = self.calc_cost_user(neighbor_row, neighbor_col)
            else:
                print("Agent Mode unknown")
                pass
            if cost <= lowest:
                lowest = cost
                next_row = neighbor_row
                next_col = neighbor_col
        self.agents[agent_index] = (next_row, next_col)

    def move_neu(self, agent_index):
        if self.mode == "Haksar":
            (next_row, next_col) = self.move_Haksar()
        self.agents[agent_index] = (next_row, next_col)

    def calc_cost_heuristic(self, row, column):
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

    def calc_cost_user(self, row, column):
        # user defined strategie finding algorithm goes here.
        # return the cost for specific neighbor position (row, column)
        return 1

    def apply_control_actions(self, row, col):
        if self.forest[row, col] == 2:
            self.actions[row, col] = 1
            self.agent_transition(row, col)
        self.actions[row, col] = 0

    def agent_transition(self, row, col):
        prob_ext = self.actions[row, col] * self.delta_beta
        prob = random.randint(0, 100)
        if (prob_ext * 100) > prob:
            self.forest[row, col] = 4

    def memorize(self, row, col, agent_index):
        if self.forest[row, col] == 2 or self.forest[row, col] == 3:
            self.memory[agent_index] = 1

    def act(self):
        agent_index = 0
        for (row, column) in self.agents:
            self.move(row, column, agent_index)
            self.memorize(row, column, agent_index)
            self.apply_control_actions(row, column)
            agent_index += 1


'''
## TODO ##
restructure code and rely on clean code! (for master branch)
Wind und Fire spreading
optimize the way to distinguish between different modes: methods, that call the different methods based on the mode
'''