#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 13 2025
@title: Misc functions and widgets
@author: Parker Lamb
@description: Contains misc widgets and functions
"""

from matplotlib import pyplot, colors, rcParams
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import FigureCanvas
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from qbstyles import mpl_style

# Set darkmode from qbstyles
mpl_style(dark=True)

class MPLCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=1.5, dpi=200):
        """
        Custom class for the base image.
        
        See https://www.pythonguis.com/tutorials/pyqt6-plotting-matplotlib/
        """
        fig = Figure(dpi=dpi)
        self.axes = fig.add_subplot(111)
        # fig, self.axes = plt.subplots(dpi)

        # Some adjustment necessary to convince plot to look okay
        self.axes.tick_params(labelsize=6)
        self.axes.xaxis.label.set_size(6)
        self.axes.yaxis.label.set_size(6)
        fig.tight_layout()
        fig.subplots_adjust(left=0.16, bottom=0.25)  # try values like 0.15–0.25
        
        # Initialize base function with above params
        super().__init__(fig)

class MPLCanvas_Polar(FigureCanvas):
    def __init__(self, parent=None, width=5, height=1.5, dpi=200):
        """
        Custom class for the base image.
        
        See https://www.pythonguis.com/tutorials/pyqt6-plotting-matplotlib/
        """
        fig = Figure(dpi=dpi)
        self.axes = fig.add_subplot(111, projection='polar')
        # fig, self.axes = plt.subplots(subplot_kw={'projection': 'polar'}, dpi=dpi)

        # Some adjustment necessary to convince plot to look okay
        self.axes.tick_params(labelsize=6)
        self.axes.xaxis.label.set_size(6)
        self.axes.yaxis.label.set_size(6)
        fig.tight_layout()
        # fig.subplots_adjust(top=0.01)  # try values like 0.15–0.25
        
        # Initialize base function with above params
        super().__init__(fig)

class MPLImage(QWidget):
    def __init__(self, title=''):
        """
        Custom class for the base image.
        """
        super().__init__()

        # Create the layout for the image
        layout = QVBoxLayout(self)

        # Add a title widget
        self.title = QLabel(title)
        layout.addWidget(self.title)

        # Enable darkmode
        mpl_style(dark=True)
        rcParams['figure.dpi'] = 50 # TODO potentially remove this
        # pyplot.style.use('dark_background')

        # Add matplotlib canvas to layout
        self.figure = pyplot.figure()
        self.ax = self.figure.add_axes([0,0,1,1])
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout.addWidget(self.canvas)

        # Hide the axes
        self.ax.get_xaxis().set_visible(True)
        self.ax.get_yaxis().set_visible(True)
        self.ax.grid()

        # Hide title if not set to anything
        if len(title) == 0:
            self.title.setVisible(False)
    
    def set_title(self, title):
        """
        Sets the title of the MPLImage.

        Parameters
        ----------
        title : str
        """
        self.title.setText(str(title))

    def refresh(self):
        """
        Refresh canvas.
        """
        # Refresh the canvas
        self.ax.draw_artist(self.ax.patch)
        self.canvas.update()
        # self.canvas.flush_events()
        self.canvas.draw()