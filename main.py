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
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)  # , NavigationToolbar2Tk)
import tkinter as tk
import yaml
matplotlib.interactive(True)
matplotlib.use("TkAgg")
        

# read standard simulation parameters from config file
with open("config.yml", "r") as configfile:
    config = yaml.load(configfile, Loader=yaml.FullLoader)

size = config["size"]
alpha = config["alpha"]
beta = config["beta"]
delta_beta = config["delta_beta"]
agents = config["agents"]
timesteps = config["timesteps"]
use_gui = config["gui"]
use_config_file = True





class Simulation(Forest.FireModel, Forest.AgentModel):

    def __init__(self, GUI):
        if use_gui:
            self.columns = GUI.size_slider.get()  # should both be odd for low numbers. Looks awful otherwise
            self.rows = self.columns
            self.number_agents = GUI.agents_slider.get()
            self.mode = "Haksar"  # Haksar or Heuristik
            likelihood_to_ignite = GUI.alpha_slider.get()  # [0, 10] higher value leads to higher prob to ignite trees
            self.likelihood = 1 - likelihood_to_ignite * 0.1  # higher likelihood leads to lower probability to ignite trees
            fire_persistence = GUI.beta_slider.get()  # indicator [0, 10]. higher value -> fire persists longer
            self.beta = fire_persistence * 0.1
            self.delta_beta = GUI.delta_beta_slider.get() * 0.1  # efficiency of extinguishing action
            self.timesteps = 5  # GUI.timesteps_slider.get()
            self.delta_time = 0
            self.fig = GUI.fig
            self.a = GUI.a
            fire_source = 'centre'  # init random or centre
        else:
            self.columns = size  # should both be odd for low numbers. Looks awful otherwise
            self.rows = self.columns
            self.number_agents = agents
            self.mode = config["mode"] # Haksar or Heuristik
            likelihood_to_ignite = alpha  # [0, 10] higher value leads to higher prob to ignite trees
            self.likelihood = 1 - likelihood_to_ignite * 0.1  # higher likelihood leads to lower probability to ignite trees
            fire_persistence = beta  # indicator [0, 10]. higher value -> fire persists longer
            self.beta = fire_persistence * 0.1
            self.delta_beta = delta_beta * 0.1  # efficiency of extinguishing action
            self.timesteps = timesteps
            self.delta_time = 0
            fire_source = 'centre'  # init random or centre
            print("Test")
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
        self.frame1 = tk.Frame(self.top_frame)
        self.frame1.pack(side=tk.LEFT)
        self.frame2 = tk.Frame(self.top_frame)
        self.frame2.pack(side=tk.LEFT)
        self.frame3 = tk.Frame(self.top_frame)
        self.frame3.pack(side=tk.LEFT)
        self.frame4 = tk.Frame(self.top_frame)
        self.frame4.pack(side=tk.LEFT)
        self.frame5 = tk.Frame(self.top_frame)
        self.frame5.pack(side=tk.RIGHT)

        self.bottom_frame = tk.Frame(self.window)
        self.bottom_frame.pack(side=tk.BOTTOM)

        self.alpha_slider = tk.Scale(self.left_frame, from_=0, to=10, orient=tk.HORIZONTAL)
        self.alpha_slider.set(alpha)
        self.alpha_slider.pack()
        self.alpha_label = tk.Label(self.left_frame, text="Ignition Likelihood")
        self.alpha_label.pack()

        self.beta_slider = tk.Scale(self.frame1, from_=0, to=10, orient=tk.HORIZONTAL)
        self.beta_slider.set(beta)
        self.beta_slider.pack()
        self.beta_label = tk.Label(self.frame1, text="Fire Persistence")
        self.beta_label.pack()

        self.delta_beta_slider = tk.Scale(self.frame2, from_=0, to=10, orient=tk.HORIZONTAL)
        self.delta_beta_slider.set(delta_beta)
        self.delta_beta_slider.pack()
        self.delta_beta_label = tk.Label(self.frame2, text="Retardant Efficiency")
        self.delta_beta_label.pack()

        self.size_slider = tk.Scale(self.frame3, from_=5, to=41, orient=tk.HORIZONTAL)
        self.size_slider.set(size)
        self.size_slider.pack()
        self.size_label = tk.Label(self.frame3, text="Forest Size")
        self.size_label.pack()

        self.agents_slider = tk.Scale(self.frame4, from_=0, to=8, orient=tk.HORIZONTAL)
        self.agents_slider.set(agents)
        self.agents_slider.pack()
        self.agents_label = tk.Label(self.frame4, text="Number of Agents")
        self.agents_label.pack()

        self.timesteps_slider = tk.Scale(self.frame5, from_=0, to=20, orient=tk.HORIZONTAL)
        self.timesteps_slider.set(timesteps)
        self.timesteps_slider.pack()
        self.timesteps_label = tk.Label(self.frame5, text="Time steps")
        self.timesteps_label.pack()

        scenario = Simulation(self)
        self.canvas = FigureCanvasTkAgg(scenario.fig, master=self.bottom_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.start_button = tk.Button(self.bottom_frame, text="Start", command=self.start_simulation)
        self.start_button.pack()

        self.window.mainloop()

    def start_simulation(self):
        scenario = Simulation(self)
        scenario.plot()
        for i in range(0, scenario.timesteps * (1 + (scenario.number_agents > 0) * 5)):
            time.sleep(scenario.delta_time)
            if not i % 6:
                scenario.transition()
            scenario.plot()
            if scenario.number_agents:
                scenario.act()


if use_gui:
    GUI = GUi()
else:
    scenario = Simulation(None)
    # scenario.plot()
    for i in range(0, scenario.timesteps * (1 + (scenario.number_agents > 0) * 5)):
        time.sleep(scenario.delta_time)
        if not i % 6:
            scenario.transition()
        #  scenario.plot()
        if scenario.number_agents:
            scenario.act()
