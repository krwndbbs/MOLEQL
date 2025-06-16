# File: mesh.py

from core.object3D import Object3D
from OpenGL.GL import *

class Mesh(Object3D):
    """ 
       Represents visible objects in scene, containing geometric
       data that specifies vertex-related properties and material
       data that specifies general appearance of object. Since a
       vertex array object links data between these two components,
       this class is also a natural place to crate and store this
       reference and set up associations between vertex buffers 
       and shader variables.
    """
    def __init__(self, geometry, material):
        super().__init__()

        self.geometry = geometry
        self.material = material

        # Should this object be rendered?
        self.visible = True

        #
        # Set up associations between attributes stored in
        #   geometry and shader program stored in material
        #
        self.vaoRef = glGenVertexArrays(1)
        glBindVertexArray(self.vaoRef)
        for variableName, attributeObject in geometry.attributes.items():
            attributeObject.associateVariable(material.programRef, variableName)

        # Unbind this vertex array object
        glBindVertexArray(0)

