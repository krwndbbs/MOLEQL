# File: ellipsoidGeometry.py

"""
   An ellipsoid is generated from a parametric equation:

          S(u,v) = ( sin(u)*cos(v), sin(v), cos(u)*cos(v) )

   Assume a sphere centered at the origin with circular
   cross-sections of radius R which are analyzed along 
   the y-axis.
"""
from geometry.parametricGeometry import ParametricGeometry
from math import sin, cos, pi

class EllipsoidGeometry(ParametricGeometry):

    def __init__(self, width=1, height=1, depth=1, 
                       radiusSegments=32, heightSegments=16,
                       color1=None, color2=None):

        # Parametric function
        def S(u, v):
            return [  width/2 * sin(u) * cos(v),
                     height/2 * sin(v),
                      depth/2 * cos(u) * cos(v) ]

        super().__init__( 0, 2*pi, radiusSegments,
                          -pi/2, pi/2, heightSegments, 
                          S, color1, color2 )

