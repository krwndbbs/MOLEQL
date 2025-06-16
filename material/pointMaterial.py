# File: pointMaterial.py
"""
   An extension of the BasicMaterial class which renders
   vertices as points.
"""

from material.basicMaterial import BasicMaterial
from OpenGL.GL import *

class PointMaterial(BasicMaterial):

    def __init__(self, properties={}):
        super().__init__()

        #
        # *Note*: 'self.settings' dict initiated 
        #         in Material class
        #

        # Render vertices as points
        self.settings["drawStyle"] = GL_POINTS  

        # Width & height of points in pixels
        self.settings["pointSize"] = 8

        # Draw points as rounded
        self.settings["roundedPoints"] = False

        self.setProperties(properties) # method from Material class

    def updateRenderSettings(self):
        """
           Method to call OpenGL functions needed to configure
           render setting previously specified.
        """
        glPointSize(self.settings["pointSize"])

        ###
        ### 'roundedPoints' not supported in 
        ###   version of OpenGL
        ###
        #if self.settings["roundedPoints"]:
        #    glEnable(GL_POINT_SMOOTH)
        #else:
        #    glDisable(GL_POINT_SMOOTH)
        ###

