# File: sphereGeometry.py

"""
   A sphere is a specific 3D surface of an ellipsoid.
"""
from geometry.ellipsoidGeometry import EllipsoidGeometry
from math import sin, cos, pi

class SphereGeometry(EllipsoidGeometry):

    def __init__(self, radius=1, radiusSegments=32, heightSegments=16,
                       color1=None, color2=None):

        super().__init__( 2*radius, 2*radius, 2*radius, 
                          radiusSegments, heightSegments,
                          color1, color2 )

