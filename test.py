#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 16:07:32 2021

@author: marvin
"""

import numpy as np

arr = np.array([[11,12,13,14,15],[21,22,23,24,25],[31,32,33,34,35],[41,42,43,44,45],[51,52,53,54,55]])
for i in range(0,5):
    for j in range(0,5):
        if j == 0:
            print(arr[i : i + 2, j : j + 2])
            continue
        if i == 0:
            print(arr[i : i + 2, j - 1: j + 2])
            result = np.count_nonzero(arr[i:i+2,j:j+2]==22)
        else:
            result = np.count_nonzero(arr[i-1:i+2,j-1:j+2]==22)
            print(arr[i - 1 : i + 2, j - 1 : j + 2])
        #print(arr[i - 1, 2])
        
        #print(np.count_nonzero(arr[i-1:i+2,j-1:j+2]==22))
        print(result)
