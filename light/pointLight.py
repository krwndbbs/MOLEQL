# File: pointLight.py

from light.light import Light

class PointLight(Light):
    """
       Point light simulates rays of light being emitted from a 
       single point in all directions (like a light bulb) and 
       incorporates attenuation --> a decrease in intensity as
       the distance between the light source and the surface
       increases.
    """
    def __init__(self, color=[1,1,1], position=[0,0,0], 
                       attenuation=[1, 0, 0.1]):

        super().__init__(Light.POINT)
        self.color = color
        self.setPosition( position )
        self.attenuation = attenuation

