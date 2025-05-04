from PySide6.QtGui import QPalette
from PySide6.QtWidgets import (QComboBox, QFileDialog, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QGridLayout)
from matplotlib import (colors, pyplot)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

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
        layout.addLayout(tglayout, 0, 0, -1, -1) # Spanning 4 columns

        # Add form layouts
        top_name_layout = QFormLayout()
        mid_dec_layout = QFormLayout()
        mid_alt_layout = QFormLayout()
        bot_epoch_layout = QFormLayout()
        tglayout.addLayout(top_name_layout, 0, 0, 1, 2)
        tglayout.addLayout(mid_dec_layout, 1, 0, 2, 1)
        tglayout.addLayout(mid_alt_layout, 1, 1, 2, 1)
        tglayout.addLayout(bot_epoch_layout, 3, 0, 1, -1)

        # Create params
        self.targetName = QLineEdit()
        self.targetRA = QLineEdit()
        self.targetDec = QLineEdit()
        self.targetAlt = QLineEdit().setEnabled(False) # TBD
        self.targetAz = QLineEdit().setEnabled(False) # TBD
        self.targetEpoch = QLineEdit()
        self.targetEpoch.setText("J2000")
    
        # Add params to layout
        top_name_layout.insertRow(0, "Name", self.targetName)
        mid_dec_layout.insertRow(0, "RA", self.targetName)
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

class TargetWidget(QWidget):
    def __init__(self):
        """
        Container widget used when the "Target" tab is selected.
        """
        super().__init__()

        # Grand layout
        layout = QHBoxLayout(self)

        # Set up target variables
        self.current_tgt = {} # Name, RA, Dec, Alt, Az, Epoch
        self.all_tgts = []

        # Target specification box
        targetBox = CurrentTarget()
        layout.addWidget(targetBox)