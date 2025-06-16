# File: directionalLight.py

from light.light import Light

class DirectionalLight(Light):
    """
       Directional lighting simulates a distant light source
       such as the sun, in wich all the light rays are
       oriented along the same direction without attenuation.
    """
    def __init__(self, color=[1,1,1], direction=[0,-1,0]):

        super().__init__(Light.DIRECTIONAL)
        self.color = color
        self.setDirection( direction )

