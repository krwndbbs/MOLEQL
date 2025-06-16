# File: light.py
"""
   Light is treated as a 3D object to be added to a scene.
"""
from core.object3D import Object3D

class Light(Object3D):
    """
       A base class to store data that could be needed
       by any type of light, including a constant that
       specifies the type of light (ambient, directional,
       or point).
    """
    AMBIENT     = 1
    DIRECTIONAL = 2
    POINT       = 3

    def __init__(self, lightType=0):

        super().__init__()
        self.lightType   = lightType
        self.color       = [1, 1, 1]
        self.attenuation = [1, 0, 0]

