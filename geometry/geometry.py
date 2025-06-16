# File: geometry.py
"""
   Geometry object will store attribute data and total 
   number of vertices.
"""
from core.attribute import Attribute
import numpy as np

class Geometry(object):

    def __init__(self):
        """
           Define a dictionary to store Attribute objects, indexed
           by name of associated variable in shader. Shader variable
           associations set up later and stored in vertex array
           object in Mesh.
        """
        self.attributes = {}

        # Number of vertices
        self.vertexCount = None

    def addAttribute(self, dataType, variableName, data):
        self.attributes[variableName] = Attribute(dataType, data)

    def countVertices(self):
        """
           Number vertices may be calculated from length of any
           Attribute object's array of data.
        """
        attrib = list( self.attributes.values() )[0]
        self.vertexCount = len(attrib.data)

    def applyMatrixLine(self, matrix, variableName="vertexPosition"):
        """ 
           Transform data in an attribute using a matrix.
        """ 
        oldPositionData = self.attributes[variableName].data
        newPositionData = []

        for oldPos in oldPositionData:
            newPos = oldPos.copy()         # avoid changing list reference
            newPos.append(1)               # add homogeneous 4th coordinate
            newPos = matrix @ newPos       # multiply by matrix
            newPos = list( newPos[0:3] )   # remove homogeneous coord
            newPositionData.append(newPos) # add to new data list

        self.attributes[variableName].data = newPositionData

        # New data must be uploaded
        self.attributes[variableName].uploadData()

    def applyMatrix(self, matrix, variableName="vertexPosition"):
        """ 
           Transform data in an attribute using a matrix.
        """ 
        oldPositionData = self.attributes[variableName].data
        newPositionData = []

        for oldPos in oldPositionData:
            newPos = oldPos.copy()         # avoid changing list reference
            newPos.append(1)               # add homogeneous 4th coordinate
            newPos = matrix @ newPos       # multiply by matrix
            newPos = list( newPos[0:3] )   # remove homogeneous coord
            newPositionData.append(newPos) # add to new data list

        self.attributes[variableName].data = newPositionData

        # Extract the rotation submatrix
        rotationMatrix = np.array( [ matrix[0][0:3],
                                     matrix[1][0:3],
                                     matrix[2][0:3] ] )

        # Update normal vector data upon transforming a geometry
        oldVertexNormalData = self.attributes["vertexNormal"].data
        newVertexNormalData = []
        for oldNormal in oldVertexNormalData:
            newNormal = oldNormal.copy()
            newNormal = rotationMatrix @ newNormal
            newVertexNormalData.append( newNormal )
        self.attributes["vertexNormal"].data = newVertexNormalData

        oldFaceNormalData = self.attributes["faceNormal"].data
        newFaceNormalData = []
        for oldNormal in oldFaceNormalData:
            newNormal = oldNormal.copy()
            newNormal = rotationMatrix @ newNormal
            newFaceNormalData.append( newNormal )
        self.attributes["faceNormal"].data = newFaceNormalData

        # New data must be uploaded
        self.attributes[variableName].uploadData()
        self.attributes["vertexNormal"].uploadData()
        self.attributes["faceNormal"].uploadData()

    def merge(self, otherGeometry):
        """
           Merge data from attributes of other geometry into this
           object, which requires both geometries to have 
           attributes with same names.
        """
        for variableName, attributeObject in self.attributes.items():
            attributeObject.data.extend(otherGeometry.attributes[variableName].data)
            attributeObject.uploadData() # new data must be uploaded

        # Update number of vertices
        self.countVertices()

