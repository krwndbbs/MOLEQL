# File: material.py
"""
   Material objects store 3 type of data related to rendering:
     • shader program references
     • Uniform objects
     • OpenGL render settings
"""

from core.openGLUtils import OpenGLUtils
from core.uniform import Uniform
from OpenGL.GL import *

class Material(object):

    def __init__(self, vertexShaderCode, fragmentShaderCode):

        self.programRef = OpenGLUtils.initializeProgram(vertexShaderCode, 
                                                        fragmentShaderCode)

        #
        # Store Uniform objects in a dictionary, indexed 
        #   by name of associated variable in shader. 
        #   Initialize dictionary with 3 uniforms which
        #   are typically contained in each shader. Values
        #   will be set during render process from Mesh/Camera.
        #
        self.uniforms = { 
            "modelMatrix":      Uniform("mat4", None),
            "viewMatrix":       Uniform("mat4", None),
            "projectionMatrix": Uniform("mat4", None), }

        #
        # Store OpenGL render settings in a dictionary, 
        #   indexed by variable name. Initialize dictionary
        #   with draw style. Additional settings added
        #   by extending classes.
        #
        self.settings = { "drawStyle": GL_TRIANGLES }

    def addUniform(self, dataType, variableName, data):
        """ 
            A method to simplify creating and 
            adding Uniform objects.
        """
        self.uniforms[variableName] = Uniform(dataType, data)

    def locateUniforms(self):
        """
           Initialize all uniform variable references. Determine and
           store all uniform variable references in the shaders.
        """
        for variableName, uniformObject in self.uniforms.items():
            uniformObject.locateVariable(self.programRef, variableName)

    def updateRenderSettings(self):
        """
           Virtual function to configure OpenGL with render settings.
        """
        pass

    def setProperties(self, properties):
        """ 
           Convenience method for setting muliple material
           "properties" (uniform & render setting values)
           from a dictionary.
        """ 
        for name, data in properties.items():
            # update uniforms
            if name in self.uniforms.keys():   
                self.uniforms[name].data = data
            # update render settings
            elif name in self.settings.keys(): 
                self.settings[name] = data
            # unknown property type
            else:
                raise Exception("Material has no property name: " + name)

