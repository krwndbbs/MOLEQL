# File: parametricGeometry.py
"""
   Use a parametric function to transform a 2D rectangular 
   region into a 3D surface, e.g., a sphere or cylinder.
   The parametric function, S, generally expresses x, y, & z
   coordinates in terms of 2 independent variable u and v:

       (x, y, z) = ( f(u,v), g(u,v), h(u,v) ) = S(u,v)

   where the rectangular domain is usually,

          0 <= u <= 1  and  0 <= v <= 1

"""
from geometry.geometry import Geometry
import numpy as np

class ParametricGeometry(Geometry):

    def __init__(self, uStart, uEnd, uResolution,
                       vStart, vEnd, vResolution, 
                       surfaceFunction, color1, color2):
        """
           uStart, uEnd == bounds for u
           vStart, vEnd == bounds for v
           uResolution == number of samples used between u values
           vResolution == number of samples used between v values
           surfaceFunction == parametric function, S(u,v)
           color1 == color, [r,g,b], of 1st half of surface
           color2 == color, [r,g,b], of 2nd half of surface
        """
        super().__init__()

        # Calculate space between u and v coordinates
        deltaU = (uEnd - uStart) / uResolution
        deltaV = (vEnd - vStart) / vResolution

        #
        # Calculate half the samples between v values. Use of 
        #   this variable leads to a departure from the original
        #   code, allowing half the vertices to be one color
        #   and the other half to possibly be a different color.
        #
        vHalfResolution = vResolution/2

        #
        # Generate set of points on surface function and 
        #   store in 2D array, positions.
        #
        positions = []
        for uIndex in range(uResolution+1):
            vArray = []
            for vIndex in range(vResolution+1):
                u = uStart + uIndex * deltaU
                v = vStart + vIndex * deltaV
                vArray.append( surfaceFunction(u,v) )
            positions.append(vArray)

        # Calculate normal vector from 3 points
        def calcNormal(P0, P1, P2):
            v1 = np.array(P1) - np.array(P0)
            v2 = np.array(P2) - np.array(P0)
            orthogonal_vector = np.cross(v1, v2)
            norm = np.linalg.norm(orthogonal_vector)
            normal_vector = orthogonal_vector / norm if norm > 1e-6 \
                else np.array(P0) / np.linalg.norm(P0)
            return normal_vector

        #
        # Populate list with vertex normal vectors
        #   at position of each vertex.
        #
        vertexNormals = []
        for uIndex in range(uResolution+1):
            vArray = []
            for vIndex in range(vResolution+1):
                u = uStart + uIndex * deltaU
                v = vStart + vIndex * deltaV
                h = 0.0001
                P0 = surfaceFunction(u, v)
                P1 = surfaceFunction(u+h, v)
                P2 = surfaceFunction(u, v+h)
                normalVector = calcNormal(P0, P1, P2)
                vArray.append( normalVector )
            vertexNormals.append(vArray)

        # Store vertex data
        positionData = []
        colorData = []

        # Default vertex colors
        C1, C2, C3 = [1, 0, 0], [0, 1, 0], [0, 0, 1]
        C4, C5, C6 = [0, 1, 1], [1, 0, 1], [1, 1, 0]

        vertexNormalData = []
        faceNormalData = []

        #
        # Group vertex data into triangles
        #   Note: [].copy() needed to avoid storing references.
        #
        for xIndex in range(uResolution):
            for yIndex in range(vResolution):
                # position data for rectangle vertices
                pA = positions[xIndex+0][yIndex+0]
                pB = positions[xIndex+1][yIndex+0]
                pD = positions[xIndex+0][yIndex+1]
                pC = positions[xIndex+1][yIndex+1]
                # rectangle as 2 triangles
                positionData += [pA.copy(), pB.copy(), pC.copy(),
                                 pA.copy(), pC.copy(), pD.copy()]
                # color for vertices
                if color1 == None:
                    colorData += [C1,C2,C3, C4,C5,C6]
                else:
                    if yIndex < vHalfResolution:
                        colorData += [color1]*6
                    else:
                        colorData += [color2]*6
                # vertex normal vectors
                nA = vertexNormals[xIndex+0][yIndex+0]
                nB = vertexNormals[xIndex+1][yIndex+0]
                nD = vertexNormals[xIndex+0][yIndex+1]
                nC = vertexNormals[xIndex+1][yIndex+1]
                vertexNormalData += [nA,nB,nC, nA,nC,nD]
                # face normal vectors
                fn0 = calcNormal(pA, pB, pC)
                fn1 = calcNormal(pA, pC, pD)
                faceNormalData += [fn0,fn0,fn0, fn1,fn1,fn1]


        # Add attributes and count vertices
        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
        self.addAttribute("vec3", "vertexNormal", vertexNormalData)
        self.addAttribute("vec3", "faceNormal", faceNormalData)

        self.countVertices()

