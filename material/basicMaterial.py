# File: basicMaterial.py
"""
   An extension of the Material class which contains shader code
   and a set of corresponding uniforms. The shaders can be used
   to render points, lines, or sufaces. The shaders for basic 
   material use two attributes: vertex positions and vertex colors.
"""

from material.material import Material
from core.uniform import Uniform

class BasicMaterial(Material):

    def __init__(self):

        # *** Vertex Shader ***
        # • Vertex color data sent from vertex shader
        #     to fragment shader via variable 'color'
        # • Vertex shader uses uniform variables model,
        #     view, & projection matrices to calculate
        #     final position of each vertex
        #
        vertexShaderCode = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        in vec3 vertexPosition;
        in vec3 vertexColor;
        out vec3 color;
        void main()
        {
            gl_Position = projectionMatrix * viewMatrix *
                  modelMatrix * vec4(vertexPosition, 1.0);
            color = vertexColor;
        }
        """

        # *** Fragment Shader ***
        # • Uniform variable 'baseColor' contains a color 
        #     applied to all vertices with default value
        #     being (1, 1, 1), i.e., white
        # • Uniform variable useVertexColors is boolean
        #     value determining whether data stored in
        #     vertex color attribute will be applied to
        #     base color
        #
        fragmentShaderCode = """
        uniform vec3 baseColor;
        uniform bool useVertexColors;
        in vec3 color;
        out vec4 fragColor;
        void main()
        {
            vec4 tempColor = vec4(baseColor, 1.0);
            if(useVertexColors)
                tempColor *= vec4(color, 1.0);
            fragColor = tempColor;
        }
        """

        super().__init__(vertexShaderCode, fragmentShaderCode)
        self.addUniform("vec3", "baseColor", [1.0,1.0,1.0])
        self.addUniform("bool", "useVertexColors", False)
        self.locateUniforms()

