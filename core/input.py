#File: input.py
"""
   Modified version of EagleEatApple original. 
"""
# Import third party library
from PySide6.QtCore import QEvent

class KeyEvent:
    def __init__(self,key,type):
        self.key = key
        self.type = type

class Input(object):
    def __init__(self) -> None:
        #
        # lists to store key states
        #   down, up: discrete event; lasts for one iteration
        #
        self.keyDownList    = []
        self.keyUpList      = []
        self.keyEvents      = []

    def update(self):
        # Reset discrete key states
        self.keyDownList = []
        self.keyUpList = []

        # iterate over all user input events (such as keyboard or
        #  mouse) that occurred since the last time events were checked
        for event in self.keyEvents:
            # Check for keydown and keyup events;
            # get name of key from event 
            # and append to or remove from corresponding lists
            if event.type == QEvent.KeyPress:
                self.keyDownList.append(event.key)
            if event.type == QEvent.KeyRelease:
                self.keyUpList.append(event.key)
        self.keyEvents = []

    # functions to check key states
    def isKeyDown(self,key):
        return key in self.keyDownList
    
    def isKeyUp(self, key):
        return key in self.keyUpList
    
    def receiveKeyEvent(self, key, type):
        self.keyEvents.append(KeyEvent(key, type))

