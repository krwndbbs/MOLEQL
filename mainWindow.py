#File: mainwindow.py
"""
   Establish a window for OpenGL drawing:
    • set window size and title
    • create and display menu bar
    • open coordinate file; read and process coordinate data
    • determine which structure model to display and then
      update the window
"""
# Import needed standard libraries
import sys
import numpy as np

# Import needed local libraries
from stickModel      import StickModel
from cpkModel        import CpkModel  
from ballStickModel  import BallStickModel
from newCanvas       import NewCanvas
from processMolecule import processMolecule

# Need following for molecular objects
import Atom
import Molecule
import Elements

# Import needed third party libraries
from PySide6.QtWidgets import (QApplication, QMainWindow, QFileDialog,
                               QMessageBox, QStatusBar, QLabel)
from PySide6.QtGui import QAction, QSurfaceFormat

class MainWindow(QMainWindow):
    """
       The QMainWindow class provides the functionalities for building a
       main window's key features, such as a menu bar, a toolbar, or dock
       widgets in predefined locations.
    """
    def __init__(self, screenSize=[512, 512], title=""):
        super().__init__()

        self.molecule = None   # initialize molecule object

        self.label = QLabel()  # Use to display mouse tracking

        # Set the title and size of window
        self.setWindowTitle("Moleql")
        self.setFixedSize(screenSize[0], screenSize[1])

        self.setCentralWidget(NewCanvas(self))
        self.createActions()
        self.createMenu()

    def createActions(self):
        """ 
           Create application's menu actions.
        """
        # File menu actions
        self.new_act = QAction("New Canvas")
        self.new_act.setShortcut("Ctrl+N")
        #
        # Remember, lambda function is used to delay invocation of action
        #   (in this case, passing an argument to a method) until action 
        #   is actually triggered, i.e., upon selection of this menu item.
        #
        self.new_act.triggered.connect(lambda: self.selectModel("blank"))

        self.open_act = QAction("Open")
        self.open_act.setShortcut("Ctrl+O")
        # lambda function not needed here since no argument is passed
        self.open_act.triggered.connect(self.openFile) # see method below

        self.quit_act = QAction("Quit")
        self.quit_act.setShortcut("Ctrl+Q")
        self.quit_act.triggered.connect(self.close) # self.close => QWidget slot

        # View menu actions
        self.stickmodel_act = QAction("Stick model")
        self.stickmodel_act.triggered.connect(lambda: self.selectModel("stick"))

        self.ballstickmodel_act = QAction("Ball-and-Stick model")
        self.ballstickmodel_act.triggered.connect(lambda: self.selectModel("ball-and-stick"))

        self.cpkmodel_act = QAction("Space-filling model")
        self.cpkmodel_act.triggered.connect(lambda: self.selectModel("cpk"))

    def createMenu(self):
        """
           Create application's menu bar.
        """
        self.menuBar().setNativeMenuBar(False)

        # Create File menu and add actions
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(self.new_act)
        file_menu.addSeparator()
        file_menu.addAction(self.open_act)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_act)

        # Create View menu and add actions
        view_menu = self.menuBar().addMenu("View")
        view_menu.addAction(self.stickmodel_act)
        view_menu.addAction(self.ballstickmodel_act)
        view_menu.addAction(self.cpkmodel_act)

        # Create status bar
        self.status_bar = QStatusBar()         
        self.label.setText('')
        self.status_bar.addWidget(self.label)
        self.setStatusBar(self.status_bar)

    def openFile(self):
        """
           Show dialog window to choose file with coordinates.
        """
        coord_file, _ = QFileDialog.getOpenFileName(
                            self, "Open File", "", 
                            "Unichem Files (*.xyz);;Python Files (*.py)")

        #
        # Create a molecule object; read in xyz coords (in Angstroms).
        #
        if coord_file:
            self.molecule = Molecule.Molecule()  # create molecule instance
            with open(coord_file, "r") as f:
                contents = f.readlines()
                title = contents[0]              # molecule title
                natoms = int(contents[1])        # number of atoms
                for i in range(2, natoms+2):
                    data = contents[i].split()   # each line contains:
                    atnum = int(data[0])         #  • atomic number
                    x = float(data[1])           #  • x coord
                    y = float(data[2])           #  • y coord
                    z = float(data[3])           #  • z coord
                    # Add newly created atom object to molecule object
                    self.molecule.addAtom(Atom.Atom(atnum, x, y, z))
        else:
            QMessageBox.information(self, "No File", "No File Selected.", 
                                    QMessageBox.StandardButton.Ok)

        #
        # Process atomic coordinates to form molecule:
        #  • determine which atoms are bonded to each other
        #  • center atomic coordinates
        #
        if self.molecule:
            self.setWindowTitle("Moleql – " + title) # reset window title
            processMolecule(self, self.molecule)

    def selectModel(self, model):
        """
           Determine which structure model has been selected.
        """
        # Check to see if molecule object exists
        if (self.molecule == None) or (self.molecule.atomCount == 0):
            QMessageBox.warning(self, "No molecule!", "Need coordinates.",
                                QMessageBox.StandardButton.Close,
                                QMessageBox.StandardButton.Close)
        # Otherwise, continue processing selection
        elif model == "blank":
            self.molecule.clear() # make molecular info disappear
            # Hide label widget to stop showing mouse tracking
            self.status_bar.removeWidget(self.label)
            self.setCentralWidget(NewCanvas(self)) # create a blank canvas
        elif model == "stick":
            self.status_bar.removeWidget(self.label)
            self.setCentralWidget(StickModel(self, self.molecule, self.label))
        elif model == "cpk":
            self.status_bar.removeWidget(self.label)
            self.setCentralWidget(CpkModel(self, self.molecule, self.label))
        elif model == "ball-and-stick":
            self.status_bar.removeWidget(self.label)
            self.setCentralWidget(BallStickModel(self, self.molecule, self.label))
        # Now, update with new model
        self.update()

class baseApp(QApplication):
    """
       QApplication is responsible for managing the application's 
       main event loop, widget initialization, widget finalization, 
       command line argument parsing, and event handling such as 
       key presses and mouse cursor handling.
    """
    def __init__(self, argv):
        """
           Configure renderable surfaces using the QSurfaceFormat class,
           a way of enabling OpengGL features.
        """
        super().__init__(argv)
        self.format = QSurfaceFormat()
        self.format.setDepthBufferSize(24)                 # set minimum buffer depth
        self.format.setStencilBufferSize(8)                # set stencil buffer depth
        # Setting number of samples per pixel used in anti-aliasing
        #   automatically enables multisampling.
        self.format.setSamples(4) 
        self.format.setVersion(3, 2)                       # set major and minor OpenGL versions
        self.format.setProfile(QSurfaceFormat.CoreProfile) # set OpenGl context profile
        QSurfaceFormat.setDefaultFormat(self.format)


def main():
    app = baseApp(sys.argv)
    window = MainWindow([800, 800])
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
