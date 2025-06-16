# File: polygonGeometry.py

"""
   A regular polygon is a 2D shape such that all sides have same 
   length and all angles have same value. The coordinates of the
   vertices are calculated by using equally spaced points on the
   circumference of a circle with radius R, using parametric 
   equations: x = R*cos(t), y = R*sin(t). Angle "t" will be 
   multiples of base angle A which is equal to 2pi divided by the
   number of sides of the polygon.
"""
from geometry.geometry import Geometry
from math import cos, sin, pi

class PolygonGeometry(Geometry):

    def __init__(self, sides=3, radius=1, color=None):
        """
           The vertices of a regular polygon are grouped into
           triangles where each triangle has one vertex at the
           origin (center of polygon) and 2 adjacent vertices
           on circumference of polygon, ordered counterclockwise.
        """
        super().__init__()

        A = 2*pi/sides
        positionData = []
        colorData = []

        # For normal vectors
        normalData = []
        normalVector = [0, 0, 1]

        #
        # Use for-loop to step through calculation of each triangle
        #   making up n-sided polygon.
        #
        for n in range(sides):
            positionData.append( [0, 0, 0] )
            positionData.append( [radius*cos(n*A), radius*sin(n*A), 0] )
            positionData.append( [radius*cos((n+1)*A), radius*sin((n+1)*A), 0] )
            if color == None:
                colorData.append( [1, 1, 1] )
                colorData.append( [1, 0, 0] )
                colorData.append( [0, 0, 1] )
            else:
                colorData += [color]*3

            normalData.append( normalVector.copy() )
            normalData.append( normalVector.copy() )
            normalData.append( normalVector.copy() )

        # Add attributes and count vertices
        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
        self.addAttribute("vec3", "vertexNormal", normalData)
        self.addAttribute("vec3", "faceNormal", normalData)
        self.countVertices()

