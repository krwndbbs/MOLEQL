#File: GLBase.py
"""
   Modified version of EagleEatApple base.py   
"""
# Import standard library
import sys
import time

# Import third party libraries
from PySide6.QtWidgets import QApplication
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtCore import QTimer
from OpenGL.GL import *

# Import local library
from core.input import Input

class GLBase(QOpenGLWidget):
    """
       QOpenGLWidget provides functionality for displaying OpenGL 
       graphics integrated into a Qt application. QOpenGLWidget
       ultimately inherits from QtWidgets.QWidget which is evident
       in the methods below.
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.timer = QTimer(self)
        # When timer times out, emit signal to update() method of QWidget
        self.timer.timeout.connect(self.update)
        # Start (or restart) timer with a timeout interval of 20 milliseconds
        self.timer.start(20)
        self.time = 0
        self.input = Input()

    def initializeGL(self):
        """
           A virtual function (QOpenGLWidget) which sets up any 
           required OpenGL resources. It is called once before 
           the first call to resizeGL() or paintGL(). It initializes 
           different OpenGL buffers and variables which will be 
           used later during rendering.
        """
        # Initialize self.last_time to current time, time.time()
        self.last_time = time.time()

    def paintGL(self):
        """
           This virtual function (QOpenGLWidget) is called whenever 
           the widget needs to be painted. This method is called by 
           resize events and by update/updateGL methods.
        """
        self.deltaTime = time.time() - self.last_time
        self.time += self.deltaTime
        self.last_time = time.time()
        self.input.update()

    def keyPressEvent(self, event):
        """
           This virtual function (QWidget) is a handler for receiving a
           key press "event" for this widget.
        """
        self.input.receiveKeyEvent(event.key(), event.type())
        self.update()

    def keyReleaseEvent(self, event):
        """
           This virtual function (QWidget) is a handler for receiving a
           key release "event" for this widget.
        """
        self.input.receiveKeyEvent(event.key(), event.type())
        self.update() 

