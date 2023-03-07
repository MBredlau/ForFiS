#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 20:28:43 2021

@author: marvin
"""
import numpy as np
import Forest
import time
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import tkinter as tk
import yaml
import sys
import os
from datetime import datetime
matplotlib.interactive(True)
matplotlib.use("TkAgg")

# Enter the name of the config file here
config_name = "config.yml"        

try:
    # read standard simulation parameters from config file
    with open(config_name, "r") as configfile:
        config = yaml.load(configfile, Loader=yaml.FullLoader)

    size = config["size"]
    alpha = config["alpha"]
    beta = config["beta"]
    delta_beta = config["delta_beta"]
    alpha_wind = config["alpha_wind"]
    wind_x = config["wind_x"]
    wind_y = config["wind_y"]
    wind = np.array([wind_x, wind_y])
    memoryless = config["memoryless"]
    agents = config["agents"]
    timesteps = config["timesteps"]
    mode = config["mode"]
    grid = config["grid"]
    weights = config["healthy"], config["extinguished"], config["time"]
    USE_GUI = config["gui"]
    USE_LOGFILE = config["logfile"]
    print("Loaded config file")
except:
    size = 22
    alpha = 7
    beta = 4
    delta_beta = 10
    alpha_wind = 10
    wind = ([2, 0])
    memoryless = False
    agents = 3
    timesteps = 5
    mode = "Haksar"
    grid = "hexagonal"
    weights = 0.6, 0.2, 0.2
    USE_GUI = True
    USE_LOGFILE = False
    print("Parameters loaded from main.py. If you want to use the config file, make sure it is named correctly and "
          "located in the right path")

if USE_LOGFILE:
    temp_stdout = sys.stdout
    filename = "log" + datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    completeName = os.path.join('./logfiles', filename)
    sys.stdout = open(completeName + ".txt", "w")


class Simulation(Forest.FireModel, Forest.AgentModel):

    def __init__(self, GUI):
        if USE_GUI:
            self.columns = GUI.size_slider.get()  # should both be odd for low numbers. Looks bad otherwise
            self.rows = self.columns
            self.number_agents = GUI.agents_slider.get()
            self.mode = mode
            self.grid = grid
            self.memoryless = memoryless
            likelihood_to_ignite = GUI.alpha_slider.get()
            self.alpha_0 = 1 - likelihood_to_ignite * 0.1
            fire_persistence = GUI.beta_slider.get()
            self.beta = fire_persistence * 0.1
            self.delta_beta = GUI.delta_beta_slider.get() * 0.1
            self.alpha_wind = alpha_wind * 0.1
            self.wind = wind
            self.timesteps = GUI.timesteps_slider.get()
            self.delta_time = 0
            self.weights = weights
            self.fig = GUI.fig
            self.a = GUI.a
            fire_source = 'centre'  # init random or centre
        else:
            self.columns = size  # should both be odd for low numbers. Looks bad otherwise
            self.rows = self.columns
            self.number_agents = agents
            self.mode = mode
            self.grid = grid
            likelihood_to_ignite = alpha
            self.alpha_0 = 1 - likelihood_to_ignite * 0.1
            fire_persistence = beta
            self.beta = fire_persistence * 0.1
            self.delta_beta = delta_beta * 0.1
            self.alpha_wind = alpha_wind * 0.1
            self.wind = wind
            self.timesteps = timesteps
            self.delta_time = 0
            self.weights = weights
            fire_source = 'centre'  # init random or centre
        super().__init__(fire_source)

    def simulate(self):
        time.sleep(self.delta_time)
        self.transition()
        if self.number_agents:
            for i in range(6):
                self.act()
                if USE_GUI:
                    self.plot(self.grid)
        else:
            self.plot(self.grid)
        healthy, onfire, burnt, extinguished = self.calc_stats()
        print("trees healthy:", healthy, "on fire:", onfire, "burnt:", burnt, "extinguished:", extinguished)
        return onfire == 0

    def run_sim(self):
        global step
        step = 1
        finished = False
        if timesteps:
            for i in range(0, self.timesteps):
                print("step:", step)
                finished = self.simulate()
                step += 1
                if USE_GUI:
                    if grid == "rectangular":
                        self.plot_rectangular()
                    else:
                        self.plot(self.grid)
                if finished:
                    break
        else:
            while not finished:
                print("step:", step)
                finished = self.simulate()
                step += 1
                if USE_GUI:
                    if grid == "rectangular":
                        self.plot_rectangular()
                    else:
                        self.plot(self.grid)
        print("Simulation finished!")
        print("Overall statistics:")
        print("Chosen strategie finding algorithm:", mode)
        print("Time steps needed:", step)
        healthy, onfire, burnt, extinguished = self.calc_stats()
        print("Trees remained healthy(%):", healthy * 100)
        print("Extinguished Trees(%):", extinguished * 100)
        print("Burnt Trees(%):", burnt * 100)
        success = self.calc_metric(step)
        print("success metric value:", success)


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

        self.agents_slider = tk.Scale(self.frame4, from_=0, to=16, orient=tk.HORIZONTAL)
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
        self.canvas.get_tk_widget().pack(side=tk.TOP)

        self.start_button = tk.Button(self.bottom_frame, text="Start", command=self.start_simulation)
        self.start_button.pack()

        self.window.mainloop()

    def start_simulation(self):
        scenario = Simulation(self)
        if scenario.grid == "rectangular":
            scenario.plot_rectangular()
        else:
            scenario.plot(scenario.grid)
        scenario.run_sim()


if __name__ == '__main__':
    if USE_GUI:
        GUI = GUi()
    else:
        scenario = Simulation(None)
        scenario.run_sim()

    if USE_LOGFILE:
        sys.stdout.close()
        sys.stdout = temp_stdout
