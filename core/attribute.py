# File: attribute.py
"""
   Manage attribute data by:
    • storing array of data in a vertex buffer
    • associating vertex buffer to a shader variable 
        in a given program
"""
from OpenGL.GL import *
import numpy as np

class Attribute(object):

    def __init__(self, dataType, data):
        # Type of elements in data array:
        #    int | float | vec2 | vec3 | vec4
        self.dataType = dataType

        # Array of data to be stored in buffer
        self.data = data

        # Reference of available buffer from GPU
        self.bufferRef = glGenBuffers(1) # return 1 buffer reference

        # Upload data immediately
        self.uploadData()

    def uploadData(self):
        """ 
           Upload data to a GPU buffer.
        """
        # Convert data to numpy array format ... convert 
        #   numbers to 32-bit floats
        data = np.array(self.data).astype(np.float32)

        # Select buffer used by following functions
        #   • GL_ARRAY_BUFFER == for vertex attributes
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef)

        # Store data in currently bound buffer
        #   • GL_STATIC_DRAW == buffer contents modified once
        #   • data.ravel() == a numpy function to return a 
        #                     contiguous flattened array
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)

    def associateVariable(self, programRef, variableName):
        """
           Associate variable in program with this buffer.
        """
        # Get reference for program variable with given name
        variableRef = glGetAttribLocation(programRef, variableName)

        # Exit if program does not reference variable
        if(variableRef == -1):
            return

        # Select buffer used by following functions
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef)

        # Specify how data will be read from currently bound
        #   buffer into specified variable
        if(self.dataType == "int"):
            glVertexAttribPointer(variableRef, 1, GL_INT, False, 0, None)
        elif(self.dataType == "float"):
            glVertexAttribPointer(variableRef, 1, GL_FLOAT, False, 0, None)
        elif(self.dataType == "vec2"):
            glVertexAttribPointer(variableRef, 2, GL_FLOAT, False, 0, None)
        elif(self.dataType == "vec3"):
            glVertexAttribPointer(variableRef, 3, GL_FLOAT, False, 0, None)
        elif(self.dataType == "vec4"):
            glVertexAttribPointer(variableRef, 4, GL_FLOAT, False, 0, None)
        else:
            raise Exception(" Attribute " + variableName + 
                            " has unknown type " + self.dataType)

        # Indicate that data will be streamed to this variable
        glEnableVertexAttribArray(variableRef)

