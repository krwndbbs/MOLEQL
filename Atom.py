# File name: Atom.py
"""
	Atom module file documentation
"""

import numpy as np
import Elements

def atomDistance(a1, a2):
    """
        atomDistance(atom1, atom2)

        args:    atom1 and atom2 are instances of class Atom
        returns: atom1-atom2 distance in Angstroms
    """
    diff = a2.coordinates - a1.coordinates
    distance = np.linalg.norm(diff)
    return distance

def atomAngle(a1, a2, a3):
    """
        atomAngle(atom1, atom2, atom3)

        args:     atom1, atom2, and atom3 are instances of class Atom
        returns:  the angle atom1-atom2-atom3 in degrees
    """
    v1 = (a2.coordinates - a1.coordinates)
    v2 = (a3.coordinates - a2.coordinates)
    lenv1 = atomDistance(a1, a2)
    lenv2 = atomDistance(a3, a2)
    angle = np.arccos( v1.T@v2/(lenv1*lenv2) )  # angle in radians
    return np.rad2deg(angle)                    # angle converted to degrees

def atomDihedral(a1, a2, a3, a4):
    """
        atomDihedral(atom1, atom2, atom3, atom4)

        args:    atom1, atom2, atom3 and atom4 are instances of class Atom
        returns: the dihedral angle atom1-atom2-atom3-atom4 in degrees
    """
    v1 = (a2.coordinates - a1.coordinates)
    v2 = (a3.coordinates - a2.coordinates)
    v3 = (a4.coordinates - a3.coordinates)
    v4 = np.cross(v1, v2)
    v5 = np.cross(v2, v3)
    lenv4 = np.linalg.norm(v4)
    lenv5 = np.linalg.norm(v5)
    angle = np.arccos( v4.T@v5/(lenv4*lenv5) )  # angle in radians
    d = np.rad2deg(angle)
    if (v4 * v3) < 0:
        d = -d
    if d <= -180:
        d = d + 360.0
    return d


def sumOfSingleBondRadii(a1, a2):
    return a1.singleBondRadius() + a2.singleBondRadius()


