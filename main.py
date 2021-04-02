#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 20:28:43 2021

@author: marvin
"""

import Forest
import time
import hexalattice as hexa
import matplotlib.pyplot as plt
import tkinter as tk
        
class simulation(Forest.Fire_model, Forest.Agent_model):
    def __init__(self):
        self.columns = 21
        self.rows = 21
        likelihood_to_ignite = 3 # indicator [0, 10], higher value leads to a higher prob to ignite the neighbor trees
        self.likelihood = 1 - likelihood_to_ignite * 0.1 # higher likelihood leads to a lower probability to ignite the trees
        fire_agression = 4 # indicator [0, 10]. higher value leads to a faster burning down
        self.beta = (10 - fire_agression) * 0.1
        self.delta_beta = 0.5 # efficiency of extinguishing action
        self.timesteps = 20
        fire_source = 'centrum' # init random or centrum
        super().__init__(self.rows, self.columns, fire_source)
                
def start_simulation():
    scenario = simulation()
    scenario.plot()
    for i in range(0, scenario.timesteps):
        time.sleep(0.5)
        scenario.transition()
        scenario.plot()
        scenario.act()

#plt.figure(clear=True)

fenster = tk.Tk()
fenster.title("Nur ein Fenster")
start_button = tk.Button(fenster, text="Start", command=start_simulation)
start_button.pack()
fenster.mainloop()
#plt.show()
hex_centers, _ = hexa.create_hex_grid(nx=5,
                                 ny=5,
                                 face_color=[[0.9, 0.1, 0.1, 0.05], [0.9, 0.1, 0.1, 0.05]],
                                 do_plot=True)
                                 
plt.show() 













