# File: drawLine.py

from core.mesh             import Mesh
from geometry.geometry     import Geometry
from material.lineMaterial import LineMaterial

class DrawLine(Geometry):
    """
       Draw a colored line from point1 to point2:
         point1 = [x1, y1, z1]
         point2 = [x2, y2, z2]
    """
    # Note: lineWidth can ONLY be 1
    def __init__(self, point1, point2, lineColor=[1,0,0], lineWidth=1):

        super().__init__()

        positionData = [ point1, point2 ]

        colorData = [ lineColor, lineColor ]

        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
        self.countVertices()