class Atom:
    """
	Class for individual atoms.

	Base classes:  none
	Subclasses:    none

	Bonding information is stored in atoms
    """

    _instanceVariableDoc = {
        'atomicNumber': """atomic number of the atom (integer)""",
        'coordinates': """(x,y,z) coordinates of this atom, in Angstroms, as np.array""",
        'coordpixels': """(x,y,z) coordinates of this atom, in pixels, as np.array""",
        'radiuspixels': """van der Waal's radius of this atom in pixels (integer)""",
        'bondedAtoms': """a list of the atoms bonded to this atom (list of Atom)""",
        'bondOrder': """a dictionary of the bond orders to each atom in bondedAtoms
                     (dictionary of Atom : Float)""",
        'bondCount': """the total number of atoms bonded to this atom (integer)""",
    }

    _methodCategory = {
        'clear': """Housekeeping""",
        'atomicMass': """Atom information""",
        'atomicSymbol': """Atom information""",
        'singleBondRadius': """Atom information""",
        'terminal': """Atom information""",
        'x': """Atom information""",
        'y': """Atom information""",
        'z': """Atom information""",
        'setCoordinates': """Setting atom properties""",
        'adjacentCoordination': """Bonding information""",
        'bondedTo': """Bonding information""",
        'countBonds': """Bonding information""",
        'countBondedContinuation': """Bonding information""",
        'createBondTo': """Bond creation, deletion, and modification""",
        'deleteBondTo': """Bond creation, deletion, and modification""",
    }

    ### Private methods - standard

    def __init__(self, atomicNumber, x=0, y=0, z=0):
        """
	    Atom(atomicNumber, x=0, y=0, z=0)

	    args:  atomicNumber is the atomic number of the new atom
          	   x,y,z become the coordinates of the new atom
	    returns:  a new instance of class Atom
        """
        self.atomicNumber = atomicNumber
        self.coordinates = np.array([x, y, z])
        self.coordpixels = np.zeros( (3,), dtype=float )
        self.radiuspixels = 0
        self.bondedAtoms = []
        self.bondOrder = {}
        self.bondCount = 0
        return

    def __repr__(self):
        """
            `anAtom`
        
            returns: the string 'Atom atomicSymbol at (x, y, z)' with the
                     appropriate values of atomicSymbol, x, y, and z
        """
        return 'Atom %-2s at (% 9.6f, % 9.6f, % 9.6f)' % (
        self.atomicSymbol(), self.coordinates[0], self.coordinates[1], self.coordinates[2])

    ### Housekeeping methods

    def clear(self):
        """
            clear()

            args:     none
            returns:  None

            Delete all bonding information associated with this atom and
            reset all instance variables to their default values.
        """
        for batom in self.bondedAtoms[:]:
            self.deleteBondTo(batom)
        self.atomicNumber = None
        self.coordinates = None
        return

    def setCoordinates(self, v):
        """
            setCoordinates(vector)

            args:     vector is an instance of class Vector
            returns:  None

            Set the (x,y,z) coordinates of this atom to vector
        """
        self.coordinates = v
        return

    def setX(self, val):
        """
            setX(number)

            args:     number is an Integer or Float
            returns:  None

            Set the x coordinate of this atom to number
        """
        self.coordinates.array[0] = val
        return

    def setY(self, val):
        """
            setY(number)

            args:     number is an Integer or Float
            returns:  None

            Set the x coordinate of this atom to number
        """
        self.coordinates.array[1] = val
        return

    def setZ(self, val):
        """
            setZ(number)

            args:     number is an Integer or Float
            returns:  None

            Set the x coordinate of this atom to number
        """
        self.coordinates.array[2] = val
        return

    def setXYZ(self, x=0, y=0, z=0):
        """
            setXYZ(x, y, z)

            args:     x, y, and z are Integers or Floats
            returns:  None

            Set the x, y, and z coordinates of this atom
        """
        del self.coordinates
        self.coordinates = np.array([x, y, z])
        return

    ### Methods which return properties of this Atom

    def atomicMass(self):
        """
            atomicMass()

            args:     none
            returns:  the atomic mass of this atom based on its atomic number.
                      Values are listed in Elements.py
        """
        return Elements.AtomicMass.get(self.atomicNumber, 0)

    def atomicSymbol(self):
        """
            atomicSymbol()

            args:     none
            returns:  the atomic symbol of this atom.  Values are stored in
                      Elements.py
        """
        return Elements.AtomicSymbol[self.atomicNumber]

    def singleBondRadius(self):
        """
            singleBondRadius()

            args:     none
            returns:  The ordinary single bond radius of the element with
                      this atom's atomic number.  Values are stored in
                      Elements.SingleBondRadius.
        """
        return Elements.SingleBondRadius[self.atomicNumber]

    def atomColor(self):
        """
            atomColor()

            args:     none
            returns:  A list of the rgb values, 0-255, for the element with
                      this atom's atomic number.  Values are stored in
                      Elements.AtomColor.
        """
        return Elements.AtomColor[self.atomicNumber]

    def vdwRadius(self):
        """
            vdwRadius()

            args:     none
            returns:  The van der waal radius of the element with
                      this atom's atomic number.  Values are stored in
                      Elements.VdwRadius.
        """
        return Elements.VdwRadius[self.atomicNumber]

    def x(self):
        """
            x()

            args:     none
            returns:  the value of this atom's x coordinate
        """
        return self.coordinates[0]

    def y(self):
        """
            y()

            args:     none
            returns:  the value of this atom's y coordinate
        """
        return self.coordinates[1]

    def z(self):
        """
            z()

            args:     none
            returns:  the value of this atom's z coordinate
        """
        return self.coordinates[2]

    ### Methods which make, break, or modify bonds

    def createBondTo(self, atom):
        """
            createBondTo(anotherAtom)

            args:     anotherAtom is an instance of class Atom
            returns:  1 if a bond is created, 0 if not

            side effects:  Both this atom and anotherAtom are changed to
                           reflect the bonding information.
        """
        if atom in self.bondedAtoms:
            return 0
        else:
            self.bondedAtoms.append(atom)
            self.bondCount = self.bondCount + 1
            atom.createBondTo(self)
            return 1

    def deleteBondTo(self, atom):
        """
            deleteBondTo(anotherAtom)

            args:     anotherAtom is an instance of class Atom
            returns:  1 if a bond is deleted, 0 if not

            This method deletes the bond (if any) to anotherAtom.

            side effects:  The bonding information in both this atom and
                           anotherAtom are changed.
        """
        if atom in self.bondedAtoms:
            self.bondedAtoms.remove(atom)
            atom.deleteBondTo(self)
            self.bondCount = self.bondCount - 1
            return 1
        else:
            return 0


