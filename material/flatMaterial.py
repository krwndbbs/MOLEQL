# File: flatMaterial.py
"""
   The simplest shading model is the flat shading model, in which
   face normal vectores are used, calculations take place in the
   vertex shader, and light contribution values are passed along
   to the fragment shader. 

   **Note**
   All code referencing 'texture' has been removed to simplify
   the class for use with PySide6. Also, code allowing the use
   of vertex colors has been incorporated. The original unaltered 
   code may be found in:
   /Users/dobbskd/Python/OpenGLPython/DevGraFraWithPyAndOGL/material/
"""

from material.material import Material
from OpenGL.GL import *

class FlatMaterial(Material):

    def __init__(self, properties={}):
        """
           In OpenGL shader language, GLSL, the 'struct' data
           structure groups together related data variables 
           as a single unit. 'struct Light' is use to store 
           light-related data.
        """
        vertexShaderCode = """
        struct Light
        {
            // 1 = AMBIENT, 2 = DIRECTIONAL, 3 = POINT
            int lightType;
            // used by all lights
            vec3 color;
            // used by directional lights
            vec3 direction;
            // used by point lights
            vec3 position;
            vec3 attenuation;
        };
        // Only 4 uniform Light variables supported
        uniform Light light0;
        uniform Light light1;
        uniform Light light2;
        uniform Light light3;

        //
        // Use lightCalc function to calculate contributions
        //   from combination of ambient, diffuse, & specular
        //   light at a point.
        //
        vec3 lightCalc(Light light, vec3 pointPosition, vec3 pointNormal)
        {
            float ambient = 0;
            float diffuse = 0;
            float specular = 0;
            float attenuation = 1;
            vec3 lightDirection = vec3(0,0,0);
            if ( light.lightType == 1 ) // ambient light
            {
                ambient = 1;
            }
            else if ( light.lightType == 2 ) // directional light
            {
                lightDirection = normalize(light.direction);
            }
            else if ( light.lightType == 3 ) // point light
            {
                lightDirection = normalize(pointPosition - light.position);
                float distance = length(light.position - pointPosition);
                attenuation = 1.0 / (light.attenuation[0] + 
                                     light.attenuation[1] * distance +
                                     light.attenuation[2] * distance * distance);
            }
            if ( light.lightType > 1 ) // directional or point light
            {
                pointNormal = normalize(pointNormal);
                diffuse = max( dot(pointNormal, -lightDirection), 0.0 );
                diffuse *= attenuation;
            }

            return light.color * (ambient + diffuse + specular);
        }

        //
        // Before being used in lightCalc function, model matrix needs to be
        //   applied to the position data and rotational part of model matrix
        //   needs to be applied to normal data.
        //
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        in vec3 vertexPosition;
        in vec3 vertexColor;
        in vec2 vertexUV;
        in vec3 faceNormal;
        out vec2 UV;
        out vec3 light;
        out vec3 color;
        void main()
        {
            gl_Position = projectionMatrix * viewMatrix * 
                                             modelMatrix *
                                             vec4(vertexPosition, 1);
            UV = vertexUV;
            color = vertexColor;
            // Calculate total effect of lights on color
            vec3 position = vec3( modelMatrix * vec4(vertexPosition, 1) );
            vec3 normal = normalize( mat3(modelMatrix) * faceNormal );
            light = vec3(0,0,0);
            light += lightCalc( light0, position, normal );
            light += lightCalc( light1, position, normal );
            light += lightCalc( light2, position, normal );
            light += lightCalc( light3, position, normal );
        }
        """

        #
        # Total light contribution is passed from vertex shader
        #   to determine final color of each fragment.
        # 
        fragmentShaderCode = """
        uniform vec3 baseColor;
        uniform bool useVertexColors;
        in vec2 UV;
        in vec3 light;
        in vec3 color;
        out vec4 fragColor;
        void main()
        {
            vec4 tempColor = vec4(baseColor, 1.0);
            if( useVertexColors )
                tempColor *= vec4(color, 1.0);
            tempColor *= vec4( light, 1 );
            fragColor = tempColor;
        }
        """

        super().__init__(vertexShaderCode, fragmentShaderCode)

        # Uniform objects to be added
        self.addUniform("vec3", "baseColor", [1.0, 1.0, 1.0])
        self.addUniform("Light", "light0", None )
        self.addUniform("Light", "light1", None )
        self.addUniform("Light", "light2", None )
        self.addUniform("Light", "light3", None )
        self.addUniform("bool", "useVertexColors", False)

        self.locateUniforms()

        #
        # *Note*: 'self.settings' dict initiated 
        #         in Material class
        #

        # Render both sides?
        self.settings["doubleSide"] = True

        # Render triangles as wireframe?
        self.settings["wireframe"] = False

        # Line thickness for wireframe
        self.settings["lineWidth"] = 1

        self.setProperties(properties) # method from Material class

    def updateRenderSettings(self):
        """
           Method to call OpenGL functions needed to configure
           render setting previously specified.
        """
        if self.settings["doubleSide"]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)

        if self.settings["wireframe"]:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glLineWidth(self.settings["lineWidth"])

