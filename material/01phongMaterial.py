# File: phongMaterial.py
"""
   Modeling Phong material is similar to that of Lambert material but also
   includes specular light contributions. The Phong shading model is applied,
   but the light calculations are different. Rather than determining the 
   angle between the surface normal vector and light direction vector, as
   in the Lambert material, the angle of interest in the Phong material 
   involves the reflection of the light direction vector and the vector
   from the viewer (or virtual camera) to the surface point.

   **Note**
   All code referencing 'shadows' have been removed to simplify 
   the class for use with PySide6. The original unaltered code may 
   be found in:
   /Users/dobbskd/Python/OpenGLPython/DevGraFraWithPyAndOGL/material/
"""

from material.material import Material
from OpenGL.GL import *

class PhongMaterial(Material):

    def __init__(self, properties={}):

        # Use struct data structure to store light-related data
        vertexShaderCode = """

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
        in vec3 vertexNormal;
        out vec3 position;
        out vec3 color;
        out vec2 UV;
        out vec3 normal;
        void main()
        {
            gl_Position = projectionMatrix * viewMatrix * 
                                             modelMatrix *
                                             vec4(vertexPosition, 1);
            color = vertexColor;
            position = vec3( modelMatrix * vec4(vertexPosition, 1) );
            UV = vertexUV;
            // Calculate total effect of lights on color
            normal = normalize( mat3(modelMatrix) * vertexNormal );
        }
        """

        #
        # Total light contribution is passed from vertex shader
        #   to determine final color of each fragment.
        # 
        fragmentShaderCode = """
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
        uniform Light light0;
        uniform Light light1;
        uniform Light light2;
        uniform Light light3;

        //
        //  Use lightCalc function to calculate contributions from 
        //    combination of ambient, diffuse, & specular light.
        //
        in vec3 color;
        uniform bool useVertexColors;
        uniform vec3 viewPosition;
        uniform vec3 baseColor;
        uniform float ambientR;
        uniform float ambientG;
        uniform float ambientB;
        uniform float diffuseR;
        uniform float diffuseG;
        uniform float diffuseB;
        uniform float specularStrength;
        uniform float shininess;
        vec3 lightCalc(Light light, vec3 pointPosition, vec3 pointNormal)
        {
            float ambient = 0;
            //float diffuse = 0;
            float costh = 0;
            float csthsq = 0;
            float rspec = 0;
            float gspec = 0;
            float bspec = 0;
            float specular = 0;
            float attenuation = 1;
            vec3 lightDirection = vec3(0,0,0);
            vec3 colorShade = vec3(0,0,0);
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
                //float distance = length(light.position - pointPosition);
                //attenuation = 1.0 / (light.attenuation[0] + 
                //                     light.attenuation[1] * distance +
                //                     light.attenuation[2] * distance * distance);
            }
            if ( light.lightType > 1 ) // directional or point light
            {
                pointNormal = normalize(pointNormal);
                costh = max( dot(pointNormal, -lightDirection), 0.0 );
                csthsq = costh * costh;
                //diffuse *= attenuation;
                vec3 tempColor = baseColor;
                if ( useVertexColors )
                    tempColor = color;
                float c0 = ambientR*tempColor[0] + diffuseR*tempColor[0]*costh;
                float c1 = ambientG*tempColor[1] + diffuseG*tempColor[1]*costh;
                float c2 = ambientB*tempColor[2] + diffuseB*tempColor[2]*costh;
                if (csthsq >= 0.0)
                {
                    vec3 viewDirection = normalize(viewPosition - pointPosition);
                    vec3 reflectDirection = reflect(lightDirection, pointNormal);
                    specular = max( dot(viewDirection, reflectDirection), 0.0 );
                    //specular = specularStrength * pow(specular, shininess);
                    //float base = 2*csthsq - 1.0;
                    //float gloss = specularStrength * pow(base, shininess);
                    float gloss = specularStrength * pow(specular, shininess);
                    colorShade[0] = min( (c0 + (1.0 - c0)*gloss), 1.0);
                    colorShade[1] = min( (c1 + (1.0 - c1)*gloss), 1.0);
                    colorShade[2] = min( (c2 + (1.0 - c2)*gloss), 1.0);
                }

            }

            //return light.color * (ambient + diffuse + specular);
            return colorShade;
        }

        //uniform vec3 baseColor;
        in vec3 position;
        in vec2 UV;
        in vec3 normal;
        out vec4 fragColor;
        void main()
        {
            //vec4 color = vec4(baseColor, 1.0);
            //if ( useTexture )
            //    color *= texture( texture2D, UV );
            // Calculate total effect of lights on color
            vec3 total = vec3(0,0,0);
            total += lightCalc( light0, position, normal );
            total += lightCalc( light1, position, normal );
            total += lightCalc( light2, position, normal );
            total += lightCalc( light3, position, normal );
            //color *= vec4( total, 1 );
            vec4 color = vec4( total, 1 );
            fragColor = color;
        }
        """

        super().__init__(vertexShaderCode, fragmentShaderCode)

        # Uniforms to be added
        self.addUniform("vec3", "baseColor", [1.0, 1.0, 1.0])
        self.addUniform("Light", "light0", None )
        self.addUniform("Light", "light1", None )
        self.addUniform("Light", "light2", None )
        self.addUniform("Light", "light3", None )
        self.addUniform("vec3", "viewPosition", [0,0,0])
        self.addUniform("float", "ambientR", 0.32)
        self.addUniform("float", "ambientG", 0.30)
        self.addUniform("float", "ambientB", 0.35)
        self.addUniform("float", "diffuseR", 0.60)
        self.addUniform("float", "diffuseG", 0.60)
        self.addUniform("float", "diffuseB", 0.60)
        self.addUniform("float", "specularStrength", 1)
        self.addUniform("float", "shininess", 32)
        self.addUniform("bool", "useVertexColors", False)

        self.locateUniforms()

        #
        # 'settings' dict initiated in Material class
        #
        # Render both sides?
        self.settings["doubleSide"] = True
        # Render triangles as wireframe?
        self.settings["wireframe"] = False
        # Line thickness for wireframe
        self.settings["lineWidth"] = 1

        self.setProperties(properties) # method from Material class

    def updateRenderSettings(self):

        if self.settings["doubleSide"]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)

        if self.settings["wireframe"]:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glLineWidth(self.settings["lineWidth"])

