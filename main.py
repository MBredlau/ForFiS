#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 20:28:43 2021

@author: marvin
"""

import Forest
import time
import hexalattice as hexa
import matplotlib
import matplotlib.pyplot as plt
matplotlib.interactive(True)
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
#from matplotlib.figure import Figure
import tkinter as tk
        
    
class simulation(Forest.Fire_model, Forest.Agent_model):
    def __init__(self, GUI):
        self.columns = 21
        self.rows = 21
        likelihood_to_ignite = GUI.alpha_regler.get() #3 # indicator [0, 10], higher value leads to a higher prob to ignite the neighbor trees
        self.likelihood = 1 - likelihood_to_ignite * 0.1 # higher likelihood leads to a lower probability to ignite the trees
        fire_agression = GUI.beta_regler.get() # indicator [0, 10]. higher value leads to a faster burning down
        self.beta = fire_agression * 0.1#(10 - fire_agression) * 0.1
        self.delta_beta = 0.5 # efficiency of extinguishing action
        self.timesteps = GUI.timesteps_regler.get()
        self.delta_time = 0.5
        self.fig = GUI.fig
        self.a = GUI.a
        fire_source = 'centrum' # init random or centrum
        super().__init__(self.rows, self.columns, fire_source)
                

class GUi():

    def __init__(self):    
        
        self.fig = plt.figure()
        self.a = self.fig.add_subplot(111)
        self.fenster = tk.Tk()
        self.fenster.title("Forest Fire Simulation")
        self.top_frame = tk.Frame(self.fenster)
        self.top_frame.pack()
        self.left_frame = tk.Frame(self.top_frame)
        self.left_frame.pack(side=tk.LEFT)
        self.frame2 = tk.Frame(self.top_frame)
        self.frame2.pack(side = tk.LEFT)
        self.frame3 = tk.Frame(self.top_frame)
        self.frame3.pack(side = tk.RIGHT)
        
        self.bottom_frame = tk.Frame(self.fenster)
        self.bottom_frame.pack(side=tk.BOTTOM)

        
        self.alpha_regler = tk.Scale(self.left_frame, from_=0, to=10, orient=tk.HORIZONTAL)
        self.alpha_regler.set(3)
        self.alpha_regler.pack()
        self.alpha_label = tk.Label(self.left_frame, text="Ignition Likelihood")
        self.alpha_label.pack()
        
        self.beta_regler = tk.Scale(self.frame2, from_=0, to=10, orient=tk.HORIZONTAL)
        self.beta_regler.set(4)
        self.beta_regler.pack()
        self.beta_label = tk.Label(self.frame2, text="Fire Agression")
        self.beta_label.pack()
        
        self.timesteps_regler = tk.Scale(self.frame3, from_=0, to=20, orient=tk.HORIZONTAL)
        self.timesteps_regler.set(15)
        self.timesteps_regler.pack()
        self.timesteps_label = tk.Label(self.frame3, text="Timesteps")
        self.timesteps_label.pack()
        
        scenario = simulation(self)
        self.canvas = FigureCanvasTkAgg(scenario.fig, master=self.bottom_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.bottom_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.start_button = tk.Button(self.bottom_frame, text="Start", command=self.start_simulation)
        self.start_button.pack()
        
        self.fenster.mainloop()

    def start_simulation(self):
        scenario = simulation(self)
        scenario.plot()
        for i in range(0, scenario.timesteps):
            time.sleep(scenario.delta_time)
            scenario.transition()
            scenario.plot()
            scenario.act()


GUI = GUi()

hex_centers, _ = hexa.create_hex_grid(nx=5,
                                 ny=5,
                                 face_color=[[0.9, 0.1, 0.1, 0.05], [0.9, 0.1, 0.1, 0.05]],
                                 do_plot=True)
                                 
plt.show() 



