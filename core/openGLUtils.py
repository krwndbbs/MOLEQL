# File: openGLUtils.py
"""
   Static methods to load and compile OpenGL shaders
   and link to create programs.
"""
from OpenGL.GL import *

class OpenGLUtils(object):
    """
       initializeShader is declared to be static so that
       it may be called directly from the OpenGLUtils class
       rather than requiring an instance of the class to
       be created.
    """

    @staticmethod
    def initializeShader(shaderCode, shaderType):

        # Specify required OpenGl/GLSL version
        shaderCode = '#version 330\n' + shaderCode

        # Create empty shader object (for storing source code
        #   of a shader) and return reference value
        shaderRef = glCreateShader(shaderType)

        # Store source code in shader
        glShaderSource(shaderRef, shaderCode)

        # Compile source code previously stored in shader object
        glCompileShader(shaderRef)

        # Query whether shader compile was successful
        compileSuccess = glGetShaderiv(shaderRef, GL_COMPILE_STATUS)
        if not compileSuccess:
            # Retrieve error message
            errorMessage = glGetShaderInfoLog(shaderRef)
            # Free memory used to store shader program
            glDeleteShader(shaderRef)
            # Convert byte string to character string
            errorMessage = '\n' + errorMessage.decode('utf-8')
            # Raise exception: halt program & print error message
            raise Exception(errorMessage)

        # Compilation was successful ... return shader reference value
        return shaderRef

    @staticmethod
    def initializeProgram(vertexShaderCode, fragmentShaderCode):
        """
           A program object must be created and the compiled shaders
           must be attached and linked together.
        """

        vertexShaderRef = OpenGLUtils.initializeShader(
                           vertexShaderCode, GL_VERTEX_SHADER)

        fragmentShaderRef = OpenGLUtils.initializeShader(
                             fragmentShaderCode, GL_FRAGMENT_SHADER)

        # Create empty program object (for attaching shader objects)
        #   and store its reference
        programRef = glCreateProgram()

        # Attach previously compiled shader objects to program object
        glAttachShader(programRef, vertexShaderRef)
        glAttachShader(programRef, fragmentShaderRef)

        # Link vertex shader to fragment shader, both of which are 
        #   attached to program object
        glLinkProgram(programRef)

        # Query whether program link was successful
        linkSuccess = glGetProgramiv(programRef, GL_LINK_STATUS)
        if not linkSuccess:
            # Retrieve error message
            errorMessage = glGetProgramInfoLog(programRef)
            # Free memory used to store shader program
            glDeleteProgram(programRef)
            # Convert byte string to character string
            errorMessage = '\n' + errorMessage.decode('utf-8')
            # Raise exception: halt program & print error message
            raise Exception(errorMessage)

        # Linking was successful ... return program reference value
        return programRef

    @staticmethod
    def printSystemInfo():
        print(' Vendor: ' + glGetString(GL_VENDOR).decode('utf-8'))
        print(' Renderer: ' + glGetString(GL_RENDERER).decode('utf-8'))
        print(' OpenGL version supported: ' + glGetString(GL_VERSION).decode('utf-8'))
        print('   GLSL version supported: ' + 
                  glGetString(GL_SHADING_LANGUAGE_VERSION).decode('utf-8'))

