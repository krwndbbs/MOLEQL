# File name: Molecule.py
"""
      This file, Molecule.py, is a significantly modified version
        of Paul Soper's AtomCollection.py file.
"""

import Atom
import Elements
import numpy as np

from core.matrix   import Matrix

class Molecule:
    """
        Class for a collection of atoms as a molecule.

        Base classes:  none
    """

    ### Class variables

    _instanceVariableDoc = {
        'atomCount': """the number of atoms in this molecule (integer)""",
        'bondCount': """the number of bonds in this molecule (integer)""",
        'atoms': """a list of the atoms in this molecule""",
        'bonds': """a list of tuples: (atomA, atomB, bond length)""",
        'scaler': """a number to scale size of molecule (real)""",
    }

    ### Private methods - standard

    def __init__(self, atoms=None):
        """
            Molecule(atoms=None)

            args:     atoms is a list of instances of class Atom
            returns:  a new instance of class Molecule
        """
        self.atomCount = 0
        self.bondCount = 0
        self.atoms = []
        self.bonds = []
        self.scaler = 1.0
        if atoms:
            for atom in atoms:
                self.addAtom(atom)

        return

    ### Housekeeping methods

    def clear(self):
        """
            clear()

            args:     none
            returns:  None

            Delete all atoms, rings, rotors, vibrations, and Z-matrix
              information associated with this atomCollection and reset
              all instance variables to their default values.
        """
        for atom in self.atoms[:]:
            self.deleteAtom(atom)
        self.atomCount = 0
        self.bondCount = 0

    ### Molecular file I/O and printing

    def printAtom(self, atom, indent=0):
        print("%s%-7s %-10s %s" % (" " * indent, self.atomString(atom), id(atom), atom))
        return

    def printAtoms(self, atomList=None, indent=0):
        if atomList is None:
            atomList = self.atoms
        for atom in atomList:
            self.printAtom(atom, indent)
        return

    def printCoordinates(self, atomList=None, indent=0):
        if atomList is None:
            atomList = self.atoms
        for atom in atomList:
            print("%s%-7s %-10s % 6.2f % 6.2f % 6.2f" % (
                " " * indent, self.atomString(atom), id(atom), atom.x(), atom.y(), atom.z()))
        return

    ### Methods which return molecular or substructure properties

    def atomAngleString(self, a1, a2, a3):
        return "Angle    %s-%s-%s = %.1f" % (
            self.atomString(a1), self.atomString(a2), self.atomString(a3), Atom.atomAngle(a1, a2, a3))

    def atomCoordinateString(self, atom):
        return '%s(%d) at (% 5.2f, % 5.2f, % 5.2f)' % (
            atom.atomicSymbol(), 1 + self.atoms.index(atom), atom.coordinates[0], atom.coordinates[1],
            atom.coordinates[2])

    def atomDihedralString(self, a1, a2, a3, a4):
        return "Dihedral %s-%s-%s-%s = %.1f" % (
            self.atomString(a1), self.atomString(a2), self.atomString(a3), self.atomString(a4),
            Atom.atomDihedral(a1, a2, a3, a4))

    def atomDistanceString(self, a1, a2):
        return "Distance %s-%s = %.3f" % (self.atomString(a1), self.atomString(a2), Atom.atomDistance(a1, a2))

    def atomName(self, atom):
        return "%s%d" % (atom.atomicSymbol(), 1 + self.atoms.index(atom))

    def atomString(self, atom):
        return "%s(%d)" % (atom.atomicSymbol(), 1 + self.atoms.index(atom))

    def countAtoms(self):
        self.atomCount = len(self.atoms)
        return self.atomCount

    def countBonds(self, atomList=None):
        if atomList is None:
            atomList = self.atoms
        count = 0
        for atom in atomList:
            for batom in atom.bondedAtoms:
                if batom in atomList:
                    count = count + 1
        if atomList == self.atoms:
            self.bondCount = count / 2
        return count / 2

    def extrema(self):
        """
            Return a tuple of two Vector's containing 
              the min and max x y z values.
        """
        vl = self.atoms[0].coordinates
        vh = self.atoms[0].coordinates
        for atom in self.atoms:
            vl = np.minimum(vl, atom.coordinates)
            vh = np.maximum(vh, atom.coordinates)
        return vl, vh

    def bounding_box_center(self):
        """
            bounding_box_center()
            args:     none
            returns:  Vector

            bounding_box_center() returns a Vector which is the 
              center of the AtomCollection's bounding box.
        """
        (vl, vh) = self.extrema()
        return (vh + vl) / 2

    def maxExtension(self, minvec, maxvec, radext=0):
        """
            maxExtension()
            args:     none
            returns:  distance between vector endpoints
        """
        diff = maxvec - minvec + radext
        ###print(' diff = ', diff)
        distance = np.linalg.norm(diff)
        return distance

    def toPixels(self, ang_to_pix):
        """
            toPixels(ang_to_pix)
               args:  ang_to_pix => constant to convert Angstroms
                                    to pixels
            returns:  atom coordinates and corresponding van der Waal
                      radius in pixel units
        """
        for atom in self.atoms:
            # Use np.rint to round floating point pixel 
            #   values to nearest integers
            ###atom.coordpixels = np.rint(atom.coordinates * ang_to_pix)
            ###atom.radiuspixels = round(atom.vdwRadius() * ang_to_pix)
            atom.coordpixels = atom.coordinates * ang_to_pix
            atom.radiuspixels = atom.vdwRadius() * ang_to_pix
        return

    ### Methods which change molecular structure

    def addAtom(self, newAtom):
        if not newAtom in self.atoms:
            self.atoms.append(newAtom)
            self.atomCount = self.atomCount + 1
        return

    def bondAtoms(self, bondFromAtom, bondToAtom):
        """
            newBond is 1 if a bond is created, 0 if not
        """
        newBond = bondFromAtom.createBondTo(bondToAtom)
        if newBond:
            bond = (bondFromAtom, bondToAtom)
            self.bonds.append(bond)
            self.bondCount = self.bondCount + newBond
        return

    def unbondAtoms(self, bondFromAtom, bondToAtom):
        self.bondCount = self.bondCount - bondFromAtom.deleteBondTo(bondToAtom)
        return

    def deleteAtom(self, atom):
        for batom in atom.bondedAtoms:
            self.unbondAtoms(atom, batom)
        self.removeAtom(atom)
        atom.clear()
        del atom
        return

    def deleteAtoms(self):
        for atom in self.atoms:
            self.deleteAtom(atom)
        return

    def removeAtom(self, atom):
        if atom not in self.atoms:
            return
        self.atoms.remove(atom)
        self.atomCount = self.atomCount - 1
        return

    def xyzRotate(self, deltaX, deltaY, deltaZ):
        """
            Rotate the molecule based on deltaX, deltaY, & deltaZ
         
            phi == rotation angle about X axis
          theta == rotation angle about Y axis
            chi == rotation angle about Z axis

            Returns altered xyz coordinates resulting from 
            rotation about the X, Y, & Z axes. Coordinates
            are in pixels, not Angstroms.
        """
        import math as m

        to_rad = 4.0 * m.atan(1.0) / 180.0
        ###phi   = deltaX * to_rad
        ###theta = deltaY * to_rad
        ###chi   = deltaZ * to_rad
        phi   = -deltaX * to_rad
        theta = -deltaY * to_rad
        chi   = -deltaZ * to_rad
        coseat = m.cos(theta)
        sineat = m.sin(theta)
        coseac = m.cos(chi)
        sineac = m.sin(chi)
        coseap = m.cos(phi)
        sineap = m.sin(phi)
        cs1 = coseac * coseat
        cs2 = coseat * sineac
        cs3 = coseap * sineac
        cs4 = coseac * coseap
        cs5 = coseat * sineap
        cs6 = sineac * sineap
        cs7 = coseac * sineap
        cs8 = coseap * coseat
        cs9  = cs7 * sineat
        cs10 = cs6 * sineat
        cs11 = cs4 * sineat
        cs12 = cs3 * sineat

        # apply rotation matrix to coordinates
        for atom in self.atoms:
            x = atom.coordpixels[0]
            y = atom.coordpixels[1]
            z = atom.coordpixels[2]
            atom.coordpixels[0] = (x * cs1) - (y * cs2) - (z * sineat)
            atom.coordpixels[1] = x * (cs3 - cs9) + y * (cs4 + cs10) - (z * cs5)
            atom.coordpixels[2] = x * (cs6 + cs11) + y * (cs7 - cs12) + (z * cs8)

        return

    def rotateXYZ(self, deltaX, deltaY, deltaZ):
        """
            Using matrix multiplication, rotate the molecule. 
         
            deltaX == rotation angle about X axis (radians)
            deltaY == rotation angle about Y axis (radians)
            deltaZ == rotation angle about Z axis (radians)

            Returns altered xyz coordinates resulting from 
            rotating xyz coordinates (Angstroms).
        """
        transform = (Matrix.makeRotationZ(deltaZ) @
                     Matrix.makeRotationY(deltaY) @
                     Matrix.makeRotationX(deltaX))
        # Get 3x3 submatrix with just rotation part
        transform = np.array( [ transform[0][0:3],
                                transform[1][0:3],
                                transform[2][0:3] ] )

        # Apply tranform matrix to atomic coordinates
        for atom in self.atoms:
            atom.coordinates = transform @ atom.coordinates

        return

    def scaleXYZ(self, factor):
        """
            Using matrix multiplication, scale coordinates of
            the molecule. 
         
            factor == scaling factor (real number)

            Returns:
              • altered xyz coordinates resulting from scaling 
                xyz coordinates (Angstroms).
              • updated scaler for molecule
        """
        transform = Matrix.makeScale(factor)
        # Get 3x3 submatrix with just scaling part
        transform = np.array( [ transform[0][0:3],
                                transform[1][0:3],
                                transform[2][0:3] ] )

        # Apply tranform matrix to atomic coordinates
        for atom in self.atoms:
            atom.coordinates = transform @ atom.coordinates

        # Update scaler with 'factor'
        self.scaler = self.scaler * factor

        return

    ### Methods to find bonds

    def findBonds(self):
        self._computeBonds()
        return

    ### Private methods - bond order

    def _computeNonTransitionMetalBonds(self, factor=1.2):
        delta = 0
        for i in range(self.atomCount - 1):
            a1 = self.atoms[i]
            for j in range(i + 1, self.atomCount):
                a2 = self.atoms[j]
                s = Atom.sumOfSingleBondRadii(a1, a2)
                d = Atom.atomDistance(a1, a2)
                if d <= factor * s:
                    self.bondAtoms(a1, a2)
                    delta = delta + 1

        return delta

    def _computeBonds(self, factor=1.2):
        return self._computeNonTransitionMetalBonds(factor)

