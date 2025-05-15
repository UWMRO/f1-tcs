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
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from qbstyles import mpl_style

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