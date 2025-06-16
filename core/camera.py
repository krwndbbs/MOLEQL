# File: camera.py

from core.object3D import Object3D
from core.matrix import Matrix
from numpy.linalg import inv

class Camera(Object3D):
    """ 
       Defines position and orientation of viewer and stores
       data describing visible region of scene, which is 
       encapsulated by projection matrix. Thus, this class
       stores both a view matrix and a projection matrix.
    """
    def __init__(self, angleOfView=60, aspectRatio=1, 
                 near=0.1, far=1000):

        super().__init__()

        self.projectionMatrix = Matrix.makePerspective(
                                angleOfView, aspectRatio, near, far)
        self.viewMatrix = Matrix.makeIdentity()

    def updateViewMatrix(self):
        self.viewMatrix = inv(self.getWorldMatrix())
        
    def setPerspective(self, angleOfView=50, aspectRatio=1, 
                             near=0.1, far=1000):

        self.projectionMatrix = Matrix.makePerspective(
                                angleOfView, aspectRatio, near, far)

    def setOrthographic(self, left=-1, right=1, bottom=-1, 
                              top=1, near=-1, far=1):

        self.projectionMatrix = Matrix.makeOrthographic(
                                left, right, bottom, top, near, far)

