# File: object3D.py

from core.matrix import Matrix
import numpy as np

class Object3D(object):
    """ 
       Represent a node in scene graph tree structure that contains:
        • a list of references to child objects 
          & parent object
        • "add" & "remove" functions to update parent & child references
        • "getWorldMatrix function to calculate world transformation
           from stored transform data (as a numpy matrix object)
        • "getDescendantList" function collects all nodes in tree into a
          list to iterate over when rendering the scene
        • a set of functions for translating, rotating, & scaling an object
        • a set of functions to get & set position of an object
    """
    def __init__(self):
        self.transform = Matrix.makeIdentity() # Initialize transform matrix
        self.parent = None
        self.children = []

    def add(self, child):
        self.children.append(child)
        child.parent = self

    def remove(self, child):
        self.children.remove(child)
        child.parent = None

    def getWorldMatrix(self):
        """
           Calculate transformation of this Object3D relative
           to the root Object3D of scene graph.
        """
        if self.parent == None:
            return self.transform
        else:
            return self.parent.getWorldMatrix() @ self.transform

    def getDescendantList(self):
        """
           Return a single list containing all descendants.
        """
        # Master list of all descendant nodes
        descendants = []

        #
        # Nodes to be added to descendant list, and
        #   whose children will be added to this list
        #
        nodesToProcess = [self]

        # Continue processing nodes while any are left
        while( len(nodesToProcess) > 0 ):
            # Remove first node from list
            node = nodesToProcess.pop(0)
            # Add this node to descendant list
            descendants.append(node)
            # This node's children must also be processed
            nodesToProcess = node.children + nodesToProcess

        return descendants

    #
    # Apply geometric transformations
    #
    def applyMatrix(self, matrix, localCoord=True):
        """ Choose either local or global transformation """
        if localCoord:
            self.transform = self.transform @ matrix
        else:
            self.transform = matrix @ self.transform

    def translate(self, x, y, z, localCoord=True):
        m = Matrix.makeTranslation(x, y, z)
        self.applyMatrix(m, localCoord)

    def rotateX(self, angle, localCoord=True):
        m = Matrix.makeRotationX(angle)
        self.applyMatrix(m, localCoord)

    def rotateY(self, angle, localCoord=True):
        m = Matrix.makeRotationY(angle)
        self.applyMatrix(m, localCoord)

    def rotateZ(self, angle, localCoord=True):
        m = Matrix.makeRotationZ(angle)
        self.applyMatrix(m, localCoord)

    def scale(self, s, localCoord=True):
        m = Matrix.makeScale(s)
        self.applyMatrix(m, localCoord)

    #
    # Get/set position components of transform
    #
    def getPosition(self):
        return [ self.transform.item( (0, 3) ),   # item is numpy function
                 self.transform.item( (1, 3) ),
                 self.transform.item( (2, 3) ) ]

    def getWorldPosition(self):
        worldTransform = self.getWorldMatrix()
        return [ worldTransform.item( (0, 3) ),
                 worldTransform.item( (1, 3) ),
                 worldTransform.item( (2, 3) ) ]

    def setPosition(self, position):
            self.transform.itemset( (0, 3), position[0] )
            self.transform.itemset( (1, 3), position[1] )
            self.transform.itemset( (2, 3), position[2] )

    #
    # Apply look-at matrix to object, retaining object's position
    #   while replacing its orientation so that object faces target.
    #
    def lookAt(self, targetPosition):
        self.transform = Matrix.makeLookAt( self.getWorldPosition(), targetPosition )

    #
    # The following 3 functions enables getting and setting
    #   direction an object is facing (forward direction)
    #   which is defined by orientation of its local 
    #   negative z-axis.
    #
    def getRotationMatrix(self):
        """ Returns 3x3 submatrix with rotation data. """
        return np.array( [ self.transform[0][0:3],
                           self.transform[1][0:3],
                           self.transform[2][0:3] ] )

    def getDirection(self):
        forward = np.array([0,0,-1])
        return list( self.getRotationMatrix() @ forward )

    def setDirection(self, direction):
        position = self.getPosition()
        targetPosition = [ position[0] + direction[0],
                           position[1] + direction[1],
                           position[2] + direction[2] ]
        self.lookAt( targetPosition )

