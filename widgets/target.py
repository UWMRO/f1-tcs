#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thurs May 5 2025
@title: Target tab GUI components
@author: Parker Lamb
@description: Qt6 widgets to assist with targeting and target list setup. 
"""

import numpy as np
from PySide6.QtGui import QPalette
from PySide6.QtCore import QDate
from PySide6.QtWidgets import (QComboBox, QFileDialog, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QGridLayout, QTableWidget, QTableWidgetItem, QDateTimeEdit)
from matplotlib import (colors, pyplot)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import qtawesome as qta
from astropy.time import Time
from astroplan.plots import (plot_airmass, plot_sky, dark_style_sheet)
from astroplan import Observer, FixedTarget
from .misc import MPLCanvas, MPLCanvas_Polar

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
        self.totable_button = QPushButton(qta.icon('fa5s.angle-double-down'), '')
        self.totable_button.setToolTip("Add to observation table")
        layout.addWidget(search_button, 0, 1)
        layout.addWidget(self.totable_button, 3, 1)

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

        # Disable alt/az, TODO remove?
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
        self.observer = Observer.at_site("mro", timezone="America/Vancouver")
        self.observe_time = Time.now()

        # Layout
        layout = QVBoxLayout(self)

        # Airmass image
        self.amImg = MPLCanvas(self, dpi=100)
        self.plot_airmass()
        layout.addWidget(self.amImg)

        # Skyplot image
        self.spImg = MPLCanvas_Polar(self, dpi=100)
        layout.addWidget(self.spImg)

        # Add a 'time selector' for the images
        timeBox = QGroupBox()
        timeLayout = QHBoxLayout()
        timeBox.setLayout(timeLayout)

        deets_label = QLabel()
        self.time_start = QDateTimeEdit(QDate.currentDate())
        # self.time_end = QDateTimeEdit(QDate.currentDate().addDays(1))
        time_label = QLabel()
        self.refresh_button = QPushButton(qta.icon('mdi.refresh'), '')
        self.refresh_button.setMaximumWidth(30)
        self.time_start.setDisplayFormat('MM/dd @ HH:mm')
        # self.time_end.setDisplayFormat('MM/dd @ HH:mm')
        deets_label.setText("Night start:")
        time_label.setText("PT")

        timeLayout.addWidget(deets_label)
        timeLayout.addWidget(self.time_start)
        # timeLayout.addWidget(self.time_end)
        timeLayout.addWidget(time_label)
        timeLayout.addWidget(self.refresh_button)
        layout.addWidget(timeBox)

    def plot_airmass(self, targets=[]):
        """
        Plot some targets on an image
        """
        self.amImg.axes.cla()
        # plot_airmass(targets, self.observer, self.observe_time.to_datetime(timezone=self.observer.timezone), self.amImg.axes, use_local_tz=True, brightness_shading=True)
        plot_airmass(targets, self.observer, self.observe_time.to_datetime(timezone=self.observer.timezone), self.amImg.axes, use_local_tz=True, brightness_shading=True)
        if len(targets) > 0:
            self.amImg.axes.legend()

        # We need to reset the axes title sizing for some reason
        self.amImg.axes.yaxis.get_label().set_fontsize(7)
        self.amImg.axes.xaxis.get_label().set_fontsize(7)

        self.amImg.draw()

    def plot_skyplot(self, targets=[]):
        """
        Plot skyplot on its respective image.
        """
        for target in targets:
            # TODO color variations per target
            plot_sky(target, self.observer, self.observe_time, self.spImg.axes)
            self.spImg.axes.legend(bbox_to_anchor=(1.25, 0))

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
        self.targetBox = CurrentTarget()
        self.targetBox.setMinimumWidth(500)
        left_column.addWidget(self.targetBox)
        
        # Observation table box
        self.obsTable = ObservationTable()
        left_column.addWidget(self.obsTable)

        # Add a right column for SkyPlots and Airmass Plots
        right_column = QVBoxLayout()
        layout.addLayout(right_column)

        # Add images to column
        self.images = AirmassSkyplotImages()
        right_column.addWidget(self.images)

        # Add button functionality
        self.targetBox.totable_button.clicked.connect(self.copy_target_to_table)
        self.images.refresh_button.clicked.connect(self.update_plot_timerange)

    def copy_target_to_table(self):
        """
        Copy the current target to the targets table.
        """
        # current_data = [name, ra, dec, alt, az, epoch]
        current_data = self.targetBox.get_params()

        # QTableWidgetItem is a per-cell widget
        name = QTableWidgetItem(current_data[0])
        ra = QTableWidgetItem(current_data[1])
        dec = QTableWidgetItem(current_data[2])
        epoch = QTableWidgetItem(current_data[5])

        # Get current row # and add a new one
        current_row = self.obsTable.table.rowCount()
        self.obsTable.table.insertRow(current_row)
        for col, entry in zip(range(4), [name, ra, dec, epoch]):
            self.obsTable.table.setItem(current_row, col, entry)
    
    def update_plot_timerange(self):
        """
        Update the timeranges for airmass and skyplot.
        """
        time_start = self.images.time_start.dateTime()
        # time_end = self.images.time_end.dateTime() # We don't need this, just go until sunrise-ish

        # We're still operating in PT here - convert to astropy Time objects
        start_pydt = Time(time_start.toPyDateTime())
        # end_pydt = Time(time_end.toPyDateTime())
        # dt = end_pydt - start_pydt
        observe_time = start_pydt

        # Update observe time and replot both
        self.images.observe_time = observe_time
        self.images.plot_airmass()
        self.images.plot_skyplot()

    def update_plots_from_table(self):
        """
        Update each plot with the corresponding data from a table entry. 
        """