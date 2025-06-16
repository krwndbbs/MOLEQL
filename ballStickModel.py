# File: ballStickModel.py
"""
   Using OpenGL within PySide6 framework to draw 
   ball and stick model of a molecule.
"""
# Import needed standard libraries
import sys
import numpy as np
from math import pi

# Need following for molecular objects
import Atom
import Elements

# Import any needed third party library
from PySide6.QtCore import Qt
from OpenGL.GL import *

# Import any needed local library
from core.glBase     import GLBase
from core.renderer import Renderer
from core.scene    import Scene
from core.group    import Group
from core.camera   import Camera
from core.matrix   import Matrix
from core.mesh     import Mesh
from geometry.bondGeometry    import BondGeometry
from geometry.sphereGeometry  import SphereGeometry
from light.ambientLight       import AmbientLight
from light.directionalLight   import DirectionalLight
from material.lambertMaterial import LambertMaterial
from material.flatMaterial    import FlatMaterial
from material.phongMaterial   import PhongMaterial

def bondDirection(point1, point2):
    """
       A bond between an atom at point1 and an atom at point2
       has a particular direction in space. The initial 
       drawing of a bond is along the y axis and centered at
       the xyz origin. It is then necessary to determine the
       rotation matrix for the actual bond direction for 
       application to the drawn bond. The code below was
       adopted from pp.221-222 in Computer Graphics: Principles
       and Practice, 2nd ed., 1990.
    """
    vz = np.array([1,0,1])
    v12 = point2 - point1
    PD = v12/np.linalg.norm(v12) # normalize preferred direction
    xp = np.cross(vz, PD)
    zp = np.cross(PD, xp)
    nxp = np.linalg.norm(xp)
    nzp = np.linalg.norm(zp)
    XP = xp/nxp if nxp > 1e-6 else xp
    ZP = zp/nzp if nzp > 1e-6 else zp
    R = np.array( [[XP[0], PD[0], ZP[0], 0],        
                   [XP[1], PD[1], ZP[1], 0],        
                   [XP[2], PD[2], ZP[2], 0],        
                   [    0,      0,     0, 1]] ).astype(float)
    return R

#
# Establish this structure model as a QOpenGLWidget with 
#   pre-established functions/methods.
#
class BallStickModel(GLBase):
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
        self.mouse_track_label.setMaximumHeight(20)

        # Turn on mouse tracking
        self.setMouseTracking(True)

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

        # Initialize radii for bonds and balls
        self.bondRadius = 0.10
        self.ballRadius = 0.30

    def initializeGL(self):
        super().initializeGL()

        # Set scene
        self.renderer = Renderer(self, clearColor=[0.5, 0.5, 0.5]) # set gray background
        self.scene = Scene()
        self.ballstick = Group() # collection of bonds and spheres making up molecule
        self.camera = Camera( angleOfView=60, aspectRatio=1, near=0.1, far=1000 ) 
        self.camera.setPosition( [0, 0, 6] ) # set camera along positive z-axis

        # Establish lighting for scene
        ambient = AmbientLight( color=[0.8, 0.8, 0.8] )
        self.scene.add( ambient )
        directional = DirectionalLight( color=[1.0, 1.0, 1.0], direction=[3, 0, -3] )
        self.scene.add( directional )

        #
        # Use Flat lighting model for bonds and 
        #   Phong lighting model for spheres.
        #
        flatMat = FlatMaterial( properties={ "useVertexColors" : True } )
        phongMat = PhongMaterial( properties={ "useVertexColors" : True,
                                               "shininess" : 64,
                                               "specularStrength" : 1.5} )

        # Update bondRadius to represent current molecular size
        self.bondRadius = self.bondRadius * self.molecule.scaler

        # Draw each bond of molecule
        for bond in self.molecule.bonds:
            atom1, atom2 = bond[0], bond[1]
            bondLength = Atom.atomDistance(atom1, atom2)
            bondMidpoint = (atom1.coordinates + atom2.coordinates)/2
            rgb1 = (np.array(Elements.AtomColor[atom1.atomicNumber]))/255
            rgb2 = (np.array(Elements.AtomColor[atom2.atomicNumber]))/255
            # Convert numpy arrays, rgb1 and rgb2, to Python lists
            c1, c2 = rgb1.tolist(), rgb2.tolist()
            #
            # Draw a 2-color bond with radius and length along the y-axis
            #   and centered at the origin
            #
            bondGeometry = BondGeometry(radius=self.bondRadius, height=bondLength,
                                        radialSegments=32,
                                        color1=c1, color2=c2)
            #
            # Transform bondGeometry such that it has same direction vector 
            #   as that between the 2 atoms of the bond.
            #
            bondGeometry.applyMatrix( bondDirection(atom1.coordinates, atom2.coordinates) )
            #
            # Translate center (0,0,0) of drawn bondGeometry to actual bond
            #   center (x,y,z) between the 2 atoms.
            #
            x, y, z = bondMidpoint.tolist()
            bondGeometry.applyMatrix( Matrix.makeTranslation(x,y,z) )
            #
            # Apply shading model to bond
            #
            bondObject = Mesh(bondGeometry, flatMat)
            self.ballstick.add(bondObject)

        # Update ballRadius to represent current molecular size
        self.ballRadius = self.ballRadius * self.molecule.scaler

        # Draw each atom of molecule as a shaded sphere
        for atom in self.molecule.atoms:
            atom_coord = atom.coordinates
            rgb = (np.array(Elements.AtomColor[atom.atomicNumber]))/255
            # Convert numpy array, rgb, to Python list
            color = rgb.tolist()
            #
            # Draw a single-color sphere/ball with radius and centered at the origin
            #
            sphereGeometry = SphereGeometry(radius=self.ballRadius, color1=color, color2=color)
            #
            # Apply shading model to sphere/ball
            # 
            sphereObject = Mesh(sphereGeometry, phongMat)
            #
            # Translate center (0,0,0) of sphere/ball to actual atom coordinates
            #
            sphereObject.setPosition(atom_coord)
            self.ballstick.add(sphereObject)

        self.scene.add(self.ballstick)

    def paintGL(self):
        super().paintGL()

        self.setFocus()
        localCoord = False

        # Rotation actions upon mouse presses and movements
        if self.xy_rotation:
            self.ballstick.rotateX( self.phi, localCoord )
            self.ballstick.rotateY( self.theta, localCoord )
            self.molecule.rotateXYZ(self.phi, self.theta, 0)
        elif self.z_rotation:
            self.ballstick.rotateZ( self.chi, localCoord )
            self.molecule.rotateXYZ(0, 0, self.chi)
       
        # Scaling actions upon key presses
        if self.input.isKeyDown(Qt.Key_L):
            self.ballstick.scale( 1.1, localCoord )
            self.molecule.scaleXYZ(1.1)
        if self.input.isKeyDown(Qt.Key_S):
            self.ballstick.scale( 0.9, localCoord )
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
            self.phi = dy * to_rad
            self.theta = dx * to_rad
            self.update()
        elif (event.buttons() and Qt.MouseButton.RightButton) and self.z_rotation:
            self.chi = dy * to_rad
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

