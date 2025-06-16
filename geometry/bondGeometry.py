# File: bondGeometry.py

"""
   A bond is a specific case of a cylindrical surface in
   which the top and bottom have the same radius, both 
   the top and bottom are closed, and half the surface is
   one color while the other half may be of a different
   color.
"""
from geometry.parametricGeometry import ParametricGeometry
from geometry.hemisphereGeometry import HemisphereGeometry
from core.matrix import Matrix
from math import sin, cos, pi

class BondGeometry(ParametricGeometry):

    def __init__(self, radius=1, height=1, radialSegments=32, 
                 heightSegments=4, color1=[0.5,0.5,1.0], 
                 color2=[1.0,0.5,0.5]):

        # Parametric function
        def S(u, v):
            return [ (v*radius+(1-v)*radius)*sin(u), 
                     height*(v-0.5),
                     (v*radius+(1-v)*radius)*cos(u) ]

        super().__init__( 0, 2*pi, radialSegments, 
                          0, 1, heightSegments, 
                          S, color1, color2 )

        #
        # Put rounded cap on top of bond
        #
        heightSlices = 4
        topGeometry = HemisphereGeometry(radius, [0,height/2,0], "top", 
                                         radialSegments, heightSlices, color2)
        self.merge(topGeometry)
        #
        # Put rounded cap on bottom of bond
        #
        bottomGeometry = HemisphereGeometry(radius, [0,-height/2,0], "bottom",
                                            radialSegments, heightSlices, color1)
        self.merge(bottomGeometry)

