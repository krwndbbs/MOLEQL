# File: group.py

from core.object3D import Object3D

class Group(Object3D):
    """ 
       Represents an interior node to which other nodes
       are attached to more easily transform them as a 
       single unit. Also, this class does not correspond
       to visible objects in scene.
    """
    def __init__(self):
        super().__init__()
        
