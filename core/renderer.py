# File: renderer.py
"""
   All code referencing both 'render target' and 
   'shadows' have been removed to simplify the class
   for use with PySide6. The original unaltered code
   may be found in:
   /Users/dobbskd/Python/OpenGLPython/DevGraFraWithPyAndOGL/core/
"""
from core.mesh import Mesh
from light.light import Light
from OpenGL.GL import *

class Renderer(object):
    """ 
       Perform general rendering tasks, including enabling depth
       testing, antialiasing, and setting the color used when 
       clearing the color buffer (the default background color).
    """
    def __init__(self, widget, clearColor=[0, 0, 0]):

        glEnable(GL_DEPTH_TEST)        # enable depth testing
        glEnable(GL_MULTISAMPLE)       # required for antialiasing
        glClearColor(clearColor[0], 
                     clearColor[1], 
                     clearColor[2], 1) # background color

        # Get the window dimensions
        self.widget = widget
        self.windowSize = widget.size().toTuple()

    def render(self, scene, camera, clearColor=True, clearDepth=True):

        # Clear color and/or depth buffers?
        if clearColor:
            glClear(GL_COLOR_BUFFER_BIT)
        if clearDepth:
            glClear(GL_DEPTH_BUFFER_BIT)

        # Update camera view (calculate inverse)
        camera.updateViewMatrix()

        #
        # Extract list of all Mesh objects in scene using
        #   getDescendantList method and then filter list
        #   using Python functions 'filter' & 'isinstance'
        #
        descendantList = scene.getDescendantList() 
        meshFilter = lambda x : isinstance(x, Mesh) 
        meshList = list( filter( meshFilter, descendantList ) )

        #
        # Extract list of all lights in scene, using a filter
        #   function applied to list of descendents of root
        #   of scene graph.
        #
        lightFilter = lambda x : isinstance(x, Light)
        lightList = list( filter( lightFilter, descendantList ) )
        # Scenes support 4 lights ... precisely 4 must be present
        while len(lightList) < 4:
            lightList.append( Light() )

        for mesh in meshList:
            # If this object is not visible,
            #   continue to next object in list
           if not mesh.visible:
               continue

           # Select shader program to use when rendering
           glUseProgram( mesh.material.programRef )

           # Bind VAO (vertex array object)
           glBindVertexArray( mesh.vaoRef )

           #
           # Values corresponding to model, view, and projection 
           #   matrices (stored outside of material) must be stored
           #   in corresponding uniform objects
           #
           mesh.material.uniforms["modelMatrix"].data = mesh.getWorldMatrix() 
           mesh.material.uniforms["viewMatrix"].data = camera.viewMatrix
           mesh.material.uniforms["projectionMatrix"].data = camera.projectionMatrix

           # If material uses light data, add lights from list
           if "light0" in mesh.material.uniforms.keys():
               for lightNumber in range(4):
                   lightName = "light" + str(lightNumber)
                   lightObject = lightList[lightNumber]
                   mesh.material.uniforms[lightName].data = lightObject
           # If Phong material (specular lighting), add camera position 
           if "viewPosition" in mesh.material.uniforms.keys():
               mesh.material.uniforms["viewPosition"].data = camera.getWorldPosition()


           # Values in all material uniform objects must be uploaded to GPU
           for variableName, uniformObject in mesh.material.uniforms.items():
               uniformObject.uploadData()

           # Render settings are applied via specified OpenGL functions
           mesh.material.updateRenderSettings()

           # Specify correct draw mode and number of vertices to be rendered
           glDrawArrays( mesh.material.settings["drawStyle"], 0,
                         mesh.geometry.vertexCount )

