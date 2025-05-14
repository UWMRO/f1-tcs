#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thurs May 5 2025
@title: Target tab GUI components
@author: Parker Lamb
@description: Qt6 widgets to assist with targeting and target list setup. 
"""

from PySide6.QtGui import QPalette
from PySide6.QtWidgets import (QComboBox, QFileDialog, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QGridLayout, QTableWidget)
from matplotlib import (colors, pyplot)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import qtawesome as qta
from astropy.time import Time
from astroplan.plots import (plot_airmass, dark_style_sheet)
from astroplan import Observer, FixedTarget
from .misc import MPLImage

class CurrentTarget(QGroupBox):
    """
    Group box which contains current target info. 
    """
    def __init__(self):
        """
        Current target params.
        """
        super().__init__()

        # We want two columns: text entry left, buttons right
        layout = QGridLayout(self)

        # In the text entry colunn, add another group box to allow for two forms
        tglayout = QGridLayout()
        tglayout.setSpacing(10)
        layout.addLayout(tglayout, 0, 0, 4, 1) # May need to resize to occupy multiple rows/columns

        # Add buttons to the right
        search_button = QPushButton(qta.icon('fa5s.search'), '')
        search_button.setToolTip("Query online databases for target name")
        totable_button = QPushButton(qta.icon('fa5s.angle-double-down'), '')
        totable_button.setToolTip("Add to observation table")
        layout.addWidget(search_button, 0, 1)
        layout.addWidget(totable_button, 3, 1)

        # Add form layouts
        top_name_layout = QFormLayout()
        mid_dec_layout = QFormLayout()
        mid_alt_layout = QFormLayout()
        bot_epoch_layout = QFormLayout()
        tglayout.addLayout(top_name_layout, 0, 0, 1, -1)
        tglayout.addLayout(mid_dec_layout, 1, 0)
        tglayout.addLayout(mid_alt_layout, 1, 1)
        tglayout.addLayout(bot_epoch_layout, 3, 0, 1, -1)

        # Create params
        self.targetName = QLineEdit()
        self.targetRA = QLineEdit()
        self.targetDec = QLineEdit()
        self.targetAlt = QLineEdit()
        self.targetAz = QLineEdit()
        self.targetEpoch = QLineEdit()
        self.targetEpoch.setText("J2000")

        # Disable alt/az, TODO
        self.targetAlt.setDisabled(True)
        self.targetAz.setDisabled(True)
    
        # Add params to layout
        top_name_layout.insertRow(0, "Name", self.targetName)
        mid_dec_layout.insertRow(0, "RA     ", self.targetRA)
        mid_dec_layout.insertRow(1, "Dec", self.targetDec)
        mid_alt_layout.insertRow(0, "Alt", self.targetAlt)
        mid_alt_layout.insertRow(1, "Az", self.targetAz)
        bot_epoch_layout.insertRow(0, "Epoch", self.targetEpoch)

    def get_params(self):
        """
        Return the parameters of the box.

        Returns
        -------
        params : list
        """
        # Set the placeholder text to the actual text if run without an entry
        name = self.targetName.text()
        ra = self.targetRA.text()
        dec = self.targetDec.text()
        alt = self.targetAlt.text()
        az = self.targetAz.text()
        epoch = self.targetEpoch.text()

        return([name, ra, dec, alt, az, epoch])

class ObservationTable(QWidget):
    def __init__(self):
        """
        Observation table widget
        """
        super().__init__()

        # Let's start with a QVBox
        layout = QVBoxLayout(self)
        
        # Add table header
        header_layout = QHBoxLayout()
        layout.addLayout(header_layout)

        obslabel = QLabel()
        obslabel.setText("Observation table")
        header_layout.addWidget(obslabel)
        header_layout.addStretch(1)

        # Add buttons
        open_btn = QPushButton(qta.icon('fa6s.folder-open'), '')
        save_btn = QPushButton(qta.icon('fa5s.save'), '')
        open_btn.setToolTip("Open list of targets")
        save_btn.setToolTip("Save CSV of targets")

        header_layout.addWidget(open_btn)
        header_layout.addWidget(save_btn)
        header_layout.addStretch(20)
        
        up_btn = QPushButton(qta.icon('ei.chevron-up'), '')
        down_btn = QPushButton(qta.icon('ei.chevron-down'), '')
        trash_btn = QPushButton(qta.icon('fa6s.trash-can'), '')
        up_btn.setToolTip("Move selected target up")
        down_btn.setToolTip("Move selected target down")
        trash_btn.setToolTip("Delete selected target")
        header_layout.addWidget(up_btn)
        header_layout.addWidget(down_btn)
        header_layout.addWidget(trash_btn)

        # Add the actual table now
        self.table = QTableWidget(0,4)
        self.table.setHorizontalHeaderLabels(["Target", "RA", "Dec", "Epoch"])
        layout.addWidget(self.table)

class AirmassSkyplotImages(QWidget):
    def __init__(self):
        """
        Airmass and Skyplot images for the targeting tab. 
        """
        super().__init__()

        # Define observer
        observer = Observer.at_site("mro", timezone="America/Vancouver")
        observe_time = Time.now()

        # Layout
        layout = QVBoxLayout(self)

        # Airmass image
        self.amImg = MPLImage()
        tgt = FixedTarget.from_name("Vega")
        plot_airmass(tgt, observer, observe_time, self.amImg.ax)
        layout.addWidget(self.amImg)

        # Skyplot image
        self.spImg = MPLImage()
        layout.addWidget(self.spImg)

    def plot_airmass(self, target):
        """
        Plot airmass on its respective image.
        """

    def plot_skyplot(self):
        """
        Plot skyplot on its respective image.
        """

class TargetWidget(QWidget):
    def __init__(self):
        """
        Container widget used when the "Target" tab is selected.
        """
        super().__init__()

        # Grand layout
        layout = QHBoxLayout(self)

        # Add a left column for target box, observation table
        left_column = QVBoxLayout()
        layout.addLayout(left_column)

        # Target specification box
        targetBox = CurrentTarget()
        targetBox.setMinimumWidth(450)
        left_column.addWidget(targetBox)

        # Observation table box
        self.obsTable = ObservationTable()
        left_column.addWidget(self.obsTable)

        # Add a right column for SkyPlots and Airmass Plots
        right_column = QVBoxLayout()
        layout.addLayout(right_column)

        # Add images to column
        images = AirmassSkyplotImages()
        right_column.addWidget(images)