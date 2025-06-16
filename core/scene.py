# File: scene.py

from core.object3D import Object3D

class Scene(Object3D):
    """ 
       Represents the root node in the scene graph and
       does not correspond to visible objects in scene.
    """
    def __init__(self):
        super().__init__()
        
