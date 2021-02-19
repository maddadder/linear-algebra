from tkinter import * 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  NavigationToolbar2Tk) 

import matplotlib.animation as animation
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
from collections.abc import Sequence
from MyTypes import *
from typing import Dict

from sections import MathSection1


class ScatterPlot:
    def __init__(self, _window):
        # the main Tkinter window 
        self.window = _window
        plt.ioff()
        self.figure = plt.figure()

        self.ax = self.figure.add_subplot(111, projection='3d')
        self.quiver = self.ax.quiver(0, 0, 0, 0, 0, 0, length=1, color='g', arrow_length_ratio=0.1)
        self.plus_quiver = self.ax.quiver(0, 0, 0, 0, 0, 0, length=1, color='g', arrow_length_ratio=0.1)
        self.plot_update_isFirstRun = False
        self.frames = 150
        
    # Smoothing function that acts similar to Bezier smoothing with keyframes.
    # Returns how complete the transformation is on a scale from 0 to 1,
    # based on the current and total frame count
    def sigmoid(self,i):
        return max(1.01799 / (1 + math.exp(-10 / self.frames * i + 4)) - 0.01799, 0)

    def plot(self, example:dict):
        print('plotting')
        self.BACKGROUND_COLOUR = '#000000'
        # Creates points for a grid from -10 to 10 spaced 1 unit apart
        # The grid is 1,000 points by default (10 x 10 x 10)
        self._range = 4
        self.points = self._range / 4
        self.x = ([[x, y, z] for x in np.arange(-self._range, self._range, self.points) for y in np.arange(-self._range, self._range, self.points) for z in np.arange(-self._range, self._range, self.points)])

        # Number of frames in the animation
        
        self.i_origin = example['i_origin']
        self.j_origin = example["j_origin"]
        self.k_origin = example["k_origin"]

        self.i_vector = example["i_vector"]
        self.j_vector = example["j_vector"]
        self.k_vector = example["k_vector"]

        self.i_plus_vector = example["i_plus_vector"]
        self.j_plus_vector = example["j_plus_vector"]
        self.k_plus_vector = example["k_plus_vector"]


        #self.figure.patch.set_facecolor(self.BACKGROUND_COLOUR)
        #self.ax.set_facecolor(self.BACKGROUND_COLOUR)
        self.elevation=5
        self.angle=5
        self.ax.view_init(self.elevation, self.angle)
        self.ax.dist = 5
        self.ax.grid(False)
        plt.axis('off')
        self.ax.set_xlim((-self._range, self._range))
        self.ax.set_ylim((-self._range, self._range))
        self.ax.set_zlim((-self._range, self._range))
        self.scat = self.ax.scatter([], [], marker='.', s=4)
        self.scat.set_offsets(self.x)
        #plt.show()


    def set_title(self, title):
        self.ax.set_title(title)

    def show(self):
        print('showing')

        self.sectionDict: Dict[str, MathSection] = dict()

        self.section1 = MathSection1.MathSection1(self)

        self.sectionDict['section1'] = self.section1.getMathSection()
        self.labels = []
        self.btns = []
        self.index = 0
        self.offset = 1
        for title, section in self.sectionDict.items():
            section.ui.addCanvas()
            self.labels.append(Label(section.ui.frame1, bg='#FFFFFF',text=section.getContent()))
            self.labels[self.index].config(font=('Arial', 14))
            self.labels[self.index].pack() 
            self.plot(section.ui.d)
            #self.btns[self.index].pack()
            section.ui.addUI()
            self.index+=1

    def hide(self):
        self.window.hide()
        self.is_hidden = True

    def destroy(self):
        self.window.destroy()