#File: processMolecule.py
"""
   Process atoms and associated coordinates to determine
   which atoms are bonded along with their respective 
   bond lengths. Also, atomic coordinates are adjusted 
   to center the molecule at origin, [0, 0, 0]
"""
# Need following for molecular objects
import Atom
import Elements

# Import third party libraries
from PySide6.QtWidgets import QMessageBox

def processMolecule(self, molecule):
    """ Complete processing of molecule.  """
    ###
    ###print('atomCount = ', molecule.atomCount)
    ###print('')
    ###
    # Create molecular bonds
    molecule.findBonds()  
    ###
    ###print('bondCount = ', molecule.bondCount)
    ###for bond in molecule.bonds:
    ###    print(bond[0], ' bonded to ', bond[1])
    ###    print(bond[0].coordinates[0], bond[0].coordinates[1], bond[0].coordinates[2])
    ###    print(bond[1].coordinates[0], bond[1].coordinates[1], bond[1].coordinates[2])
    ###print('')
    ###for atom in molecule.atoms:
    ###    print('            atom = ', atom)
    ###    print('  atom.bondCount = ', atom.bondCount)
    ###    print('atom.bondedAtoms = ', atom.bondedAtoms)
    ###print('')
    ###

    # minAtom: minimum values of x, y, z coordinates in molecule
    # maxAtom: maximum values of x, y, z coordinates in molecule
    # maxCoord: maximum extension (Angstroms) of molecule in 3D space is
    #           the distance between minAtom and maxAtom. This value
    #           will be used to convert atom coordinates from Angstroms
    #           to pixels and vice versa.
    ###(minAtom, maxAtom) = molecule.extrema()
    ###self.maxCoord = molecule.maxExtension(minAtom, maxAtom)
    ###radext = 2
    ###maxangstroms = molecule.maxExtension(minAtom, maxAtom, radext)

    # Determine the center of the molecular coordinates
    boxCenter = molecule.bounding_box_center()

    ###
    ###print('minAtom, maxAtom = ', minAtom, ', ', maxAtom)
    ###print('        maxCoord = ', self.maxCoord)
    ###print('      box_center = ', boxCenter)
    ###print('')
    ###print(' Before centering of molecule:')
    ###print('    atoms = ', molecule.atoms)
    ###print('')
    ###

    # Translate the center of the molecule so it is at the origin.
    for atom in molecule.atoms:
        atom.coordinates = atom.coordinates - boxCenter

    ###
    ###print(' After centering of molecule:')
    ###for atom in molecule.atoms:
    ###    rgb = (np.array(Elements.AtomColor[atom.atomicNumber]))/255
    ###    print('    atom, VWD radius, rgb = ', atom, atom.vdwRadius(), rgb)
    ###print('')
    ###for bond in molecule.bonds:
    ###    atom1, atom2 = bond[0], bond[1]
    ###    symbol1 = Elements.AtomicSymbol[atom1.atomicNumber]
    ###    symbol2 = Elements.AtomicSymbol[atom2.atomicNumber]
    ###    if (symbol1 == 'Ir' and symbol2 == 'N') or (symbol1 == 'N' and symbol2 == 'Ir'):
    ###        s = Atom.sumOfSingleBondRadii(atom1, atom2)
    ###        d = Atom.atomDistance(atom1, atom2)
    ###        t = 1.2 * s
    ###        print(' atom1, atom2 = ', atom1, atom2)
    ###        print('      s, d, t = ', s, d, t)
    ###print('')
    ###

    #
    # Finally, launch message box to tell user to choose 
    #   which structure model to draw
    #
    QMessageBox.information(self, "Atom coordinates ready for drawing!",
                            """<p>Atom coordinates ready for drawing!<\p>
                            <p>Choose structure model from View menu.<\p>""",
                            QMessageBox.StandardButton.Ok,
                            QMessageBox.StandardButton.Ok)

