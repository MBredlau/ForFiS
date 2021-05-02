#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 20:28:43 2021

@author: marvin
"""

import Forest
import time
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk
matplotlib.interactive(True)
matplotlib.use("TkAgg")
        
    
class Simulation(Forest.FireModel, Forest.AgentModel):
    def __init__(self, GUI):
        self.columns = 11  # should both be odd for low numbers. Looks awful otherwise
        self.rows = 11
        likelihood_to_ignite = GUI.alpha_slider.get()  #3 # indicator [0, 10], higher value leads to a higher prob to ignite the neighbor trees
        self.likelihood = 1 - likelihood_to_ignite * 0.1  # higher likelihood leads to a lower probability to ignite the trees
        fire_agression = GUI.beta_slider.get()  # indicator [0, 10]. higher value leads to a faster burning down
        self.beta = fire_agression * 0.1  #(10 - fire_agression) * 0.1
        self.delta_beta = 0.5  # efficiency of extinguishing action
        self.timesteps = GUI.timesteps_slider.get()
        self.delta_time = 0.5
        self.fig = GUI.fig
        self.a = GUI.a
        fire_source = 'centre'  # init random or centre
        super().__init__(fire_source)
                

class GUi:

    def __init__(self):    
        
        self.fig = plt.figure()
        self.a = self.fig.add_subplot(111)
        plt.close()
        self.window = tk.Tk()
        self.window.title("Forest Fire Simulation")
        self.top_frame = tk.Frame(self.window)
        self.top_frame.pack()
        self.left_frame = tk.Frame(self.top_frame)
        self.left_frame.pack(side=tk.LEFT)
        self.frame2 = tk.Frame(self.top_frame)
        self.frame2.pack(side=tk.LEFT)
        self.frame3 = tk.Frame(self.top_frame)
        self.frame3.pack(side=tk.RIGHT)
        
        self.bottom_frame = tk.Frame(self.window)
        self.bottom_frame.pack(side=tk.BOTTOM)
        
        self.alpha_slider = tk.Scale(self.left_frame, from_=0, to=10, orient=tk.HORIZONTAL)
        self.alpha_slider.set(3)
        self.alpha_slider.pack()
        self.alpha_label = tk.Label(self.left_frame, text="Ignition Likelihood")
        self.alpha_label.pack()
        
        self.beta_slider = tk.Scale(self.frame2, from_=0, to=10, orient=tk.HORIZONTAL)
        self.beta_slider.set(4)
        self.beta_slider.pack()
        self.beta_label = tk.Label(self.frame2, text="Fire Agression")
        self.beta_label.pack()
        
        self.timesteps_slider = tk.Scale(self.frame3, from_=0, to=20, orient=tk.HORIZONTAL)
        self.timesteps_slider.set(3)
        self.timesteps_slider.pack()
        self.timesteps_label = tk.Label(self.frame3, text="Time steps")
        self.timesteps_label.pack()
        
        scenario = Simulation(self)
        self.canvas = FigureCanvasTkAgg(scenario.fig, master=self.bottom_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.bottom_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.start_button = tk.Button(self.bottom_frame, text="Start", command=self.start_simulation)
        self.start_button.pack()
        
        self.window.mainloop()

    def start_simulation(self):
        scenario = Simulation(self)
        scenario.plot_hex()
        for i in range(0, scenario.timesteps):
            time.sleep(scenario.delta_time)
            scenario.transition()
            scenario.plot_hex()
            scenario.act()


GUI = GUi()
