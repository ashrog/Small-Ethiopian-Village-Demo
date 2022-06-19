#version 330 core
// in vec2 newTexCoord;
// out vec4 color;
in vec2 newTexCoord;
// out vec4 color;
uniform sampler2D texSampler;

void main()
{
    color = texture(texSampler, newTexCoord);

}
