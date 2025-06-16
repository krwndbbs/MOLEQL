# File: hemisphereGeometry.py

"""
   A hemisphere is a specific 3D surface of an ellipsoid.
"""
from geometry.parametricGeometry import ParametricGeometry
from math import sin, cos, pi

class HemisphereGeometry(ParametricGeometry):

    def __init__(self, radius=1, position=[0,0,0], end=None, 
                       radiusSegments=32, heightSegments=32, color=None):

        x, y, z = position
        Start, End = 0, pi/2
        if end == "top":
            Start, End = 0, pi/2
        if end == "bottom":
            Start, End = -pi/2, 0

        # Parametric function
        def S(u, v):
            return [ x + radius * sin(u) * cos(v),
                     y + radius * sin(v),
                     z + radius * cos(u) * cos(v) ]

        super().__init__( 0, 2*pi, radiusSegments, 
                          Start, End, heightSegments,
                          S, color, color )

