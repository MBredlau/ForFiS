#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 20:28:43 2021

@author: marvin
"""

import Forest
import time
        
class simulation(Forest.Fire_model, Forest.Agent_model):
    def __init__(self, initmode):
        self.columns = 10
        self.rows = 10
        likelihood_to_ignite = 3 # indicator [0, 10], higher value leads to a higher prob to ignite the neighbor trees
        self.likelihood = 1 - likelihood_to_ignite * 0.1 # higher likelihood leads to a lower probability to ignite the trees
        fire_agression = 4 # indicator [0, 10]. higher value leads to a faster burning down
        self.beta = (10 - fire_agression) * 0.1
        print(self.beta)
        self.delta_beta = 0.5
        self.timesteps = 15
        super().__init__(self.rows, self.columns, initmode)
                
scenario = simulation('centrum') # init random or centrum
scenario.plot()
for i in range(0, scenario.timesteps):
    time.sleep(0.5)
    scenario.transition()
    scenario.plot()
    scenario.act()














