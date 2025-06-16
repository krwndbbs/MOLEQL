# File: lineMaterial.py
"""
   An extension of the BasicMaterial class which renders
   vertices as lines.
"""

from material.basicMaterial import BasicMaterial
from OpenGL.GL import *

class LineMaterial(BasicMaterial):

    def __init__(self, properties={}):
        super().__init__()

        #
        # *Note*: 'self.settings' dict initiated 
        #         in Material class
        #

        # Render vertices as continuous line by default
        self.settings["drawStyle"] = GL_LINE_STRIP

        # Set the line thickness
        self.settings["lineWidth"] = 1

        # Possible line types: "connected" | "loop" | "segments"
        self.settings["lineType"] = "connected"

        self.setProperties(properties) # method from Material class

    def updateRenderSettings(self):
        """
           Method to call OpenGL functions needed to configure
           render setting previously specified.
        """
        glLineWidth(self.settings["lineWidth"])
        if self.settings["lineType"] == "connected":
            self.settings["drawStyle"] = GL_LINE_STRIP
        elif self.settings["lineType"] == "loop":
            self.settings["drawStyle"] = GL_LINE_LOOP
        elif self.settings["lineType"] == "segments":
            self.settings["drawStyle"] = GL_LINES
        else:
            raise Exception("Unknown LineMaterial draw style")

