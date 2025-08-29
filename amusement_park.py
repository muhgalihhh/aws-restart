#!/usr/bin/env python3
"""
3D Amusement Park Simulation
Converted from C++ to Python using PyOpenGL
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import numpy as np
from PIL import Image

# Global variables - Camera and view settings
eyeX, eyeY, eyeZ = -10, 5.0, 100
refX, refY, refZ = 0, 0, 0
windowHeight, windowWidth = 1000, 1000

# Animation variables
alpha = 0.0
theta = 0.0
orbiterAlpha = -45.0
orbiterTheta = 0.0
testTheta = -45.0
pirateBoatTheta = 0.0
cmOrbiterAlpha = 0.0
cmOrbiterTheta = 0.0
skyDropPos = 0.0

# Flags
bRotate = False
uRotate = False
fanSwitch = False
door1 = False
orbiterFlag = False
testFlag = True
pirateBoatFlag = False
pirateBoatCheck = False
cmOrbiterFlag = False
skyDropFlag = False
upFlag = True
downFlag1 = True
downFlag2 = False
downFlag3 = False
show = False
day = True
switchOne = False
switchTwo = False
switchThree = False
switchFour = False

# Flag animation variables
yf = 0
xf = 0
yflag = False
xflag = False

# Texture IDs
ID = None
ID2 = [None] * 40

# Quadric object
quad = None

# Color definitions
colors = [
    [1, 0, 0, 0.5, 0, 0],    # red
    [0, 1, 0, 0, 0.5, 0],    # green
    [0, 0, 1, 0, 0, 0.5],    # blue
    [1, 1, 0, 0.5, 0.5, 0]   # yellow
]

# Cube vertices
v_cube = [
    [0.0, 0.0, 0.0],  # 0
    [0.0, 0.0, 3.0],  # 1
    [3.0, 0.0, 3.0],  # 2
    [3.0, 0.0, 0.0],  # 3
    [0.0, 3.0, 0.0],  # 4
    [0.0, 3.0, 3.0],  # 5
    [3.0, 3.0, 3.0],  # 6
    [3.0, 3.0, 0.0]   # 7
]

# Cube face indices
quadIndices = [
    [0, 1, 2, 3],  # bottom
    [4, 5, 6, 7],  # top
    [5, 1, 2, 6],  # front
    [3, 7, 4, 0],  # back
    [2, 3, 7, 6],  # right
    [0, 4, 5, 1]   # left
]

# Box vertices
v_box = [
    [0.0, 0.0, 0.0],  # 0
    [3.0, 0.0, 0.0],  # 1
    [0.0, 0.0, 3.0],  # 2
    [3.0, 0.0, 3.0],  # 3
    [0.0, 3.0, 0.0],  # 4
    [3.0, 3.0, 0.0],  # 5
    [0.0, 3.0, 3.0],  # 6
    [3.0, 3.0, 3.0]   # 7
]

# Box face indices
BoxquadIndices = [
    [0, 2, 3, 1],
    [0, 2, 6, 4],
    [2, 3, 7, 6],
    [1, 3, 7, 5],
    [1, 5, 4, 0],
    [6, 7, 5, 4]
]

# Pyramid vertices
v_pyramid = [
    [0.0, 0.0, 0.0],
    [0.0, 0.0, 2.0],
    [2.0, 0.0, 2.0],
    [2.0, 0.0, 0.0],
    [1.0, 4.0, 1.0]
]

# Pyramid face indices
p_Indices = [
    [4, 1, 2],
    [4, 2, 3],
    [4, 3, 0],
    [4, 0, 1]
]

PquadIndices = [[0, 3, 2, 1]]

# Trapezoid vertices
v_trapezoid = [
    [0.0, 0.0, 0.0],  # 0
    [0.0, 0.0, 3.0],  # 1
    [3.0, 0.0, 3.0],  # 2
    [3.0, 0.0, 0.0],  # 3
    [0.5, 3.0, 0.5],  # 4
    [0.5, 3.0, 2.5],  # 5
    [2.5, 3.0, 2.5],  # 6
    [2.5, 3.0, 0.5]   # 7
]

# Trapezoid face indices
TquadIndices = [
    [0, 1, 2, 3],  # bottom
    [4, 5, 6, 7],  # top
    [5, 1, 2, 6],  # front
    [3, 7, 4, 0],  # back
    [2, 3, 7, 6],  # right
    [0, 4, 5, 1]   # left
]

# Bezier curve parameters
nt = 60  # number of slices along x-direction
ntheta = 20
PI = 3.14159265389


def LoadTexture2(filename, num):
    """Load texture from file (placeholder - implement based on your texture files)"""
    global ID2
    try:
        # This is a placeholder - you'll need to implement actual texture loading
        # based on your texture file format (.sgi files)
        ID2[num] = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, ID2[num])
        
        # Set texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)
        
        # For now, create a dummy texture
        dummy_data = np.zeros((64, 64, 3), dtype=np.uint8)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 64, 64, 0, GL_RGB, GL_UNSIGNED_BYTE, dummy_data)
    except:
        print(f"Warning: Could not load texture {filename}")


def materialProperty():
    """Set default material properties"""
    glColor3f(1, 1, 1)
    no_mat = [0.0, 0.0, 0.0, 1.0]
    mat_ambient = [1.0, 1.0, 1.0, 1.0]
    mat_diffuse = [1.0, 1.0, 1.0, 1.0]
    mat_specular = [1.0, 1.0, 1.0, 1.0]
    mat_shininess = [60]
    
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glMaterialfv(GL_FRONT, GL_EMISSION, no_mat)


def matCurve(difX, difY, difZ, ambfactor=1.0, specfactor=1.0, shine=50):
    """Set material properties for curves"""
    glColor3f(1, 1, 1)
    no_mat = [0.0, 0.0, 0.0, 1.0]
    mat_ambient = [difX*ambfactor, difY*ambfactor, difZ*ambfactor, 1.0]
    mat_diffuse = [difX, difY, difZ, 1.0]
    mat_specular = [1.0, 1.0, 1.0, 1.0]
    mat_shininess = [60]
    
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glMaterialfv(GL_FRONT, GL_EMISSION, no_mat)


def getNormal3p(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    """Calculate normal vector for three points"""
    Ux = x2 - x1
    Uy = y2 - y1
    Uz = z2 - z1
    
    Vx = x3 - x1
    Vy = y3 - y1
    Vz = z3 - z1
    
    Nx = Uy * Vz - Uz * Vy
    Ny = Uz * Vx - Ux * Vz
    Nz = Ux * Vy - Uy * Vx
    
    glNormal3f(Nx, Ny, Nz)


def drawCube1(difX, difY, difZ, ambX=0, ambY=0, ambZ=0, shine=50):
    """Draw a cube with specified material properties"""
    no_mat = [0.0, 0.0, 0.0, 1.0]
    mat_ambient = [ambX, ambY, ambZ, 1.0]
    mat_diffuse = [difX, difY, difZ, 1.0]
    mat_specular = [1.0, 1.0, 1.0, 1.0]
    mat_shininess = [shine]
    
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glMaterialfv(GL_FRONT, GL_EMISSION, no_mat)
    
    glBegin(GL_QUADS)
    for i in range(6):
        getNormal3p(v_cube[quadIndices[i][0]][0], v_cube[quadIndices[i][0]][1], v_cube[quadIndices[i][0]][2],
                    v_cube[quadIndices[i][1]][0], v_cube[quadIndices[i][1]][1], v_cube[quadIndices[i][1]][2],
                    v_cube[quadIndices[i][2]][0], v_cube[quadIndices[i][2]][1], v_cube[quadIndices[i][2]][2])
        glVertex3fv(v_cube[quadIndices[i][0]])
        glVertex3fv(v_cube[quadIndices[i][1]])
        glVertex3fv(v_cube[quadIndices[i][2]])
        glVertex3fv(v_cube[quadIndices[i][3]])
    glEnd()


def drawSphere(difX, difY, difZ, ambX, ambY, ambZ, shine=90):
    """Draw a sphere with specified material properties"""
    no_mat = [0.0, 0.0, 0.0, 1.0]
    mat_ambient = [ambX, ambY, ambZ, 1.0]
    mat_diffuse = [difX, difY, difZ, 1.0]
    mat_specular = [1.0, 1.0, 1.0, 1.0]
    mat_shininess = [shine]
    
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glMaterialfv(GL_FRONT, GL_EMISSION, no_mat)
    
    glutSolidSphere(1.0, 16, 16)


def drawTorus(difX, difY, difZ, ambX, ambY, ambZ, innerRadius, outerRadius, nsides, rings, shine=90):
    """Draw a torus with specified material properties"""
    no_mat = [0.0, 0.0, 0.0, 1.0]
    mat_ambient = [ambX, ambY, ambZ, 1.0]
    mat_diffuse = [difX, difY, difZ, 1.0]
    mat_specular = [1.0, 1.0, 1.0, 1.0]
    mat_shininess = [shine]
    
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glMaterialfv(GL_FRONT, GL_EMISSION, no_mat)
    
    glutSolidTorus(innerRadius, outerRadius, nsides, rings)


def drawCylinder(difX, difY, difZ, ambX, ambY, ambZ, shine=90):
    """Draw a cylinder with specified material properties"""
    no_mat = [0.0, 0.0, 0.0, 1.0]
    mat_ambient = [ambX, ambY, ambZ, 1.0]
    mat_diffuse = [difX, difY, difZ, 1.0]
    mat_specular = [1.0, 1.0, 1.0, 1.0]
    mat_shininess = [shine]
    
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glMaterialfv(GL_FRONT, GL_EMISSION, no_mat)
    
    quadratic = gluNewQuadric()
    gluCylinder(quadratic, 1.5, 1.5, 19, 32, 32)


def drawBox():
    """Draw a textured box"""
    materialProperty()
    glBegin(GL_QUADS)
    for i in range(6):
        getNormal3p(v_box[BoxquadIndices[i][0]][0], v_box[BoxquadIndices[i][0]][1], v_box[BoxquadIndices[i][0]][2],
                    v_box[BoxquadIndices[i][1]][0], v_box[BoxquadIndices[i][1]][1], v_box[BoxquadIndices[i][1]][2],
                    v_box[BoxquadIndices[i][2]][0], v_box[BoxquadIndices[i][2]][1], v_box[BoxquadIndices[i][2]][2])
        
        glVertex3fv(v_box[BoxquadIndices[i][0]])
        glTexCoord2f(1, 1)
        glVertex3fv(v_box[BoxquadIndices[i][1]])
        glTexCoord2f(1, 0)
        glVertex3fv(v_box[BoxquadIndices[i][2]])
        glTexCoord2f(0, 0)
        glVertex3fv(v_box[BoxquadIndices[i][3]])
        glTexCoord2f(0, 1)
    glEnd()


def drawpyramid(difX, difY, difZ, ambX, ambY, ambZ, shine):
    """Draw a pyramid with specified material properties"""
    no_mat = [0.0, 0.0, 0.0, 1.0]
    mat_ambient = [ambX, ambY, ambZ, 1.0]
    mat_diffuse = [difX, difY, difZ, 1.0]
    mat_specular = [1.0, 1.0, 1.0, 1.0]
    mat_shininess = [shine]
    
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glMaterialfv(GL_FRONT, GL_EMISSION, no_mat)
    
    glBegin(GL_TRIANGLES)
    for i in range(4):
        getNormal3p(v_pyramid[p_Indices[i][0]][0], v_pyramid[p_Indices[i][0]][1], v_pyramid[p_Indices[i][0]][2],
                    v_pyramid[p_Indices[i][1]][0], v_pyramid[p_Indices[i][1]][1], v_pyramid[p_Indices[i][1]][2],
                    v_pyramid[p_Indices[i][2]][0], v_pyramid[p_Indices[i][2]][1], v_pyramid[p_Indices[i][2]][2])
        glVertex3fv(v_pyramid[p_Indices[i][0]])
        glVertex3fv(v_pyramid[p_Indices[i][1]])
        glVertex3fv(v_pyramid[p_Indices[i][2]])
    glEnd()
    
    glBegin(GL_QUADS)
    for i in range(1):
        getNormal3p(v_pyramid[PquadIndices[i][0]][0], v_pyramid[PquadIndices[i][0]][1], v_pyramid[PquadIndices[i][0]][2],
                    v_pyramid[PquadIndices[i][1]][0], v_pyramid[PquadIndices[i][1]][1], v_pyramid[PquadIndices[i][1]][2],
                    v_pyramid[PquadIndices[i][2]][0], v_pyramid[PquadIndices[i][2]][1], v_pyramid[PquadIndices[i][2]][2])
        glVertex3fv(v_pyramid[PquadIndices[i][0]])
        glVertex3fv(v_pyramid[PquadIndices[i][1]])
        glVertex3fv(v_pyramid[PquadIndices[i][2]])
        glVertex3fv(v_pyramid[PquadIndices[i][3]])
    glEnd()


def drawTrapezoid(difX, difY, difZ, ambX, ambY, ambZ, shine=50):
    """Draw a trapezoid with specified material properties"""
    no_mat = [0.0, 0.0, 0.0, 1.0]
    mat_ambient = [ambX, ambY, ambZ, 1.0]
    mat_diffuse = [difX, difY, difZ, 1.0]
    mat_specular = [1.0, 1.0, 1.0, 1.0]
    mat_shininess = [shine]
    
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glMaterialfv(GL_FRONT, GL_EMISSION, no_mat)
    
    glBegin(GL_QUADS)
    for i in range(6):
        getNormal3p(v_trapezoid[TquadIndices[i][0]][0], v_trapezoid[TquadIndices[i][0]][1], v_trapezoid[TquadIndices[i][0]][2],
                    v_trapezoid[TquadIndices[i][1]][0], v_trapezoid[TquadIndices[i][1]][1], v_trapezoid[TquadIndices[i][1]][2],
                    v_trapezoid[TquadIndices[i][2]][0], v_trapezoid[TquadIndices[i][2]][1], v_trapezoid[TquadIndices[i][2]][2])
        
        glVertex3fv(v_trapezoid[TquadIndices[i][0]])
        glVertex3fv(v_trapezoid[TquadIndices[i][1]])
        glVertex3fv(v_trapezoid[TquadIndices[i][2]])
        glVertex3fv(v_trapezoid[TquadIndices[i][3]])
    glEnd()


def light():
    """Set up the main light source"""
    no_light = [0.0, 0.0, 0.0, 1.0]
    light_ambient = [1.0, 1.0, 1.0, 1.0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]
    light_position = [20.0, 50.0, 0.0, 1.0]
    
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)


def sky(x, y, z, width, height, length):
    """Draw the skybox"""
    materialProperty()
    glDisable(GL_DEPTH_TEST)
    x = x - width / 2
    y = y - height / 2
    z = z - length / 2
    
    # Front
    glEnable(GL_TEXTURE_2D)
    if day:
        glBindTexture(GL_TEXTURE_2D, ID2[8])
    else:
        glBindTexture(GL_TEXTURE_2D, ID2[28])
    
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x+width, y, z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x+width, y, z+length)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x+width, y+height, z+length)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x+width, y+height, z)
    glEnd()
    
    # Up
    if day:
        glBindTexture(GL_TEXTURE_2D, ID2[27])
    else:
        glBindTexture(GL_TEXTURE_2D, ID2[28])
    
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x+width, y+height, z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x+width, y+height, z+length)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x, y+height, z+length)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, y+height, z)
    glEnd()
    
    # Back
    if day:
        glBindTexture(GL_TEXTURE_2D, ID2[9])
    else:
        glBindTexture(GL_TEXTURE_2D, ID2[28])
    
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x, y+height, z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, y+height, z+length)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, y, z+length)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x, y, z)
    glEnd()
    
    # Right
    if day:
        glBindTexture(GL_TEXTURE_2D, ID2[10])
    else:
        glBindTexture(GL_TEXTURE_2D, ID2[28])
    
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x+width, y, z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x+width, y+height, z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, y+height, z)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, y, z)
    glEnd()
    
    # Left
    if day:
        glBindTexture(GL_TEXTURE_2D, ID2[11])
    else:
        glBindTexture(GL_TEXTURE_2D, ID2[28])
    
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x, y, z+length)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x, y+height, z+length)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x+width, y+height, z+length)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x+width, y, z+length)
    glEnd()
    
    glDisable(GL_TEXTURE_2D)


def ground():
    """Draw the ground"""
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, ID2[14])
    glPushMatrix()
    materialProperty()
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(150, -20, 150)
    glTexCoord2f(5.0, 0.0)
    glVertex3f(150, -20, -150)
    glTexCoord2f(5.0, 5.0)
    glVertex3f(-100, -20, -100)
    glTexCoord2f(0.0, 5.0)
    glVertex3f(-100, -20, 100)
    glEnd()
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)


def ground2():
    """Draw secondary ground texture"""
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, ID2[2])
    glPushMatrix()
    materialProperty()
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(10, -19.8, 10)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(10, -19.8, -10)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-10, -19.8, -10)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-10, -19.8, 10)
    glEnd()
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)


def ferrisWheelSeat():
    """Draw a single ferris wheel seat"""
    # Seat
    glPushMatrix()
    glTranslatef(0, -0.5, 0)
    glScalef(0.5, 0.2, 1.5)
    drawCube1(0.804, 0.361, 0.361, 0.403, 0.1805, 0.1805)
    glPopMatrix()
    
    # Seat belt rod
    glPushMatrix()
    glTranslatef(1.3, 0.7, 0)
    glScalef(0.02, 0.02, 1.5)
    drawCube1(0, 0, 0, 0, 0, 0.0)
    glPopMatrix()
    
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, ID2[4])
    
    # Back
    glPushMatrix()
    glScalef(0.2, 0.5, 1.5)
    drawBox()
    glPopMatrix()
    
    # Seat right side
    glPushMatrix()
    glScalef(0.5, 0.5, 0.02)
    drawBox()
    glPopMatrix()
    
    # Seat left side
    glPushMatrix()
    glTranslatef(0, 0, 4.445)
    glScalef(0.5, 0.5, 0.02)
    drawBox()
    glPopMatrix()
    
    # Bottom bent part
    glPushMatrix()
    glTranslatef(1.48, -0.5, 0)
    glRotatef(-45, 0, 0, 1)
    glScalef(0.15, 0.02, 1.5)
    drawBox()
    glPopMatrix()
    
    # Bottom straight part
    glPushMatrix()
    glTranslatef(1.8, -0.8, 0)
    glScalef(0.16, 0.02, 1.5)
    drawBox()
    glPopMatrix()
    
    # Bottom farthest part
    glPushMatrix()
    glTranslatef(2.25, -0.8, 0)
    glScalef(0.02, 0.1, 1.5)
    drawBox()
    glPopMatrix()
    
    glDisable(GL_TEXTURE_2D)


def wheel():
    """Draw the ferris wheel structure"""
    glPushMatrix()
    glScalef(1, 1, 2)
    drawSphere(1, 0, 0, 0.5, 0, 0)
    glPopMatrix()
    
    glPushMatrix()
    drawTorus(1, 1, 0.3, 0.5, 0.5, 0.15, 0.5, 10.0, 32, 64)
    glPopMatrix()
    
    # The big lines
    for i in range(0, 180, 30):
        glPushMatrix()
        glRotatef(i, 0, 0, 1)
        glScalef(6.6, 0.1, 0.5)
        glTranslatef(-1.5, -1.5, -1.5)
        drawCube1(0.867, 0.627, 0.867, 0.4335, 0.3135, 0.4335, 100)
        glPopMatrix()


def bulbsOnFerrisWheel():
    """Draw decorative bulbs on the ferris wheel"""
    for i in range(0, 361, 45):
        glPushMatrix()
        glRotatef(i, 0, 0, 1)
        glTranslatef(10, 0, 0)
        glScalef(0.5, 0.5, 0.5)
        drawSphere(1, 1, 1, 0.5, 0.5, 0.5)
        glPopMatrix()
    
    for i in range(15, 361, 45):
        glPushMatrix()
        glRotatef(i, 0, 0, 1)
        glTranslatef(10, 0, 0)
        glScalef(0.5, 0.5, 0.5)
        drawSphere(1, 0, 0, 0.5, 0, 0)
        glPopMatrix()
    
    for i in range(30, 361, 45):
        glPushMatrix()
        glRotatef(i, 0, 0, 1)
        glTranslatef(10, 0, 0)
        glScalef(0.5, 0.5, 0.5)
        drawSphere(0, 0, 1, 0, 0, 0.5)
        glPopMatrix()


def ferrisWheel():
    """Draw the complete ferris wheel ride"""
    global theta, alpha
    
    # Right stand on the back
    glPushMatrix()
    glTranslatef(-.2, 0, -1)
    glRotatef(-75, 0, 0, 1)
    glScalef(7, 0.28, 0.1)
    drawCube1(0.545, 0.000, 0.545, 0.2725, 0.0, 0.2725)
    glPopMatrix()
    
    # Left stand on the back
    glPushMatrix()
    glTranslatef(-0.6, 0, -1)
    glRotatef(-105, 0, 0, 1)
    glScalef(7, 0.28, 0.1)
    drawCube1(0.545, 0.000, 0.545, 0.2725, 0.0, 0.2725)
    glPopMatrix()
    
    # Right stand on the front
    glPushMatrix()
    glTranslatef(-.2, 0, 6)
    glRotatef(-75, 0, 0, 1)
    glScalef(7, 0.28, 0.1)
    drawCube1(0.545, 0.000, 0.545, 0.2725, 0.0, 0.2725)
    glPopMatrix()
    
    # Left stand on the front
    glPushMatrix()
    glTranslatef(-0.6, 0, 6)
    glRotatef(-105, 0, 0, 1)
    glScalef(7, 0.28, 0.1)
    drawCube1(0.545, 0.000, 0.545, 0.2725, 0.0, 0.2725)
    glPopMatrix()
    
    # Base stand
    glPushMatrix()
    glTranslatef(0, -19.5, 2.5)
    glScalef(4, 0.5, 3)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.545, 0.271, 0.075, 0.2725, 0.1355, 0.0375)
    glPopMatrix()
    
    # Fence in the front
    for j in range(-9, 20, 2):
        glPushMatrix()
        glTranslatef(j, -19.5, 11)
        glScalef(0.1, 2.5, 0.1)
        glTranslatef(-1.5, -1.5, -1.5)
        drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(j, -16.1, 11)
        glScalef(.4, .4, .4)
        drawSphere(0.855, 0.439, 0.839, 0.4275, 0.2195, 0.4195)
        glPopMatrix()
    
    # The horizontal lines of the front fence
    glPushMatrix()
    glTranslatef(4, -17, 11)
    glScalef(10, 0.05, 0.1)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(4, -18, 11)
    glScalef(10, 0.05, 0.1)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(4, -19, 11)
    glScalef(10, 0.05, 0.1)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    # Gate
    glPushMatrix()
    glTranslatef(-15, -20, 11)
    glRotatef(-alpha, 0, 1, 0)
    for j in range(0, 5, 2):
        glPushMatrix()
        glTranslatef(j, 0, 0)
        glScalef(0.1, 1.5, 0.1)
        drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(j, 4.4, 0.2)
        glScalef(.4, .4, .4)
        drawSphere(0.855, 0.439, 0.839, 0.4275, 0.2195, 0.4195)
        glPopMatrix()
    
    for j in range(1, 4):
        glPushMatrix()
        glTranslatef(0, j, 0)
        glScalef(1.5, 0.05, 0.1)
        drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
        glPopMatrix()
    glPopMatrix()
    
    # Fence in the back
    for j in range(-15, 20, 2):
        glPushMatrix()
        glTranslatef(j, -19.5, -5)
        glScalef(0.1, 2.5, 0.1)
        glTranslatef(-1.5, -1.5, -1.5)
        drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(j, -16.1, -5)
        glScalef(.4, .4, .4)
        drawSphere(0.855, 0.439, 0.839, 0.4275, 0.2195, 0.4195)
        glPopMatrix()
    
    glPushMatrix()
    glTranslatef(2, -17, -5)
    glScalef(11.5, 0.05, 0.1)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(2, -18, -5)
    glScalef(11.5, 0.05, 0.1)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(2, -19, -5)
    glScalef(11.5, 0.05, 0.1)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    # Fence in the left
    for j in range(-3, 10, 2):
        glPushMatrix()
        glTranslatef(-15, -19.5, j)
        glScalef(0.1, 2.5, 0.1)
        glTranslatef(-1.5, -1.5, -1.5)
        drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(-15, -16.1, j)
        glScalef(.4, .4, .4)
        drawSphere(0.855, 0.439, 0.839, 0.4275, 0.2195, 0.4195)
        glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-15, -17, 3)
    glScalef(.1, 0.05, 5.5)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-15, -18, 3)
    glScalef(.1, 0.05, 5.5)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-15, -19, 3)
    glScalef(.1, 0.05, 5.5)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    # Fence in the right
    for j in range(-3, 10, 2):
        glPushMatrix()
        glTranslatef(19, -19.5, j)
        glScalef(0.1, 2.5, 0.1)
        glTranslatef(-1.5, -1.5, -1.5)
        drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(19, -16.1, j)
        glScalef(.4, .4, .4)
        drawSphere(0.855, 0.439, 0.839, 0.4275, 0.2195, 0.4195)
        glPopMatrix()
    
    glPushMatrix()
    glTranslatef(19, -17, 3)
    glScalef(.1, 0.05, 5.5)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(19, -18, 3)
    glScalef(.1, 0.05, 5.5)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(19, -19, 3)
    glScalef(.1, 0.05, 5.5)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    # Rotating part
    glPushMatrix()
    glRotatef(-theta, 0, 0, 1)
    glScalef(1.5, 1.5, 1)
    wheel()
    glPushMatrix()
    glTranslatef(0, 0, 5)
    wheel()
    glPopMatrix()
    
    # Bulbs
    glPushMatrix()
    glTranslatef(0, 0, 5.5)
    bulbsOnFerrisWheel()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 0, -0.5)
    bulbsOnFerrisWheel()
    glPopMatrix()
    
    # The middle line between two spheres
    glPushMatrix()
    glScalef(0.1, 0.05, 1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    # The smaller lines in between
    for j in range(0, 361, 30):
        glPushMatrix()
        glRotatef(j, 0, 0, 1)
        for i in range(1, 8):
            glPushMatrix()
            glTranslatef(i, 0, 0)
            glScalef(0.1, 0.05, 1.5)
            drawCube1(0.780, 0.082, 0.522, 0.39, 0.041, 0.261)
            glPopMatrix()
        glPopMatrix()
    
    # The seats
    for i in range(0, 360, 30):
        glPushMatrix()
        glRotatef(i, 0, 0, 1)
        glTranslatef(10, 0, 0.9)
        glRotatef(-i, 0, 0, 1)
        glRotatef(theta, 0, 0, 1)
        glScalef(1, 1, 0.8)
        ferrisWheelSeat()
        glPopMatrix()
    
    glPopMatrix()
    
    # Ground
    glPushMatrix()
    glTranslatef(2, 0, 0)
    glScalef(2, 1, 1.5)
    ground2()
    glPopMatrix()


def bush():
    """Draw a bush"""
    global quad
    quad = gluNewQuadric()
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, ID2[24])
    
    glPushMatrix()
    gluQuadricTexture(quad, 1)
    gluSphere(quad, 1, 100, 100)
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)


def tree():
    """Draw a tree"""
    global quad
    quad = gluNewQuadric()
    glEnable(GL_TEXTURE_2D)
    
    glBindTexture(GL_TEXTURE_2D, ID2[30])
    
    glPushMatrix()
    glScalef(1, 2, 1)
    gluQuadricTexture(quad, 1)
    gluSphere(quad, 4, 100, 100)
    glPopMatrix()
    
    glBindTexture(GL_TEXTURE_2D, ID2[29])
    glPushMatrix()
    glTranslatef(0, -7, 0)
    glRotatef(90, 1, 0, 0)
    gluQuadricTexture(quad, 1)
    gluCylinder(quad, 1, 1, 10, 32, 32)
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)


def rings():
    """Draw decorative rings"""
    for i in np.arange(-3.5, -17.5, -1):
        glPushMatrix()
        glTranslatef(0, i, 0)
        glRotatef(90, 1, 0, 0)
        glScalef(0.2, 0.2, 0.2)
        drawTorus(1, 0, 0, 0.5, 0, 0, 1.5, 7.5, 32, 64)
        glPopMatrix()
    
    for i in np.arange(-3, -17, -1):
        glPushMatrix()
        glTranslatef(0, i, 0)
        glRotatef(90, 1, 0, 0)
        glScalef(0.2, 0.2, 0.2)
        drawTorus(1, 1, 1, 0.5, 0.5, 0.5, 1.5, 7.5, 32, 64)
        glPopMatrix()


def orbiter():
    """Draw the orbiter ride"""
    global orbiterAlpha, orbiterTheta, alpha
    
    glPushMatrix()
    glScalef(2, 1, 2)
    ground2()
    glPopMatrix()
    
    # The 1st torus at the bottom
    rings()
    
    glPushMatrix()
    glTranslatef(0, -18, 0)
    glRotatef(90, 1, 0, 0)
    glScalef(0.2, 0.2, 0.2)
    drawTorus(1, 1, 1, 0.5, 0.5, 0.5, 2, 8, 32, 64)
    glPopMatrix()
    
    # The 2nd torus at the bottom
    glPushMatrix()
    glTranslatef(0, -18.5, 0)
    glRotatef(90, 1, 0, 0)
    glScalef(0.2, 0.2, 0.2)
    drawTorus(1, 0, 0, 0.5, 0, 0, 2, 10, 32, 64)
    glPopMatrix()
    
    # The sphere
    glPushMatrix()
    glTranslatef(0, -1, 0)
    glScalef(2.5, 2.5, 2.5)
    drawSphere(1, 0, 0, 0.5, 0, 0)
    glPopMatrix()
    
    # Fence in the front
    for j in range(-10, 17, 2):
        glPushMatrix()
        glTranslatef(j, -19.5, 17)
        glScalef(0.1, 2.5, 0.1)
        glTranslatef(-1.5, -1.5, -1.5)
        drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(j, -16.1, 17)
        glScalef(.4, .4, .4)
        drawSphere(0.855, 0.439, 0.839, 0.4275, 0.2195, 0.4195)
        glPopMatrix()
    
    # The horizontal lines of the front fence
    glPushMatrix()
    glTranslatef(2.5, -17, 17)
    glScalef(9, 0.05, 0.1)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(2.5, -18, 17)
    glScalef(9, 0.05, 0.1)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(2.5, -19, 17)
    glScalef(9, 0.05, 0.1)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    # Gate
    glPushMatrix()
    glTranslatef(-15.5, -20, 17)
    glRotatef(-alpha, 0, 1, 0)
    for j in range(0, 5, 2):
        glPushMatrix()
        glTranslatef(j, 0, 0)
        glScalef(0.1, 1.5, 0.1)
        drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(j, 4.4, 0.2)
        glScalef(.4, .4, .4)
        drawSphere(0.855, 0.439, 0.839, 0.4275, 0.2195, 0.4195)
        glPopMatrix()
    
    for j in range(1, 4):
        glPushMatrix()
        glTranslatef(0, j, 0)
        glScalef(1.5, 0.05, 0.1)
        drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
        glPopMatrix()
    glPopMatrix()
    
    # Fence in the back
    for j in range(-14, 17, 2):
        glPushMatrix()
        glTranslatef(j, -19.5, -17)
        glScalef(0.1, 2.5, 0.1)
        glTranslatef(-1.5, -1.5, -1.5)
        drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(j, -16.1, -17)
        glScalef(.4, .4, .4)
        drawSphere(0.855, 0.439, 0.839, 0.4275, 0.2195, 0.4195)
        glPopMatrix()
    
    # The horizontal lines of the back fence
    glPushMatrix()
    glTranslatef(0, -17, -17)
    glScalef(10.5, 0.05, 0.1)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, -18, -17)
    glScalef(10.5, 0.05, 0.1)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, -19, -17)
    glScalef(10.5, 0.05, 0.1)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    # Fence in the right
    for j in range(-17, 16, 2):
        glPushMatrix()
        glTranslatef(16, -19.5, j)
        glScalef(0.1, 2.5, 0.1)
        glTranslatef(-1.5, -1.5, -1.5)
        drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(16, -16.1, j)
        glScalef(.4, .4, .4)
        drawSphere(0.855, 0.439, 0.839, 0.4275, 0.2195, 0.4195)
        glPopMatrix()
    
    # The horizontal lines
    glPushMatrix()
    glTranslatef(16, -17, 0)
    glScalef(.1, 0.05, 11.5)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(16, -18, 0)
    glScalef(.1, 0.05, 11.5)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(16, -19, 0)
    glScalef(.1, 0.05, 11.5)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    # Fence in the left
    for j in range(-17, 18, 2):
        glPushMatrix()
        glTranslatef(-16, -19.5, j)
        glScalef(0.1, 2.5, 0.1)
        glTranslatef(-1.5, -1.5, -1.5)
        drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(-16, -16.1, j)
        glScalef(.4, .4, .4)
        drawSphere(0.855, 0.439, 0.839, 0.4275, 0.2195, 0.4195)
        glPopMatrix()
    
    # The horizontal lines
    glPushMatrix()
    glTranslatef(-16, -17, 0)
    glScalef(.1, 0.05, 11.5)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-16, -18, 0)
    glScalef(.1, 0.05, 11.5)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-16, -19, 0)
    glScalef(.1, 0.05, 11.5)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    # Translating the rotating part down
    glPushMatrix()
    glTranslatef(0, -5, 0)
    
    # Rotating part
    glPushMatrix()
    glRotatef(orbiterTheta, 0, 1, 0)
    # Seat
    for i in range(0, 361, 45):
        glPushMatrix()
        glRotatef(i, 0, 1, 0)
        
        glPushMatrix()
        glRotatef(orbiterAlpha, 0, 0, 1)
        glRotatef(0, 0, 1, 0)
        glTranslatef(15, 0, -2)
        glRotatef(-0, 0, 1, 0)
        glRotatef(-orbiterAlpha, 0, 0, 1)
        ferrisWheelSeat()
        glPopMatrix()
        
        glPushMatrix()
        glRotatef(orbiterAlpha, 0, 0, 1)
        glScalef(5.1, 0.2, 0.2)
        drawCube1(0, 0, 1, 0, 0, 0.5)
        glPopMatrix()
        
        glPopMatrix()
    
    glPopMatrix()
    
    glPopMatrix()


def boatBody():
    """Draw the pirate boat body"""
    glPushMatrix()
    glTranslatef(-1.3, 0, 0)
    glScalef(3.7, 0.1, 1)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.412, 0.412, 0.412, 0.0, 0.0, 0.0)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 1.5, 1.5)
    glScalef(5.5, 1, 0.1)
    glRotatef(180, 0, 0, 1)
    glTranslatef(-1.25, -1.5, -1.25)
    drawTrapezoid(0.412, 0.412, 0.412, 0.0, 0.0, 0.0)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 1.5, -1.5)
    glScalef(5.5, 1, 0.1)
    glRotatef(180, 0, 0, 1)
    glTranslatef(-1.25, -1.5, -1.25)
    drawTrapezoid(0.412, 0.412, 0.412, 0.0, 0.0, 0.0)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(5.5, 1.5, 0)
    glRotatef(-42, 0, 0, 1)
    glScalef(0.1, 1.3, 1)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.412, 0.412, 0.412, 0.0, 0.0, 0.0)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-8.1, 1.5, 0)
    glRotatef(42, 0, 0, 1)
    glScalef(0.1, 1.3, 1)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.412, 0.412, 0.412, 0.0, 0.0, 0.0)
    glPopMatrix()
    
    for i in range(-6, 3, 2):
        glPushMatrix()
        glTranslatef(i, 0, -1.5)
        glScalef(0.1, 1, 1)
        drawCube1(0.412, 0.412, 0.412, 0.0, 0.0, 0.0)
        glPopMatrix()
    
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, ID2[3])
    glPushMatrix()
    glTranslatef(-6.9, 0, 1.7)
    glScalef(3.7, 1, 0.01)
    drawBox()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-6.9, 0, -1.7)
    glScalef(3.7, 1, 0.01)
    drawBox()
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)


def pirateBoat():
    """Draw the pirate boat ride"""
    global pirateBoatTheta
    
    glPushMatrix()
    glTranslatef(1, 0, 0)
    glScalef(1.3, 1, 1.3)
    ground2()
    glPopMatrix()
    
    # Base stand
    glPushMatrix()
    glTranslatef(0.5, -19.5, 0)
    glScalef(6, 0.5, 4)
    glTranslatef(-1.5, -1.5, -1.5)
    drawCube1(0.545, 0.271, 0.075, 0.2725, 0.1355, 0.0375)
    glPopMatrix()
    
    # Translate down
    glPushMatrix()
    glTranslatef(0, -5.5, 0)
    
    glPushMatrix()
    glTranslatef(0, 0, -4)
    glScalef(0.2, 0.2, 0.5)
    drawCylinder(1, 0, 0, 0.5, 0, 0.5)
    glPopMatrix()
    
    # Boat body
    glPushMatrix()
    glRotatef(pirateBoatTheta, 0, 0, 1)
    glTranslatef(1.5, -12, 0)
    boatBody()
    glPopMatrix()
    
    # Stand on the front
    glPushMatrix()
    glTranslatef(0, 0, 1.4)
    glRotatef(pirateBoatTheta, 0, 0, 1)
    drawSphere(0, 0, 1, 0, 0, 0.5)
    # Left stand
    glPushMatrix()
    glRotatef(-55, 0, 0, 1)
    glScalef(4, 0.28, 0.1)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    # Right stand
    glPushMatrix()
    glRotatef(-125, 0, 0, 1)
    glScalef(4, 0.28, 0.1)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    glPopMatrix()
    
    # Stand on the back
    glPushMatrix()
    glTranslatef(0, 0, -1.6)
    glRotatef(pirateBoatTheta, 0, 0, 1)
    drawSphere(0, 0, 1, 0, 0, 0.5)
    # Left stand
    glPushMatrix()
    glRotatef(-55, 0, 0, 1)
    glScalef(4, 0.28, 0.1)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    # Right stand
    glPushMatrix()
    glRotatef(-125, 0, 0, 1)
    glScalef(4, 0.28, 0.1)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    glPopMatrix()
    
    # Base stand at the front
    glPushMatrix()
    glTranslatef(0, 0, 5)
    drawSphere(0, 0, 1, 0, 0, 0.5)
    # Left stand
    glPushMatrix()
    glRotatef(-60, 0, 0, 1)
    glScalef(6, 0.28, 0.1)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    # Right stand
    glPushMatrix()
    glRotatef(-120, 0, 0, 1)
    glScalef(6, 0.28, 0.1)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.055)
    glPopMatrix()
    glPopMatrix()
    
    # Base stand at the back
    glPushMatrix()
    glTranslatef(0, 0, -5)
    drawSphere(0, 0, 1, 0, 0, 0.5)
    # Left stand
    glPushMatrix()
    glRotatef(-60, 0, 0, 1)
    glScalef(6, 0.28, 0.1)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    
    # Right stand
    glPushMatrix()
    glRotatef(-120, 0, 0, 1)
    glScalef(6, 0.28, 0.1)
    drawCube1(0.2, 0.1, 0.1, 0.1, 0.05, 0.05)
    glPopMatrix()
    glPopMatrix()
    
    glPopMatrix()


def chair():
    """Draw a chair"""
    # Seat part
    glPushMatrix()
    glScalef(0.5, 0.05, 0.5)
    drawCube1(0.8, 0.2, 0.4, 0.4, 0.1, 0.2)
    glPopMatrix()
    
    # Seat left back
    glPushMatrix()
    glTranslatef(0, -1.5, 0)
    glScalef(0.05, 1.4, 0.05)
    drawCube1(0.8, 0.2, 0.4, 0.4, 0.1, 0.2)
    glPopMatrix()
    
    # Seat right back
    glPushMatrix()
    glTranslatef(1.35, -1.5, 0)
    glScalef(0.05, 1.4, 0.05)
    drawCube1(0.8, 0.2, 0.4, 0.4, 0.1, 0.2)
    glPopMatrix()
    
    # Seat horizontal up back
    glPushMatrix()
    glTranslatef(0, 2, 0)
    glScalef(0.5, 0.05, 0.05)
    drawCube1(0.8, 0.2, 0.4, 0.4, 0.1, 0.2)
    glPopMatrix()
    
    # Seat horizontal up back
    glPushMatrix()
    glTranslatef(0, 1.5, 0)
    glScalef(0.5, 0.05, 0.05)
    drawCube1(0.8, 0.2, 0.4, 0.4, 0.1, 0.2)
    glPopMatrix()
    
    # Seat horizontal up back
    glPushMatrix()
    glTranslatef(0, 1, 0)
    glScalef(0.5, 0.05, 0.05)
    drawCube1(0.8, 0.2, 0.4, 0.4, 0.1, 0.2)
    glPopMatrix()
    
    # Seat left front leg
    glPushMatrix()
    glTranslatef(0, -1.5, 1.3)
    glScalef(0.05, .55, 0.05)
    drawCube1(0.8, 0.2, 0.4, 0.4, 0.1, 0.2)
    glPopMatrix()
    
    # Seat right front leg
    glPushMatrix()
    glTranslatef(1.35, -1.5, 1.3)
    glScalef(0.05, .55, 0.05)
    drawCube1(0.8, 0.2, 0.4, 0.4, 0.1, 0.2)
    glPopMatrix()


def table():
    """Draw a table"""
    # Table
    glPushMatrix()
    glScalef(4, 0.3, 4)
    drawSphere(0.8, 0.4, 0.00, 0.4, 0.2, 0)
    glPopMatrix()
    
    # Stand
    glPushMatrix()
    glScalef(0.1, -1, -0.1)
    drawCube1(0, 0, 0, 0, 0, 0.5)
    glPopMatrix()
    
    # Stand bottom
    glPushMatrix()
    glTranslatef(0, -2.8, 0)
    glScalef(1, 0.2, 1)
    drawSphere(1, 0.549, 0.00, 0.5, 0.2745, 0)
    glPopMatrix()


def diningSet():
    """Draw a dining set with table and chairs"""
    glPushMatrix()
    glTranslatef(0, -16, 0)
    table()
    glPopMatrix()
    
    for i in range(0, 361, 72):
        glPushMatrix()
        glRotatef(i, 0, 1, 0)
        glTranslatef(0, -17, -4)
        chair()
        glPopMatrix()


def quad1():
    """Draw a quad for building walls"""
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(10, 4, 3)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, 4, 3)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 3)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(10, 0, 3)
    glEnd()


def quad2():
    """Draw a quad for building walls"""
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(0, 8, 5)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, 8, 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(0, 0, 5)
    glEnd()


def icecreamParlor():
    """Draw an ice cream parlor building"""
    materialProperty()
    glEnable(GL_TEXTURE_2D)
    
    glBindTexture(GL_TEXTURE_2D, ID2[16])
    glPushMatrix()
    quad1()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 11, -2)
    glRotatef(90, 1, 0, 0)
    glScalef(1, 1.5, 1)
    quad1()
    glPopMatrix()
    
    glBindTexture(GL_TEXTURE_2D, ID2[17])
    glPushMatrix()
    glTranslatef(0, 0, -5)
    glScalef(1, 2, 1)
    quad1()
    glPopMatrix()
    
    glBindTexture(GL_TEXTURE_2D, ID2[18])
    
    glPushMatrix()
    glTranslatef(0, 0, -2)
    quad2()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(10, 0, -2)
    quad2()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 3, -2)
    glRotatef(90, 1, 0, 0)
    quad1()
    glPopMatrix()
    
    glBindTexture(GL_TEXTURE_2D, ID2[5])
    glPushMatrix()
    glTranslatef(0, 6, 1)
    glScalef(1, 0.5, 1)
    quad1()
    glPopMatrix()
    
    glDisable(GL_TEXTURE_2D)


def pizzaHut():
    """Draw a Pizza Hut building"""
    materialProperty()
    glEnable(GL_TEXTURE_2D)
    
    glBindTexture(GL_TEXTURE_2D, ID2[15])
    glPushMatrix()
    quad1()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 11, -2)
    glRotatef(90, 1, 0, 0)
    glScalef(1, 1.5, 1)
    quad1()
    glPopMatrix()
    
    glBindTexture(GL_TEXTURE_2D, ID2[22])
    glPushMatrix()
    glTranslatef(0, 0, -5)
    glScalef(1, 2, 1)
    quad1()
    glPopMatrix()
    
    glBindTexture(GL_TEXTURE_2D, ID2[4])
    glPushMatrix()
    glTranslatef(0, 0, -2)
    quad2()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(10, 0, -2)
    quad2()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 3, -2)
    glRotatef(90, 1, 0, 0)
    quad1()
    glPopMatrix()
    
    glBindTexture(GL_TEXTURE_2D, ID2[6])
    glPushMatrix()
    glTranslatef(0, 6, 1)
    glScalef(1, 0.5, 1)
    quad1()
    glPopMatrix()
    
    glDisable(GL_TEXTURE_2D)


def dunkinDonuts():
    """Draw a Dunkin Donuts building"""
    materialProperty()
    glEnable(GL_TEXTURE_2D)
    
    glBindTexture(GL_TEXTURE_2D, ID2[19])
    glPushMatrix()
    quad1()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 11, -2)
    glRotatef(90, 1, 0, 0)
    glScalef(1, 1.5, 1)
    quad1()
    glPopMatrix()
    
    glBindTexture(GL_TEXTURE_2D, ID2[21])
    glPushMatrix()
    glTranslatef(0, 0, -5)
    glScalef(1, 2, 1)
    quad1()
    glPopMatrix()
    
    glBindTexture(GL_TEXTURE_2D, ID2[20])
    glPushMatrix()
    glTranslatef(0, 0, -2)
    quad2()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(10, 0, -2)
    quad2()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 3, -2)
    glRotatef(90, 1, 0, 0)
    quad1()
    glPopMatrix()
    
    glBindTexture(GL_TEXTURE_2D, ID2[7])
    glPushMatrix()
    glTranslatef(0, 6, 1)
    glScalef(1, 0.5, 1)
    quad1()
    glPopMatrix()
    
    glDisable(GL_TEXTURE_2D)


def cafeteriaFence():
    """Draw cafeteria fence with bushes"""
    for i in range(-12, 25, 4):
        glPushMatrix()
        glTranslatef(-15.5, -17, i)
        glScalef(1, 2, 1)
        bush()
        glPopMatrix()
    
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, ID2[25])
    
    glPushMatrix()
    glTranslatef(-17, -20, -16.5)
    glScalef(1, 0.5, 15)
    drawBox()
    glPopMatrix()
    
    glDisable(GL_TEXTURE_2D)


def cafeteria():
    """Draw the complete cafeteria area"""
    for i in range(-4, 33, 12):
        for j in range(2, 27, 12):
            glPushMatrix()
            glTranslatef(i, 10, j)
            glScalef(1, 1.5, 1)
            diningSet()
            glPopMatrix()
    
    glPushMatrix()
    glTranslatef(5, -18, -10)
    glScalef(1.5, 2, 1)
    pizzaHut()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-12, -18, -10)
    glScalef(1.5, 2, 1)
    icecreamParlor()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(22, -18, -10)
    glScalef(1.5, 2, 1)
    dunkinDonuts()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(13, 0, 5)
    glScalef(2.9, 1, 2.4)
    ground2()
    glPopMatrix()
    
    cafeteriaFence()
    
    glPushMatrix()
    glTranslatef(58, 0, 0)
    cafeteriaFence()
    glPopMatrix()


def complexOrbiterUnit():
    """Draw a single unit of the complex orbiter"""
    global cmOrbiterTheta
    
    glPushMatrix()
    drawSphere(0, 0, 1, 0, 0, 0.5)
    glPopMatrix()
    
    glPushMatrix()
    glRotatef(cmOrbiterTheta, 0, 1, 0)
    
    j = 0
    for i in range(0, 360, 90):
        glPushMatrix()
        glRotatef(i, 0, 1, 0)
        
        glPushMatrix()
        glRotatef(-45, 0, 0, 1)
        glTranslatef(4, 0, -2.4)
        glRotatef(45, 0, 0, 1)
        ferrisWheelSeat()
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0, 0, -0.5)
        glRotatef(-45, 0, 0, 1)
        glScalef(1.6, 0.2, 0.2)
        drawCube1(colors[j][0], colors[j][1], colors[j][2], colors[j][3], colors[j][4], colors[j][5])
        glPopMatrix()
        
        glPopMatrix()
        
        j += 1
    glPopMatrix()


def complexOrbiter():
    """Draw the complete complex orbiter ride"""
    global cmOrbiterAlpha, cmOrbiterTheta
    
    glPushMatrix()
    glScalef(2, 1, 2)
    ground2()
    glPopMatrix()
    
    # The sphere
    glPushMatrix()
    glTranslatef(0, -1, 0)
    glScalef(2, 2, 2)
    drawSphere(1, 0, 0, 0.5, 0, 0)
    glPopMatrix()
    
    # The cylinder stand
    glPushMatrix()
    glRotatef(90, 1, 0, 0)
    drawCylinder(0, 1, 0, 0, 0.5, 0.5)
    glPopMatrix()
    
    # The ride
    glPushMatrix()
    glRotatef(cmOrbiterAlpha, 0, 1, 0)
    
    for i in range(0, 360, 72):
        glPushMatrix()
        glRotatef(i, 0, 1, 0)
        
        glPushMatrix()
        glTranslatef(0, 0, -0.5)
        glRotatef(-45, 0, 0, 1)
        glScalef(5.8, 0.2, 0.2)
        drawCube1(1, 0, 0, 0.5, 0, 0)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(12, -12, 0)
        complexOrbiterUnit()
        glPopMatrix()
        
        glPopMatrix()
    
    glPopMatrix()


def skyDropStructure():
    """Draw the sky drop structure"""
    for i in np.arange(0, 91, 2.8):
        glPushMatrix()
        glTranslatef(0, i, 0)
        glScalef(0.1, 0.1, -1.5)
        drawCube1(1, 0, 0, 0.5, 0, 0)
        glPopMatrix()
    
    for i in np.arange(0, 88, 2.8):
        glPushMatrix()
        glTranslatef(0, i, 0)
        glRotatef(32, 1, 0, 0)
        glScalef(0.1, 0.1, -1.8)
        drawCube1(1, 0, 0, 0.5, 0, 0)
        glPopMatrix()
    
    for i in np.arange(2.8, 91, 2.8):
        glPushMatrix()
        glTranslatef(0, i, 0)
        glRotatef(-32, 1, 0, 0)
        glScalef(0.1, 0.1, -1.8)
        drawCube1(1, 0, 0, 0.5, 0, 0)
        glPopMatrix()


def skyDropSeat():
    """Draw the sky drop seat"""
    glPushMatrix()
    glTranslatef(-6, 3.2, 1)
    
    glPushMatrix()
    glScalef(6, 1.8, 0.2)
    drawCube1(1, 1, 0, 0.5, 0.5, 0)
    glPopMatrix()
    
    glPushMatrix()
    glScalef(6, 0.2, 1.2)
    drawCube1(1, 1, 0, 0.5, 0.5, 0.5)
    glPopMatrix()
    
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-0.5, 2, 0)
    glScalef(2.2, 0.4, 0.5)
    drawCube1(1, 0, 1, 0.5, 0.5, 0.5)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-0.5, 0.5, 0)
    glScalef(0.3, 3, 0.5)
    drawCube1(0, 0, 1, 0, 0.5, 0.5)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(5.2, 0.5, 0)
    glScalef(0.3, 3, 0.5)
    drawCube1(0, 0, 1, 0, 0.5, 0.5)
    glPopMatrix()
    
    for i in np.arange(-5.5, 14, 2.1):
        glPushMatrix()
        glTranslatef(i, 8, 1.5)
        glRotatef(25, 1, 0, 0)
        glScalef(0.1, 0.1, 0.15)
        drawCylinder(0.412, 0.412, 0.412, 0.2, 0.2, 0.2)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(i, 6.8, 4)
        glRotatef(90, 1, 0, 0)
        glScalef(0.1, 0.1, 0.19)
        drawCylinder(0.412, 0.412, 0.412, 0.2, 0.2, 0.2)
        glPopMatrix()


def skyDropTexture():
    """Draw sky drop texture"""
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, ID2[12])
    glPushMatrix()
    materialProperty()
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(2, 0, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(2, 20, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, 20, 0)
    glEnd()
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)


def skyDropLogo():
    """Draw sky drop logo"""
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, ID2[13])
    glPushMatrix()
    materialProperty()
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(3, 0, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(3, 5, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, 5, 0)
    glEnd()
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)


def skyDrop():
    """Draw the complete sky drop ride"""
    global skyDropPos
    
    for i in range(0, 6, 5):
        glPushMatrix()
        glTranslatef(i, 0, 0)
        glScalef(0.2, 30, 0.2)
        drawCube1(0, 0, 1, 0, 0, 0.5)
        glPopMatrix()
    
    for i in range(0, 6, 5):
        glPushMatrix()
        glTranslatef(i, 0, -5)
        glScalef(0.2, 30, 0.2)
        drawCube1(0, 0, 1, 0, 0, 0.5)
        glPopMatrix()
    
    skyDropStructure()
    
    glPushMatrix()
    glTranslatef(5, 0, 0)
    skyDropStructure()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0.7, 0, -5)
    glRotatef(-90, 0, 1, 0)
    skyDropStructure()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, skyDropPos, 0)
    skyDropSeat()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0.8, 0, 0)
    glScalef(2, 4.5, 1)
    skyDropTexture()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-0.5, 90, 1)
    glScalef(2.5, 2, 1)
    skyDropLogo()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(3, 20, 0)
    ground2()
    glPopMatrix()


# Bezier curve functions
def setNormal(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    """Calculate and set normal for three points"""
    Ux = x2 - x1
    Uy = y2 - y1
    Uz = z2 - z1
    
    Vx = x3 - x1
    Vy = y3 - y1
    Vz = z3 - z1
    
    Nx = Uy * Vz - Uz * Vy
    Ny = Uz * Vx - Ux * Vz
    Nz = Ux * Vy - Uy * Vx
    
    glNormal3f(-Nx, -Ny, -Nz)


def nCr(n, r):
    """Calculate binomial coefficient"""
    if r > n // 2:
        r = n - r
    ans = 1
    for i in range(1, r + 1):
        ans *= n - r + i
        ans //= i
    return ans


def BezierCurve(t, xy, L, ctrlpoints):
    """Calculate point on Bezier curve"""
    y = 0
    x = 0
    t = min(t, 1.0)
    for i in range(L + 1):
        ncr = nCr(L, i)
        oneMinusTpow = pow(1 - t, L - i)
        tPow = pow(t, i)
        coef = oneMinusTpow * tPow * ncr
        x += coef * ctrlpoints[i][0]
        y += coef * ctrlpoints[i][1]
    
    xy[0] = float(x)
    xy[1] = float(y)


def showControlPoints(L, ctrlpoints):
    """Show control points for Bezier curves"""
    glPointSize(5.0)
    glColor3f(1.0, 0.0, 1.0)
    glBegin(GL_POINTS)
    for i in range(L + 1):
        glVertex3fv(ctrlpoints[i])
    glEnd()


def balloonBezier():
    """Draw a balloon using Bezier curves"""
    global show
    L = 5
    balloonctrlpoints = [
        [0.0, 0.0, 0.0], [0.7, 0.8, 0],
        [2, 0.9, 0], [2.3, 0.5, 0],
        [2.5, 0.1, 0], [2.4, 0, 0]
    ]
    
    t = 0
    dt = 1.0 / nt
    xy = [0, 0]
    BezierCurve(t, xy, 5, balloonctrlpoints)
    x = xy[0]
    r = xy[1]
    
    p1x = p1y = p1z = p2x = p2y = p2z = 0  # Initialize variables
    
    for i in range(nt):
        theta = 0
        t += dt
        BezierCurve(t, xy, 5, balloonctrlpoints)
        x1 = xy[0]
        r1 = xy[1]
        
        glBegin(GL_QUAD_STRIP)
        for j in range(ntheta + 1):
            theta += 2 * PI / ntheta
            cosa = math.cos(theta)
            sina = math.sin(theta)
            y = r * cosa
            y1 = r1 * cosa
            z = r * sina
            z1 = r1 * sina
            
            glVertex3f(x, y, z)
            
            if j > 0:
                setNormal(p1x, p1y, p1z, p2x, p2y, p2z, x, y, z)
            else:
                p1x = x
                p1y = y
                p1z = z
                p2x = x1
                p2y = y1
                p2z = z1
            
            glVertex3f(x1, y1, z1)
        glEnd()
        x = x1
        r = r1
    
    if show:
        showControlPoints(L, balloonctrlpoints)


def drawFlag():
    """Draw a flag using Bezier curves"""
    global xf, yf, show
    L = 3
    ctrlpoints1 = [
        [0, 0, 0], [3.5, 0 + yf, 0], [3.5, 0 - yf, 0], [7 + xf, 0, 0]
    ]
    
    ctrlpoints2 = [
        [0, 5, 0], [3.5, 5 + yf, 0], [3.5, 5 - yf, 0], [7 + xf, 5, 0]
    ]
    
    t = 0
    xy1 = [0, 0]
    xy2 = [0, 0]
    dt = 1.0 / nt
    
    glBegin(GL_QUAD_STRIP)
    for i in range(nt):
        BezierCurve(t, xy1, L, ctrlpoints1)
        x1 = xy1[0]
        y1 = xy1[1]
        glVertex3f(x1, y1, 0)
        BezierCurve(t, xy2, L, ctrlpoints2)
        x2 = xy2[0]
        y2 = xy2[1]
        glVertex3f(x2, y2, 0)
        t += dt
    
    glEnd()
    
    if show:
        showControlPoints(L, ctrlpoints1)
        showControlPoints(L, ctrlpoints2)


def balloon():
    """Draw a single balloon"""
    glPushMatrix()
    glRotatef(90, 0, 0, 1)
    glScalef(2, 2.5, 2)
    balloonBezier()
    glPopMatrix()


def balloonLine():
    """Draw balloon string"""
    matCurve(0, 0, 0)
    glBegin(GL_LINES)
    glVertex2f(1, 10)
    glVertex2f(1, 1)
    glEnd()


def balloons():
    """Draw multiple balloons"""
    matCurve(1, 0, 0)
    glPushMatrix()
    glTranslatef(3, -10, 0.6)
    balloon()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(1.8, -19, 0.6)
    balloonLine()
    glPopMatrix()
    
    matCurve(0, 0, 1)
    glPushMatrix()
    glTranslatef(6.2, -11, 0.6)
    balloon()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(1.8, -18, 0.6)
    glRotatef(-22, 0, 0, 1)
    balloonLine()
    glPopMatrix()
    
    matCurve(1, 1, 0)
    glPushMatrix()
    glTranslatef(0, -11, 0.6)
    balloon()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(1.8, -18, 0.6)
    glRotatef(22, 0, 0, 1)
    balloonLine()
    glPopMatrix()
    
    matCurve(1, 0.5, 0)
    glPushMatrix()
    glTranslatef(3, -13, 2.6)
    balloon()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(1.8, -20, 0.6)
    glRotatef(16, 1, 0, 0)
    balloonLine()
    glPopMatrix()
    
    matCurve(1, 0, 1)
    glPushMatrix()
    glTranslatef(3, -13, -1.8)
    balloon()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(1.8, -20, 0.6)
    glRotatef(-14, 1, 0, 0)
    balloonLine()
    glPopMatrix()


def cart():
    """Draw a cart for balloon vendor"""
    materialProperty()
    glEnable(GL_TEXTURE_2D)
    
    glBindTexture(GL_TEXTURE_2D, ID2[26])
    glPushMatrix()
    glScalef(1, 2, 1)
    quad1()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 0, -5)
    glScalef(1, 2, 1)
    quad1()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 0, -2)
    quad2()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(10, 0, -2)
    quad2()
    glPopMatrix()
    
    glBindTexture(GL_TEXTURE_2D, ID2[4])
    glPushMatrix()
    glTranslatef(0, 11, -2)
    glRotatef(90, 1, 0, 0)
    glScalef(1, 1.25, 1)
    quad1()
    glPopMatrix()
    
    glDisable(GL_TEXTURE_2D)


def balloonCart():
    """Draw balloon cart with balloons"""
    balloons()
    
    glPushMatrix()
    glTranslatef(0, -20, 0)
    glScalef(0.5, 0.5, 1)
    cart()
    glPopMatrix()


def flagpole():
    """Draw a flagpole with flag"""
    glPushMatrix()
    glTranslatef(0, 5.5, 0)
    glRotatef(90, 1, 0, 0)
    glScalef(0.2, 0.2, 1.5)
    drawCylinder(1, 0, 0, 0.5, 0, 0)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 5.5, 0)
    glScalef(0.5, 0.5, 0.5)
    drawSphere(.502, 0, 0, 0.26, 0, 0)
    glPopMatrix()
    
    matCurve(0, 0, 1)
    drawFlag()


def flagpole1():
    """Draw a flagpole with yellow flag"""
    glPushMatrix()
    glTranslatef(0, 5.5, 0)
    glRotatef(90, 1, 0, 0)
    glScalef(0.2, 0.2, 1.5)
    drawCylinder(1, 0, 0, 0.5, 0, 0)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 5.5, 0)
    glScalef(0.5, 0.5, 0.5)
    drawSphere(.502, 0, 0, 0.26, 0, 0)
    glPopMatrix()
    
    matCurve(1, 1, 0)
    drawFlag()


def flagpole2():
    """Draw a flagpole with orange flag"""
    glPushMatrix()
    glTranslatef(0, 5.5, 0)
    glRotatef(90, 1, 0, 0)
    glScalef(0.2, 0.2, 1.5)
    drawCylinder(1, 0, 0, 0.5, 0, 0)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 5.5, 0)
    glScalef(0.5, 0.5, 0.5)
    drawSphere(.502, 0, 0, 0.26, 0, 0)
    glPopMatrix()
    
    matCurve(1, 0.5, 0)
    drawFlag()


def flagpole3():
    """Draw a flagpole with purple flag"""
    glPushMatrix()
    glTranslatef(0, 5.5, 0)
    glRotatef(90, 1, 0, 0)
    glScalef(0.2, 0.2, 1.5)
    drawCylinder(1, 0, 0, 0.5, 0, 0)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 5.5, 0)
    glScalef(0.5, 0.5, 0.5)
    drawSphere(.502, 0, 0, 0.26, 0, 0)
    glPopMatrix()
    
    matCurve(1, 0, 1)
    drawFlag()


def trees():
    """Draw trees along the boundaries"""
    for i in range(-40, 56, 15):
        glPushMatrix()
        glTranslatef(-70, -2, i)
        tree()
        glPopMatrix()
    
    for i in range(-40, 56, 15):
        glPushMatrix()
        glTranslatef(100, -2, i)
        tree()
        glPopMatrix()


def wall():
    """Draw a single wall segment"""
    materialProperty()
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, ID2[31])
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(10, 4, 3)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, 4, 3)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 3)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(10, 0, 3)
    glEnd()
    glDisable(GL_TEXTURE_2D)


def walls():
    """Draw all boundary walls"""
    for i in range(20, 101, 10):
        glPushMatrix()
        glTranslatef(i, -20, 60)
        wall()
        glPopMatrix()
    
    for i in range(-80, -9, 10):
        glPushMatrix()
        glTranslatef(i, -20, 60)
        wall()
        glPopMatrix()
    
    for i in range(-80, 101, 10):
        glPushMatrix()
        glTranslatef(i, -20, -70)
        wall()
        glPopMatrix()
    
    for i in range(-57, 64, 10):
        glPushMatrix()
        glTranslatef(-83, -20, i)
        glRotatef(90, 0, 1, 0)
        wall()
        glPopMatrix()
    
    for i in range(-57, 64, 10):
        glPushMatrix()
        glTranslatef(107, -20, i)
        glRotatef(90, 0, 1, 0)
        wall()
        glPopMatrix()


def streetLampbody():
    """Draw street lamp body"""
    glPushMatrix()
    glRotatef(90, 1, 0, 0)
    glScalef(0.5, 0.5, 1)
    drawCylinder(0.1, 0.1, 0.1, 0.05, 0.05, 0.05)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, -19, 0)
    glRotatef(90, 1, 0, 0)
    glScalef(0.2, 0.2, 0.2)
    drawTorus(0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 2, 5, 32, 64)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 0, 0)
    glRotatef(90, 1, 0, 0)
    glScalef(0.2, 0.2, 0.2)
    drawTorus(0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 2, 5, 32, 64)
    glPopMatrix()


def spotLight1():
    """Set up spot light 1"""
    glPushMatrix()
    
    no_light = [0.0, 0.0, 0.0, 1.0]
    light_ambient = [0.5, 0.5, 0.5, 1.0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]
    light_position = [-5.0, 30, 0.0, 1.0]
    
    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position)
    
    spot_direction = [-0.5, -1, 0]
    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, spot_direction)
    glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, 70.0)
    glPopMatrix()


def streetLight1():
    """Draw street light 1"""
    global switchOne
    no_mat = [0.0, 0.0, 0.0, 1.0]
    mat_ambient = [0.7, 0.7, 0.7, 1.0]
    mat_ambient_color = [0.8, 0.8, 0.2, 1.0]
    mat_diffuse = [1.000, 0.843, 0.000, 1.0]
    high_shininess = [100.0]
    mat_emission = [1, 1, 1, 1.0]
    
    glPushMatrix()
    glTranslatef(0, 2, 0)
    glScalef(2, 2, 2)
    glMaterialfv(GL_FRONT, GL_AMBIENT, no_mat)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, no_mat)
    glMaterialfv(GL_FRONT, GL_SHININESS, high_shininess)
    if switchOne:
        glMaterialfv(GL_FRONT, GL_EMISSION, mat_emission)
    else:
        glMaterialfv(GL_FRONT, GL_EMISSION, no_mat)
    glutSolidSphere(1.0, 16, 16)
    glPopMatrix()
    
    streetLampbody()


def spotLight2():
    """Set up spot light 2"""
    glPushMatrix()
    
    no_light = [0.0, 0.0, 0.0, 1.0]
    light_ambient = [0.5, 0.5, 0.5, 1.0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]
    light_position = [25.0, 30, 0.0, 1.0]
    
    glLightfv(GL_LIGHT2, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT2, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT2, GL_POSITION, light_position)
    
    spot_direction = [1, -1, 0.5]
    glLightfv(GL_LIGHT2, GL_SPOT_DIRECTION, spot_direction)
    glLightf(GL_LIGHT2, GL_SPOT_CUTOFF, 70.0)
    glPopMatrix()


def streetLight2():
    """Draw street light 2"""
    global switchTwo
    no_mat = [0.0, 0.0, 0.0, 1.0]
    mat_ambient = [0.7, 0.7, 0.7, 1.0]
    mat_ambient_color = [0.8, 0.8, 0.2, 1.0]
    mat_diffuse = [1.000, 0.843, 0.000, 1.0]
    high_shininess = [100.0]
    mat_emission = [1, 1, 1, 1.0]
    
    glPushMatrix()
    glTranslatef(0, 2, 0)
    glScalef(2, 2, 2)
    glMaterialfv(GL_FRONT, GL_AMBIENT, no_mat)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, no_mat)
    glMaterialfv(GL_FRONT, GL_SHININESS, high_shininess)
    if switchTwo:
        glMaterialfv(GL_FRONT, GL_EMISSION, mat_emission)
    else:
        glMaterialfv(GL_FRONT, GL_EMISSION, no_mat)
    glutSolidSphere(1.0, 16, 16)
    glPopMatrix()
    
    streetLampbody()


def spotLight3():
    """Set up spot light 3"""
    glPushMatrix()
    
    no_light = [0.0, 0.0, 0.0, 1.0]
    light_ambient = [0.5, 0.5, 0.5, 1.0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]
    light_position = [25.0, 30, 10.0, 1.0]
    
    glLightfv(GL_LIGHT3, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT3, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT3, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT3, GL_POSITION, light_position)
    
    spot_direction = [1, -1, 0]
    glLightfv(GL_LIGHT3, GL_SPOT_DIRECTION, spot_direction)
    glLightf(GL_LIGHT3, GL_SPOT_CUTOFF, 60.0)
    glPopMatrix()


def streetLight3():
    """Draw street light 3"""
    global switchThree
    no_mat = [0.0, 0.0, 0.0, 1.0]
    mat_ambient = [0.7, 0.7, 0.7, 1.0]
    mat_ambient_color = [0.8, 0.8, 0.2, 1.0]
    mat_diffuse = [1.000, 0.843, 0.000, 1.0]
    high_shininess = [100.0]
    mat_emission = [1, 1, 1, 1.0]
    
    glPushMatrix()
    glTranslatef(0, 2, 0)
    glScalef(2, 2, 2)
    glMaterialfv(GL_FRONT, GL_AMBIENT, no_mat)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, no_mat)
    glMaterialfv(GL_FRONT, GL_SHININESS, high_shininess)
    if switchThree:
        glMaterialfv(GL_FRONT, GL_EMISSION, mat_emission)
    else:
        glMaterialfv(GL_FRONT, GL_EMISSION, no_mat)
    glutSolidSphere(1.0, 16, 16)
    glPopMatrix()
    
    streetLampbody()


def spotLight4():
    """Set up spot light 4"""
    glPushMatrix()
    
    no_light = [0.0, 0.0, 0.0, 1.0]
    light_ambient = [0.5, 0.5, 0.5, 1.0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]
    light_position = [-20.0, 30, 10.0, 1.0]
    
    glLightfv(GL_LIGHT4, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT4, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT4, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT4, GL_POSITION, light_position)
    
    spot_direction = [-0.5, -1, 0]
    glLightfv(GL_LIGHT4, GL_SPOT_DIRECTION, spot_direction)
    glLightf(GL_LIGHT4, GL_SPOT_CUTOFF, 60.0)
    glPopMatrix()


def streetLight4():
    """Draw street light 4"""
    global switchFour
    no_mat = [0.0, 0.0, 0.0, 1.0]
    mat_ambient = [0.7, 0.7, 0.7, 1.0]
    mat_ambient_color = [0.8, 0.8, 0.2, 1.0]
    mat_diffuse = [1.000, 0.843, 0.000, 1.0]
    high_shininess = [100.0]
    mat_emission = [1, 1, 1, 1.0]
    
    glPushMatrix()
    glTranslatef(0, 2, 0)
    glScalef(2, 2, 2)
    glMaterialfv(GL_FRONT, GL_AMBIENT, no_mat)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, no_mat)
    glMaterialfv(GL_FRONT, GL_SHININESS, high_shininess)
    if switchFour:
        glMaterialfv(GL_FRONT, GL_EMISSION, mat_emission)
    else:
        glMaterialfv(GL_FRONT, GL_EMISSION, no_mat)
    glutSolidSphere(1.0, 16, 16)
    glPopMatrix()
    
    streetLampbody()


def bench1():
    """Draw bench type 1"""
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, ID2[16])
    glScalef(2, 0.5, 0.5)
    drawBox()
    glDisable(GL_TEXTURE_2D)


def bench2():
    """Draw bench type 2"""
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, ID2[19])
    glScalef(2, 0.5, 0.5)
    drawBox()
    glDisable(GL_TEXTURE_2D)


def display():
    """Main display function"""
    global eyeX, eyeY, eyeZ, refX, refY, refZ
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1, 1, 300)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(eyeX, eyeY, eyeZ, refX, refY, refZ, 0, 1, 0)
    
    glEnable(GL_LIGHTING)
    
    glPushMatrix()
    sky(eyeX + (0.05 * refX), eyeY + (0.05 * refY), eyeZ + (0.05 * refZ), 250, 250, 250)
    glPopMatrix()
    
    glEnable(GL_DEPTH_TEST)
    
    spotLight1()
    spotLight2()
    spotLight3()
    spotLight4()
    ground()
    walls()
    trees()
    
    for i in range(-70, -9, 20):
        glPushMatrix()
        glTranslatef(i, -20, 55)
        bench1()
        glPopMatrix()
    
    for i in range(-60, -19, 20):
        glPushMatrix()
        glTranslatef(i, -20, 55)
        bench2()
        glPopMatrix()
    
    for i in range(30, 101, 20):
        glPushMatrix()
        glTranslatef(i, -20, 55)
        bench1()
        glPopMatrix()
    
    for i in range(40, 91, 20):
        glPushMatrix()
        glTranslatef(i, -20, 55)
        bench2()
        glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-25, 0, 0)
    streetLight1()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(50, 0, 0)
    streetLight2()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(50, 0, 30)
    streetLight3()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-25, 0, 30)
    streetLight4()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 0, 10)
    cafeteria()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(65, 0, -30)
    ferrisWheel()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(75, 0, 20)
    orbiter()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-50, 0, -30)
    complexOrbiter()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-50, 0, 10)
    pirateBoat()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-20, -20, -40)
    skyDrop()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-30, 0, 40)
    balloonCart()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-60, 0, 40)
    balloonCart()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(45, 0, 48)
    balloonCart()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(80, 0, 48)
    balloonCart()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(15, 0, -3)
    flagpole()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(5, 0, -3)
    flagpole1()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(25, 0, -3)
    flagpole2()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-5, 0, -3)
    flagpole3()
    glPopMatrix()
    
    glDisable(GL_LIGHTING)
    
    glFlush()
    glutSwapBuffers()


def myKeyboardFunc(key, x, y):
    """Handle keyboard input"""
    global eyeX, eyeY, eyeZ, refX, refY, refZ
    global orbiterFlag, fanSwitch, skyDropFlag, cmOrbiterFlag, pirateBoatFlag
    global switchOne, switchTwo, switchThree, switchFour, show, door1, day, alpha
    
    if key == b'w':  # move eye point upwards along Y axis
        eyeY += 1.0
    elif key == b's':  # move eye point downwards along Y axis
        eyeY -= 1.0
    elif key == b'a':  # move eye point left along X axis
        eyeX -= 1.0
    elif key == b'd':  # move eye point right along X axis
        eyeX += 1.0
    elif key == b'o':  # zoom out
        eyeZ += 1
    elif key == b'i':  # zoom in
        eyeZ -= 1
    elif key == b'q':  # back to default eye point and ref point
        eyeX = 0.0
        eyeY = 2.0
        eyeZ = 30.0
        refX = 0.0
        refY = 0.0
        refZ = 0.0
    elif key == b'j':  # move ref point upwards along Y axis
        refY += 1.0
    elif key == b'n':  # move ref point downwards along Y axis
        refY -= 1.0
    elif key == b'b':  # move ref point left along X axis
        refX -= 1.0
    elif key == b'm':  # move eye point right along X axis
        refX += 1.0
    elif key == b'k':  # move ref point away from screen/ along z axis
        refZ += 1
    elif key == b'l':  # move ref point towards screen/ along z axis
        refZ -= 1
    elif key == b'1':  # orbiter
        orbiterFlag = not orbiterFlag
    elif key == b'2':  # ferriswheel
        fanSwitch = not fanSwitch
    elif key == b'3':  # skydrop
        skyDropFlag = not skyDropFlag
    elif key == b'4':  # complex orbiter
        cmOrbiterFlag = not cmOrbiterFlag
    elif key == b'5':  # pirate boat
        pirateBoatFlag = not pirateBoatFlag
    elif key == b'6':  # spot light 1
        switchOne = not switchOne
        if switchOne:
            glEnable(GL_LIGHT1)
        else:
            glDisable(GL_LIGHT1)
    elif key == b'7':  # spot light 2
        switchTwo = not switchTwo
        if switchTwo:
            glEnable(GL_LIGHT2)
        else:
            glDisable(GL_LIGHT2)
    elif key == b'8':  # spot light 3
        switchThree = not switchThree
        if switchThree:
            glEnable(GL_LIGHT3)
        else:
            glDisable(GL_LIGHT3)
    elif key == b'9':  # spot light 4
        switchFour = not switchFour
        if switchFour:
            glEnable(GL_LIGHT4)
        else:
            glDisable(GL_LIGHT4)
    elif key == b'z':  # show control points
        show = not show
    elif key == b'g':  # gate
        door1 = not door1
    elif key == b'0':  # day/night
        day = not day
        if day:
            glEnable(GL_LIGHT0)
        else:
            glDisable(GL_LIGHT0)
    elif key == 27:  # Escape key
        exit(1)
    
    glutPostRedisplay()


def animate():
    """Animation function"""
    global theta, orbiterAlpha, orbiterTheta, testTheta, pirateBoatTheta, pirateBoatCheck
    global cmOrbiterAlpha, cmOrbiterTheta, skyDropPos, upFlag, downFlag1, downFlag2, downFlag3
    global alpha, door1, yf, yflag, xf, xflag
    
    # Sky drop animation
    if skyDropFlag:
        if upFlag:
            skyDropPos += 0.5
            if skyDropPos >= 80:
                upFlag = False
        else:
            if downFlag1 and not downFlag2 and not downFlag3:
                skyDropPos -= 2
                if skyDropPos <= 5:
                    upFlag = True
                    downFlag1 = False
                    downFlag2 = True
                    downFlag3 = False
            elif not downFlag1 and downFlag2 and not downFlag3:
                skyDropPos -= 3
                if skyDropPos <= 45:
                    upFlag = True
                    downFlag1 = False
                    downFlag2 = False
                    downFlag3 = True
            elif not downFlag1 and not downFlag2 and downFlag3:
                skyDropPos -= 4
                if skyDropPos <= 15:
                    upFlag = True
                    downFlag1 = True
                    downFlag2 = False
                    downFlag3 = False
    else:
        skyDropPos -= 2
        if skyDropPos <= 2:
            skyDropPos = 2
    
    # Complex orbiter animation
    if cmOrbiterFlag:
        cmOrbiterTheta += 10
        cmOrbiterAlpha += 1
    
    # Pirate boat animation
    if pirateBoatFlag:
        if pirateBoatCheck:
            pirateBoatTheta += 2
            if pirateBoatTheta == 60:
                pirateBoatCheck = False
        else:
            pirateBoatTheta -= 2
            if pirateBoatTheta == -70:
                pirateBoatCheck = True
    else:
        if pirateBoatTheta < 0:
            pirateBoatTheta += 1
            if pirateBoatTheta == 0:
                pirateBoatTheta = 0
        elif pirateBoatTheta > 0:
            pirateBoatTheta -= 1
            if pirateBoatTheta == 0:
                pirateBoatTheta = 0
    
    # Ferris wheel animation
    if fanSwitch:
        theta += 2
        if theta > 360.0:
            theta -= 360.0 * math.floor(theta / 360.0)
    
    # Orbiter animation
    if orbiterFlag:
        orbiterTheta += 3
        if orbiterTheta > 360.0:
            orbiterTheta -= 360.0 * math.floor(orbiterTheta / 360.0)
        
        orbiterAlpha += 2
        if orbiterAlpha >= 45:
            orbiterAlpha = 45
    else:
        orbiterAlpha -= 1
        if orbiterAlpha <= -45:
            orbiterAlpha = -45
        
        orbiterTheta += 3
        if orbiterAlpha == -45:
            orbiterTheta = 0
    
    # Gate animation
    if door1:
        alpha += 10
        if alpha > 90:
            alpha = 90
    else:
        alpha -= 10
        if alpha < 0:
            alpha = 0
    
    # Flag animation
    if yflag:
        yf += 0.1
        if yf >= 2:
            yflag = False
    else:
        yf -= 0.1
        if yf <= -2:
            yflag = True
    
    if xflag:
        xf += 0.1
        if xf >= 0.6:
            xflag = False
    else:
        xf -= 0.1
        if xf <= -0.6:
            xflag = True
    
    glutPostRedisplay()


def fullScreen(w, h):
    """Handle window resize"""
    # Prevent a divide by zero
    if h == 0:
        h = 1
    ratio = float(w) / float(h)
    
    # Set the perspective coordinate system
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    glViewport(0, 0, w, h)
    gluPerspective(60, ratio, 1, 500)
    glMatrixMode(GL_MODELVIEW)


def main():
    """Main function"""
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    
    glutInitWindowPosition(100, 100)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Amusement Park 3D")
    
    glShadeModel(GL_SMOOTH)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    light()
    
    # Print instructions
    print("To move Eye point:")
    print("w: up")
    print("s: down")
    print("a: left")
    print("d: right")
    print("i: zoom in")
    print("o: zoom out")
    print("")
    print("To move Camera point:")
    print("j: up")
    print("n: down")
    print("b: left")
    print("m: right")
    print("l: move nearer")
    print("k: move far")
    print("")
    print("Press q to move to default position")
    print("")
    print("To control Rides:")
    print("1: Orbiter")
    print("2: Ferris Wheel")
    print("3: Sky Drop")
    print("4: Complex Orbiter")
    print("5: Pirate Boat")
    print("")
    print("To control lights:")
    print("6: Spotlight 1")
    print("7: Spotlight 2")
    print("8: Spotlight 3")
    print("9: Spotlight 4")
    print("")
    print("Other controls:")
    print("0: Day/Night")
    print("Z: To show control points")
    print("G: Open/Close gate")
    
    # Load textures (placeholders)
    for i in range(32):
        LoadTexture2(f"texture_{i}.sgi", i)
    
    glutReshapeFunc(fullScreen)
    glutKeyboardFunc(myKeyboardFunc)
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutMainLoop()


if __name__ == "__main__":
    main()