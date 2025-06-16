# File: cpkModel.py
"""
   Using OpenGL within PySide6 framework to draw 
   space-filling model of a molecule.
"""
# Import needed standard libraries
import sys
import numpy as np

# Need following for molecular objects
import Elements

# Import needed third party libraries
from PySide6.QtCore import Qt
from OpenGL.GL import *

# Import needed local libraries
from core.glBase   import GLBase
from core.renderer import Renderer
from core.scene    import Scene
from core.group    import Group
from core.camera   import Camera
from core.matrix   import Matrix
from core.mesh     import Mesh
from geometry.sphereGeometry    import SphereGeometry
from light.ambientLight         import AmbientLight
from light.directionalLight     import DirectionalLight
from material.phongMaterial     import PhongMaterial

#
# Establish this structure model as a QOpenGLWidget with 
#   pre-established functions/methods.
#
class CpkModel(GLBase):
    def __init__(self, parent, molecule, label):
        super().__init__(parent)

        self.parent = parent      # main window for graphics display
        self.molecule = molecule  # molecule object for display
        self.setFocus()           # give keyboard input focus to this widget
        #
        # Use a label to keep track of mouse coordinates
        #   and to display current mouse position
        #
        self.mouse_track_label = label

        # Turn on mouse tracking
        self.setMouseTracking(True)
        self.mouse_track_label.setMaximumHeight(20)

        # Initialize following 2 attributes which track
        #   mouse's previous x,y coords for rotation about
        #   x, y, & z axes.
        self.prev_x = 0
        self.prev_y = 0
        
        self.xy_rotation = False  # No initial x,y rotation
        self.z_rotation = False   # No initial z rotation

        # Initialize following 3 rotation angle attributes
        self.phi = 0   # x-axis rotation angle
        self.theta = 0 # y-axis rotation angle
        self.chi = 0   # z-axis rotation angle

    def initializeGL(self):
        super().initializeGL()

        # Set scene
        self.renderer = Renderer(self, clearColor=[0.5, 0.5, 0.5]) # set gray background
        self.scene = Scene()
        self.spheres = Group() # collection of spheres/balls making up molecule
        self.camera = Camera( angleOfView=60, aspectRatio=1, near=0.1, far=1000 ) 
        self.camera.setPosition( [0, 0, 6] ) # set camera along positive z-axis

        # Establish lighting for scene
        ambient = AmbientLight( color=[0.8, 0.8, 0.8] )
        self.scene.add( ambient )
        directional = DirectionalLight( color=[1.0, 1.0, 1.0], direction=[3, 0, -3] )
        self.scene.add( directional )

        # Use Phong lighting model for spheres ??? more comments ???
        phongMat = PhongMaterial( properties={ "useVertexColors" : True,
                                               "shininess" : 64,
                                               "specularStrength" : 1.5} )

        # Draw each atom of molecule as a shaded sphere
        for atom in self.molecule.atoms:
            atom_coord = atom.coordinates
            #
            # Get atom van der Waals radius and adjust 
            #   with molecule's scale factor.
            #
            vdw_radius = Elements.VdwRadius[atom.atomicNumber] * self.molecule.scaler
            rgb = (np.array(Elements.AtomColor[atom.atomicNumber]))/255
            # Convert numpy array, rgb, to Python list
            color = rgb.tolist()
            #
            # Draw a single-color sphere/ball with radius and centered at the origin
            #
            sphereGeometry = SphereGeometry(radius=vdw_radius, color1=color, color2=color)
            #
            # Apply shading model to sphere/ball
            # 
            sphereObject = Mesh(sphereGeometry, phongMat)
            #
            # Translate center (0,0,0) of sphere/ball to actual atom coordinates
            #
            sphereObject.setPosition(atom_coord)
            self.spheres.add(sphereObject)

        self.scene.add(self.spheres)

    def paintGL(self):
        super().paintGL()

        self.setFocus()
        localCoord = False

        # Rotation actions upon mouse presses and movements
        if self.xy_rotation:
            self.spheres.rotateX( self.phi, localCoord )
            self.spheres.rotateY( self.theta, localCoord )
            self.molecule.rotateXYZ(self.phi, self.theta, 0)
        elif self.z_rotation:
            self.spheres.rotateZ( self.chi, localCoord )
            self.molecule.rotateXYZ(0, 0, self.chi)
       
        # Scaling actions upon key presses
        if self.input.isKeyDown(Qt.Key_L):
            self.spheres.scale( 1.1, localCoord )
            self.molecule.scaleXYZ(1.1)
        if self.input.isKeyDown(Qt.Key_S):
            self.spheres.scale( 0.9, localCoord )
            self.molecule.scaleXYZ(0.9)

        # Render molecular structure
        self.renderer.render( self.scene, self.camera )

    def mousePressEvent(self, event):
        """ 
           Left mouse press initiates xy rotation.
           Right mouse press initiates z rotation.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.prev_x = event.position().x() # Store current mouse x position
            self.prev_y = event.position().y() # Store current mouse y position
            self.xy_rotation = True            # Rotate molecule with mouse
        elif event.button() == Qt.MouseButton.RightButton:
            self.prev_y = event.position().y() # Store current mouse y position
            self.z_rotation = True             # Rotate molecule with mouse

    def mouseReleaseEvent(self, event):
        """
           Upon release of left or right mouse button,
           stop molecule rotation.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.xy_rotation = False
        elif event.button() == Qt.MouseButton.RightButton:
            self.z_rotation = False

    def mouseMoveEvent(self, event):
        """
           Handle mouse movements. If left mouse button is pressed,
           rotate molecule with mouse movement. If right mouse is
           pressed, rotate about the z axis with mouse movement.
           Otherwise, track coordinates of mouse in window and
           display them in status bar.
        """
        import math as m

        to_rad = 4.0 * m.atan(1.0) / 180.0    # convert degrees to radians
        curr_x = event.position().x()
        curr_y = event.position().y()
        dx = curr_x - self.prev_x
        dy = curr_y - self.prev_y
        # Call update() upon clicking left mouse button.
        if (event.buttons() and Qt.MouseButton.LeftButton) and self.xy_rotation:
            self.phi = dy * to_rad   # y movement rotates about x axis
            self.theta = dx * to_rad # x movement rotates about y axis
            self.update()
        elif (event.buttons() and Qt.MouseButton.RightButton) and self.z_rotation:
            self.chi = dy * to_rad   # y movement rotates about z axis
            self.update()
        self.prev_x = curr_x
        self.prev_y = curr_y

        # Pass mouse_pos coords to mouse_track_label to
        #   display in status bar.
        self.mouse_track_label.setVisible(True)
        sb_text = f"""<p>Mouse Coordinates: ({curr_x},
                         {curr_y})<p>"""
        self.mouse_track_label.setText(sb_text)
        self.parent.status_bar.addWidget(self.mouse_track_label)

