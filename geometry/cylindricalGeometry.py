# File: cylindricalGeometry.py

"""
   A general cylindrical surface may be used to create a regular 
   cylinder, different prism shapes, a regular cone, and different 
   pyramid shapes. The cylindrical surface is centered at the 
   origin with circular, or approximately circular, cross-sections 
   of radius R which may vary along the y-axis. 
"""
from geometry.parametricGeometry import ParametricGeometry
from geometry.polygonGeometry import PolygonGeometry
from core.matrix import Matrix
from math import sin, cos, pi

class CylindricalGeometry(ParametricGeometry):

    def __init__(self, radiusTop=1, radiusBottom=1, height=1, 
                       radialSegments=32, heightSegments=4,
                       closedTop=True, closedBottom=True,
                       color1=None, color2=None):

        # Parametric function
        def S(u, v):
            return [ (v*radiusTop+(1-v)*radiusBottom)*sin(u), 
                     height*(v-0.5),
                     (v*radiusTop+(1-v)*radiusBottom)*cos(u) ]

        super().__init__( 0, 2*pi, radialSegments,
                          0, 1, heightSegments, 
                          S, color1, color2 )

        #
        # Handle case(s) in which the top and/or bottom
        #   of the cylindrical surface is/are closed
        #
        if closedTop:
            # create a polygonal instance for top enclosure
            topGeometry = PolygonGeometry(radialSegments, radiusTop, color2)
            transform = (Matrix.makeTranslation(0, height/2, 0) @
                        Matrix.makeRotationY(-pi/2) @
                        Matrix.makeRotationX(-pi/2))
            topGeometry.applyMatrix(transform)
            self.merge(topGeometry)

        if closedBottom:
            # create a polygonal instance for bottom enclosure
            bottomGeometry = PolygonGeometry(radialSegments, radiusBottom, color1)
            transform = (Matrix.makeTranslation(0, -height/2, 0) @
                        Matrix.makeRotationY(-pi/2) @
                        Matrix.makeRotationX(pi/2))
            bottomGeometry.applyMatrix(transform)
            self.merge(bottomGeometry)
        
