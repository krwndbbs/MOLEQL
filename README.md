# MOLEQL -- a basic molecular structure display program
The MOLEQL ("molecule") project is the minimum Python code necessary to display 
molecules in 3 different structure models: stick model, ball-and-stick model, or
CPK or space-filling model. OpenGL is used to render the models as true 3D structures.

## Installation

My installation of the code (*.py, *.xyz, and directories) is within a main 
directory that I have named "moleql". The code was developed on an 2020 iMac
with macOS Monterey 12.7.5 under Python 3.10. Without any modifications, the 
code runs fine in my current environment of Python 3.13 on a 2025 Mac Studio 
with macOS Sequoia 15.5. Besides Python, you will need to install the following 
libraries:

- numpy (version 2.2.6): `pip3 install numpy`

- PyOpenGL (version 3.1.9): `pip3 install PyOpenGL PyOpenGL_accelerate`

- PySide6 (version 6.9.1): `pip3 install PySide6`


## Running of program

The program is launched from the command line: `python mainWindow.py`

Under the "File" menu, choose "Open" and then select a [].xyz file to view. Once
the coordinate file has been processed, a dialogue window will pop up, telling you
to choose a structure model from the "View" menu. The appearance of the structure
will be very quick for small molecules but will take noticeably more time for larger
molecules, especially for the ball-and-stick and space-filling models. 

Once a molecule is rendered, it may be rotated about the x and y axes with the left mouse
button. Rotation about the z axis occurs by pressing the right mouse button and moving 
the mouse along the y axis of the window. The size of the model may be made smaller by
depressing the "S" key or larger with the "L" key. No other manipulations have been 
programmed at this time.


## Acknowledgements and Citations

- I needed to learn GUI programming in the Python environment. The book, "Beginning PyQt-Second Edition",
  by Joshua M. Willman was invaluable. [*Willman's GitHub*](https://github.com/Apress/Beginning-PyQt--second-edition/tree/main) page was also quite
  useful in this learning process.

## Contributions

Anyone interested in contributing to this project should contact me by email:

kerwin.d.dobbs@gmail.com

Please keep in mind that I'm new to GitHub and how it works. It may take me some
time to figure out how some things work.
