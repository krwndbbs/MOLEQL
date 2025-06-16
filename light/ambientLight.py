# File: ambientLight.py

from light.light import Light

class AmbientLight(Light):
    """
       Ambient lighting affects all points on all geometric
       surfaces in a scene by the same amount. This lighting
       only uses the color data.
    """
    def __init__(self, color=[1,1,1]):

        super().__init__(Light.AMBIENT)
        self.color = color

