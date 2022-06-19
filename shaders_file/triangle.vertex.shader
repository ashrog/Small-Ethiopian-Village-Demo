#version 330 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoord;

out vec2 newTexCoord;
uniform mat4 projection;
uniform mat4 model;
uniform mat4 view;
void main()
{

        // gl_Position = view * model * vec4(position,1);
        gl_Position = projection *view * model * vec4(position,1);
        newTexCoord = texCoord;
}

