# File: surfaceMaterial.py
"""
   An extension of the BasicMaterial class which renders
   vertices as a surface.
"""

from material.basicMaterial import BasicMaterial
from OpenGL.GL import *

class SurfaceMaterial(BasicMaterial):

    def __init__(self, properties={}):
        super().__init__()

        #
        # *Note*: 'self.settings' dict initiated 
        #         in Material class
        #

        # Render vertices as surface
        self.settings["drawStyle"] = GL_TRIANGLES

        #
        # Render both sides? 
        #   default: front side only for rendering efficiency
        #   (vertices ordered counterclockwise)
        #
        self.settings["doubleSide"] = False

        # Render triangles as wireframe?
        self.settings["wireframe"] = False

        #
        # Set line thickness for wireframe rendering
        # *Note*: line width can ONLY be 1 with this
        #         version of OpenGL
        #
        self.settings["lineWidth"] = 1

        self.setProperties(properties) # method from Material class

    def updateRenderSettings(self):
        """
           Method to call OpenGL functions needed to configure
           render setting previously specified.
        """
        if self.settings["doubleSide"]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)

        if self.settings["wireframe"]:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glLineWidth(self.settings["lineWidth"])
