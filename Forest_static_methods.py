import math
import numpy as np


def euclidean_distance(row1, col1, row2, col2):
    return math.sqrt((row1 - row2) ** 2 + (col1 - col2) ** 2)


def vector(neighbor, current_position, grid='hexagonal'):
    vec = current_position - neighbor
    if grid == 'hexagonal':
        return vector_hex(vec, current_position[0])
    if grid == 'rectangular':
        return vector_rect(vec)
    return 1


def vector_rect(vec):
    if np.array_equal(vec, np.array([1, 1])):
        return [math.sqrt(2) / 2, math.sqrt(2) / 2]
    if np.array_equal(vec, np.array([1, 0])):
        return [1, 0]
    if np.array_equal(vec, np.array([0, 1])):
        return [0, 1]
    if np.array_equal(vec, np.array([1, -1])):
        return [math.sqrt(2) / 2, - math.sqrt(2) / 2]
    if np.array_equal(vec, np.array([0, -1])):
        return [0, -1]
    if np.array_equal(vec, np.array([-1, 1])):
        return [- math.sqrt(2) / 2, math.sqrt(2) / 2]
    if np.array_equal(vec, np.array([-1, 0])):
        return [-1, 0]
    if np.array_equal(vec, np.array([-1, -1])):
        return [- math.sqrt(2) / 2, - math.sqrt(2) / 2]
    return [1, 1]


def vector_hex(vec, row):
    if row % 2:  # in odd rows
        if np.array_equal(vec, np.array([1, 1])):
            return [1/2, math.sqrt(3)/2]
        if np.array_equal(vec, np.array([0, 1])):
            return [1, 0]
        if np.array_equal(vec, np.array([1, 0])):
            return [-1/2, math.sqrt(3)/2]
        if np.array_equal(vec, np.array([-1, 1])):
            return [1/2, -math.sqrt(3)/2]
        if np.array_equal(vec, np.array([-1, 0])):
            return [-1/2, -math.sqrt(3)/2]
        if np.array_equal(vec, np.array([0, -1])):
            return [-1, 0]
        return [1, 1]
    else:  # in even rows
        if np.array_equal(vec, np.array([1, 0])):
            return [1/2, math.sqrt(3) / 2]
        if np.array_equal(vec, np.array([0, 1])):
            return [1, 0]
        if np.array_equal(vec, np.array([1, -1])):
            return [-1/2, math.sqrt(3) / 2]
        if np.array_equal(vec, np.array([-1, 0])):
            return [1/2, -math.sqrt(3) / 2]
        if np.array_equal(vec, np.array([-1, -1])):
            return [-1/2, -math.sqrt(3) / 2]
        if np.array_equal(vec, np.array([0, -1])):
            return [-1, 0]
        return [1, 1]