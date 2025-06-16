# File: newCanvas.py
"""
   Create a blank OpenGL window:
"""
# Import any needed standard library
import sys

# Import any needed third party library
from OpenGL.GL import *

# Import any needed local library
from core.glBase     import GLBase

class NewCanvas(GLBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def initializeGL(self):
        super().initializeGL()

        # Set a grey background color.
        glClearColor(0.5, 0.5, 0.5, 1.0)

    def paintGL(self):
        super().paintGL()

        # Clear contents of color and depth buffers.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

