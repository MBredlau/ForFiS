#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 20:28:43 2021

@author: marvin
"""

import Forest
        
class simulation(Forest.Fire_model, Forest.Agent_model):
    def __init__(self, initmode):
        self.columns = 10
        self.rows = 10
        self.likelihood = 0.8
        self.beta = 1
        self.delta_beta = 1
        self.timesteps = 5
        super().__init__(self.rows, self.columns, initmode)
        
#        
scenario = simulation('centrum') # init random or centrum
scenario.plot()
for i in range(0, scenario.timesteps):
    scenario.transition()
    scenario.plot()
    scenario.act()














