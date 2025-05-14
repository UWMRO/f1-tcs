#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 13 2025
@title: Misc functions and widgets
@author: Parker Lamb
@description: Contains misc widgets and functions
"""

from matplotlib import pyplot, colors
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPalette

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

        # Add matplotlib canvas to layout
        self.figure = pyplot.figure()
        self.ax = self.figure.add_axes([0,0,1,1])
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout.addWidget(self.canvas)

        # Set the background color of the canvas
        win_color = self.palette().color(QPalette.Window).getRgbF()
        plot_color = colors.rgb2hex(win_color)
        self.figure.set_facecolor(plot_color)

        # Hide the axes
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)

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

    def set_image(self, img):
        """
        Set the axes to the image and refresh canvas.

        Parameters
        ----------
        img : ndarray
        """
        self.ax.cla()
        self.ax.imshow(img, origin="lower")
        # Refresh the canvas
        self.ax.draw_artist(self.ax.patch)
        self.canvas.update()
        # self.canvas.flush_events()
        self.canvas.draw()
    
    def plot(self, tracings, color = 'blue'):
        """
        Plot the provided tracings on the axes.

        Parameters
        ----------
        tracings : list
            List of format [[x], [y]
        color : String (optional)
            color to plot in
        """
        self.ax.plot(tracings[0], tracings[1], color=color)
        self.ax.draw_artist(self.ax.patch)
        self.canvas.update()
        # self.canvas.flush_events()
        self.canvas.draw()