#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sat 05.03.25
@title: f1-tcs
@author: Parker Lamb
@description: ASCOM frontend to help manage the UW MRO telescope
"""

from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget)
from widgets.target import TargetWidget

class TCS(QApplication):
    def __init__(self):
        """
        TCS application.
        """
        super().__init__()
        
    class Window(QMainWindow):
        def __init__(self):
            """
            Main window, holding all application elements.
            """
            super().__init__()

            # Application setup and backend
            self.version = 0.1
            self.title = "MRO-TCS v{}".format(self.version)
            self.resize(850,600)
            self.setWindowTitle(self.title)
        
            # Set up all the tabs
            tabs = QTabWidget()
            tabs.setDocumentMode(True)

            # Instantiate widgets
            targetwidget = TargetWidget()

            # Add new widgets for each page
            tabs.addTab(targetwidget, "Targets")

            self.setCentralWidget(tabs)


    def run(self):
        """
        Run the TCS application.
        """
        win = self.Window()

        win.show()
        self.exec()


if __name__ == "__main__":
    gui = TCS()
    gui.run()