from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Camera-related variables
camera_pos = [0.0, 500.0, 500.0]
fovY = 120  # Field of view
GRID_LENGTH = 600  # Length of grid lines
rand_var = 423

# ---------------------------
# Global state (ported keys)
# ---------------------------

alpha = 0.0
theta = 0.0
orbiterAlpha = -45.0
orbiterTheta = 0.0
pirateBoatTheta = 0.0
cmOrbiterAlpha = 0.0
cmOrbiterTheta = 0.0
skyDropPos = 2.0

fanSwitch = False
orbiterFlag = False
pirateBoatFlag = False
pirateBoatCheck = False
cmOrbiterFlag = False
skyDropFlag = False
upFlag = True
downFlag1 = True
downFlag2 = False
downFlag3 = False
day = True
switchOne = False
switchTwo = False
switchThree = False
switchFour = False


# ---------------------------
# Text helper (template)
# ---------------------------

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


# ---------------------------
# Basic draw helpers
# ---------------------------

def material_white(shininess=60.0):
    no_mat = [0.0, 0.0, 0.0, 1.0]
    mat_ambient = [1.0, 1.0, 1.0, 1.0]
    mat_diffuse = [1.0, 1.0, 1.0, 1.0]
    mat_specular = [1.0, 1.0, 1.0, 1.0]
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, shininess)
    glMaterialfv(GL_FRONT, GL_EMISSION, no_mat)


def set_material_color(r, g, b, amb_scale=0.5, shininess=60.0):
    no_mat = [0.0, 0.0, 0.0, 1.0]
    mat_ambient = [r * amb_scale, g * amb_scale, b * amb_scale, 1.0]
    mat_diffuse = [r, g, b, 1.0]
    mat_specular = [1.0, 1.0, 1.0, 1.0]
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, shininess)
    glMaterialfv(GL_FRONT, GL_EMISSION, no_mat)


def draw_unit_cube(size=3.0):
    glutSolidCube(size)


def draw_sphere(radius=1.0, slices=24, stacks=24):
    glutSolidSphere(radius, slices, stacks)


def draw_cylinder(base=1.5, top=1.5, height=19.0, slices=24, stacks=1):
    quad = gluNewQuadric()
    gluCylinder(quad, base, top, height, slices, stacks)


def draw_torus(inner_radius=0.5, outer_radius=10.0, sides=24, rings=48):
    glutSolidTorus(inner_radius, outer_radius, sides, rings)


# ---------------------------
# Lights
# ---------------------------

def setup_global_light():
    ambient = [1.0, 1.0, 1.0, 1.0]
    diffuse = [1.0, 1.0, 1.0, 1.0]
    specular = [1.0, 1.0, 1.0, 1.0]
    position = [20.0, 50.0, 0.0, 1.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT0, GL_POSITION, position)


def spot_light_1():
    ambient = [0.5, 0.5, 0.5, 1.0]
    diffuse = [1.0, 1.0, 1.0, 1.0]
    specular = [1.0, 1.0, 1.0, 1.0]
    position = [-5.0, 30.0, 0.0, 1.0]
    direction = [-0.5, -1.0, 0.0]
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT1, GL_POSITION, position)
    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, direction)
    glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, 70.0)


def spot_light_2():
    ambient = [0.5, 0.5, 0.5, 1.0]
    diffuse = [1.0, 1.0, 1.0, 1.0]
    specular = [1.0, 1.0, 1.0, 1.0]
    position = [25.0, 30.0, 0.0, 1.0]
    direction = [1.0, -1.0, 0.5]
    glLightfv(GL_LIGHT2, GL_AMBIENT, ambient)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT2, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT2, GL_POSITION, position)
    glLightfv(GL_LIGHT2, GL_SPOT_DIRECTION, direction)
    glLightf(GL_LIGHT2, GL_SPOT_CUTOFF, 70.0)


def spot_light_3():
    ambient = [0.5, 0.5, 0.5, 1.0]
    diffuse = [1.0, 1.0, 1.0, 1.0]
    specular = [1.0, 1.0, 1.0, 1.0]
    position = [25.0, 30.0, 10.0, 1.0]
    direction = [1.0, -1.0, 0.0]
    glLightfv(GL_LIGHT3, GL_AMBIENT, ambient)
    glLightfv(GL_LIGHT3, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT3, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT3, GL_POSITION, position)
    glLightfv(GL_LIGHT3, GL_SPOT_DIRECTION, direction)
    glLightf(GL_LIGHT3, GL_SPOT_CUTOFF, 60.0)


def spot_light_4():
    ambient = [0.5, 0.5, 0.5, 1.0]
    diffuse = [1.0, 1.0, 1.0, 1.0]
    specular = [1.0, 1.0, 1.0, 1.0]
    position = [-20.0, 30.0, 10.0, 1.0]
    direction = [-0.5, -1.0, 0.0]
    glLightfv(GL_LIGHT4, GL_AMBIENT, ambient)
    glLightfv(GL_LIGHT4, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT4, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT4, GL_POSITION, position)
    glLightfv(GL_LIGHT4, GL_SPOT_DIRECTION, direction)
    glLightf(GL_LIGHT4, GL_SPOT_CUTOFF, 60.0)


# ---------------------------
# Scene pieces (simplified)
# ---------------------------

def ground_plane():
    set_material_color(0.2, 0.6, 0.2, amb_scale=0.3)
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(150, -20, 150)
    glVertex3f(150, -20, -150)
    glVertex3f(-150, -20, -150)
    glVertex3f(-150, -20, 150)
    glEnd()


def ferris_wheel():
    global theta, alpha

    # Base
    glPushMatrix()
    glTranslatef(0, -19.5, 2.5)
    glScalef(12, 1.5, 9)
    set_material_color(0.545, 0.271, 0.075, 0.3)
    draw_unit_cube()
    glPopMatrix()

    # Supports
    set_material_color(0.545, 0.0, 0.545, 0.2)
    for z in (-1.0, 6.0):
        glPushMatrix()
        glTranslatef(-0.2, 0, z)
        glRotatef(-75, 0, 0, 1)
        glScalef(21, 0.84, 0.3)
        draw_unit_cube()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-0.6, 0, z)
        glRotatef(-105, 0, 0, 1)
        glScalef(21, 0.84, 0.3)
        draw_unit_cube()
        glPopMatrix()

    # Wheel pair
    glPushMatrix()
    glRotatef(-theta, 0, 0, 1)
    glScalef(1.5, 1.5, 1)

    # Hub spheres
    set_material_color(1.0, 0.0, 0.0)
    glPushMatrix()
    glScalef(1, 1, 2)
    draw_sphere(1.0, 24, 24)
    glPopMatrix()

    # Tori rims (front and back)
    set_material_color(1.0, 1.0, 0.3, 0.2)
    glPushMatrix()
    draw_torus(0.5, 10.0, 24, 48)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0, 5)
    draw_torus(0.5, 10.0, 24, 48)
    glPopMatrix()

    # Spokes and seats
    for ang in range(0, 360, 30):
        # Spoke bars
        set_material_color(0.867, 0.627, 0.867, 0.3, shininess=100)
        glPushMatrix()
        glRotatef(ang, 0, 0, 1)
        glScalef(6.6, 0.1, 0.5)
        glTranslatef(0, 0, 0)
        draw_unit_cube()
        glPopMatrix()

        # Seat pair (front/back)
        for z in (0.9, 5.9):
            glPushMatrix()
            glRotatef(ang, 0, 0, 1)
            glTranslatef(10, 0, z)
            glRotatef(-ang + theta, 0, 0, 1)
            glScalef(1, 1, 0.8)
            set_material_color(0.804, 0.361, 0.361, 0.2)
            draw_unit_cube(1.5)
            glPopMatrix()

    # Center bar
    set_material_color(0.2, 0.1, 0.1, 0.1)
    glPushMatrix()
    glScalef(0.3, 0.15, 4.5)
    draw_unit_cube()
    glPopMatrix()

    glPopMatrix()


def orbiter():
    global orbiterAlpha, orbiterTheta

    # Base ground
    glPushMatrix()
    glScalef(20, 1, 20)
    set_material_color(0.3, 0.3, 0.3, 0.2)
    draw_unit_cube()
    glPopMatrix()

    # Central sphere
    glPushMatrix()
    glTranslatef(0, -1, 0)
    glScalef(2.5, 2.5, 2.5)
    set_material_color(1.0, 0.0, 0.0)
    draw_sphere(1.0, 24, 24)
    glPopMatrix()

    # Rotating arms with seats
    glPushMatrix()
    glTranslatef(0, -5, 0)
    glRotatef(orbiterTheta, 0, 1, 0)
    for ang in range(0, 360, 45):
        glPushMatrix()
        glRotatef(ang, 0, 1, 0)
        # arm
        set_material_color(0.0, 0.0, 1.0, 0.2)
        glPushMatrix()
        glRotatef(orbiterAlpha, 0, 0, 1)
        glScalef(5.1, 0.2, 0.2)
        draw_unit_cube()
        glPopMatrix()

        # seat
        set_material_color(0.804, 0.361, 0.361, 0.2)
        glPushMatrix()
        glRotatef(orbiterAlpha, 0, 0, 1)
        glTranslatef(15, 0, -2)
        glScalef(1.5, 0.6, 1.2)
        draw_unit_cube()
        glPopMatrix()

        glPopMatrix()
    glPopMatrix()


def complex_orbiter():
    global cmOrbiterAlpha, cmOrbiterTheta

    # Central ball
    glPushMatrix()
    glTranslatef(0, -1, 0)
    glScalef(2, 2, 2)
    set_material_color(1.0, 0.0, 0.0)
    draw_sphere(1.0, 24, 24)
    glPopMatrix()

    # Vertical cylinder
    glPushMatrix()
    glRotatef(90, 1, 0, 0)
    set_material_color(0.0, 1.0, 0.0, 0.2)
    draw_cylinder(1.5, 1.5, 19.0, 24, 1)
    glPopMatrix()

    # Rotating star with units
    glPushMatrix()
    glRotatef(cmOrbiterAlpha, 0, 1, 0)
    for ang in range(0, 360, 72):
        glPushMatrix()
        glRotatef(ang, 0, 1, 0)
        set_material_color(1.0, 0.0, 0.0, 0.2)
        glPushMatrix()
        glTranslatef(0, 0, -0.5)
        glRotatef(-45, 0, 0, 1)
        glScalef(5.8, 0.2, 0.2)
        draw_unit_cube()
        glPopMatrix()

        # An orbiting unit ring
        glPushMatrix()
        glTranslatef(12, -12, 0)
        glRotatef(cmOrbiterTheta, 0, 1, 0)
        # four small seats
        for sub in range(0, 360, 90):
            glPushMatrix()
            glRotatef(sub, 0, 1, 0)
            set_material_color(0.8, 0.8, 0.0, 0.3)
            glPushMatrix()
            glRotatef(-45, 0, 0, 1)
            glTranslatef(4, 0, -2.4)
            glRotatef(45, 0, 0, 1)
            glScalef(1.5, 0.6, 1.2)
            draw_unit_cube()
            glPopMatrix()
            glPopMatrix()
        glPopMatrix()

        glPopMatrix()
    glPopMatrix()


def pirate_boat():
    global pirateBoatTheta

    # Base
    glPushMatrix()
    glTranslatef(0.5, -19.5, 0)
    glScalef(18, 1.5, 12)
    set_material_color(0.545, 0.271, 0.075, 0.3)
    draw_unit_cube()
    glPopMatrix()

    # Swinging boat body (simplified as a box)
    glPushMatrix()
    glTranslatef(1.5, -12, 0)
    glRotatef(pirateBoatTheta, 0, 0, 1)
    set_material_color(0.412, 0.412, 0.412, 0.2)
    glScalef(11, 2, 3)
    draw_unit_cube()
    glPopMatrix()

    # Frame arcs (simplified)
    set_material_color(0.2, 0.1, 0.1, 0.1)
    for z in (1.4, -1.6, 5.0, -5.0):
        glPushMatrix()
        glTranslatef(0, 0, z)
        glRotatef(pirateBoatTheta, 0, 0, 1)
        glRotatef(-60, 0, 0, 1)
        glScalef(18, 0.84, 0.3)
        draw_unit_cube()
        glPopMatrix()


def sky_drop():
    global skyDropPos

    # Tower columns
    set_material_color(0.0, 0.0, 1.0, 0.3)
    for dx in (0.0, 5.0):
        for dz in (0.0, -5.0):
            glPushMatrix()
            glTranslatef(dx, 0, dz)
            glScalef(0.6, 30, 0.6)
            draw_unit_cube()
            glPopMatrix()

    # Moving seat
    glPushMatrix()
    glTranslatef(0, skyDropPos, 0)
    set_material_color(1.0, 1.0, 0.0, 0.3)
    glScalef(6, 1.8, 2)
    draw_unit_cube()
    glPopMatrix()


def benches_row(x_start, x_end, step, z, color_variant=0):
    for x in range(x_start, x_end + 1, step):
        glPushMatrix()
        glTranslatef(float(x), -20.0, float(z))
        if color_variant == 0:
            set_material_color(0.6, 0.3, 0.2, 0.3)
        else:
            set_material_color(0.5, 0.5, 0.7, 0.3)
        glScalef(6, 1.5, 1.5)
        draw_unit_cube()
        glPopMatrix()


# ---------------------------
# Template demo shapes (kept minimal)
# ---------------------------

def draw_shapes():
    glPushMatrix()
    set_material_color(1, 0, 0)
    glTranslatef(0, 0, 0)
    glutSolidCube(60)

    glTranslatef(0, 0, 100)
    set_material_color(0, 1, 0)
    glutSolidCube(60)

    set_material_color(1, 1, 0)
    glScalef(2, 2, 2)
    gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)

    glTranslatef(100, 0, 100)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)

    set_material_color(0, 1, 1)
    glTranslatef(300, 0, 100)
    gluSphere(gluNewQuadric(), 80, 10, 10)
    glPopMatrix()


# ---------------------------
# Input handlers
# ---------------------------

def keyboardListener(key, x, y):
    global camera_pos, fanSwitch, orbiterFlag, cmOrbiterFlag, pirateBoatFlag
    global skyDropFlag, day, switchOne, switchTwo, switchThree, switchFour
    global alpha

    if key == b'w':
        camera_pos[1] += 10.0
    if key == b's':
        camera_pos[1] -= 10.0
    if key == b'a':
        camera_pos[0] -= 10.0
    if key == b'd':
        camera_pos[0] += 10.0
    if key == b'i':
        camera_pos[2] -= 10.0
    if key == b'o':
        camera_pos[2] += 10.0
    if key == b'q':
        camera_pos[:] = [0.0, 500.0, 500.0]

    # Toggles similar to original
    if key == b'1':
        orbiterFlag = not orbiterFlag
    if key == b'2':
        fanSwitch = not fanSwitch
    if key == b'3':
        skyDropFlag = not skyDropFlag
    if key == b'4':
        cmOrbiterFlag = not cmOrbiterFlag
    if key == b'5':
        pirateBoatFlag = not pirateBoatFlag
    if key == b'6':
        switchOne = not switchOne
        (glEnable if switchOne else glDisable)(GL_LIGHT1)
    if key == b'7':
        switchTwo = not switchTwo
        (glEnable if switchTwo else glDisable)(GL_LIGHT2)
    if key == b'8':
        switchThree = not switchThree
        (glEnable if switchThree else glDisable)(GL_LIGHT3)
    if key == b'9':
        switchFour = not switchFour
        (glEnable if switchFour else glDisable)(GL_LIGHT4)
    if key == b'0':
        day = not day
        (glEnable if day else glDisable)(GL_LIGHT0)

    # Gate angle control (g like original toggled animation; here we just open/close)
    if key == b'g':
        alpha = 90.0 if alpha <= 0.0 else 0.0


def specialKeyListener(key, x, y):
    global camera_pos
    cx, cy, cz = camera_pos
    if key == GLUT_KEY_LEFT:
        cx -= 10.0
    if key == GLUT_KEY_RIGHT:
        cx += 10.0
    camera_pos[:] = [cx, cy, cz]


def mouseListener(button, state, x, y):
    pass


# ---------------------------
# Camera setup (template)
# ---------------------------

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 3000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    x, y, z = camera_pos
    gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)


# ---------------------------
# Animation loop
# ---------------------------

def idle():
    animate()
    glutPostRedisplay()


def animate():
    global skyDropPos, upFlag, downFlag1, downFlag2, downFlag3
    global cmOrbiterFlag, cmOrbiterTheta, cmOrbiterAlpha
    global pirateBoatFlag, pirateBoatCheck, pirateBoatTheta
    global fanSwitch, theta, orbiterFlag, orbiterTheta, orbiterAlpha
    global alpha

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
            elif (not downFlag1) and downFlag2 and (not downFlag3):
                skyDropPos -= 3
                if skyDropPos <= 45:
                    upFlag = True
                    downFlag1 = False
                    downFlag2 = False
                    downFlag3 = True
            elif (not downFlag1) and (not downFlag2) and downFlag3:
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

    if cmOrbiterFlag:
        cmOrbiterTheta += 10
        cmOrbiterAlpha += 1

    if pirateBoatFlag:
        if pirateBoatCheck:
            pirateBoatTheta += 2
            if pirateBoatTheta >= 60:
                pirateBoatCheck = False
        else:
            pirateBoatTheta -= 2
            if pirateBoatTheta <= -70:
                pirateBoatCheck = True
    else:
        if pirateBoatTheta < 0:
            pirateBoatTheta += 1
        elif pirateBoatTheta > 0:
            pirateBoatTheta -= 1

    if fanSwitch:
        theta += 2
        if theta > 360.0:
            theta -= 360.0 * int(theta / 360.0)

    if orbiterFlag:
        orbiterTheta += 3
        if orbiterTheta > 360.0:
            orbiterTheta -= 360.0 * int(orbiterTheta / 360.0)
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

    # Gate open/close smoothing
    if alpha > 0:
        alpha = min(alpha + 0.0, 90.0)
    else:
        alpha = max(alpha - 0.0, 0.0)


# ---------------------------
# Display
# ---------------------------

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    # Background color based on day/night
    if day:
        glClearColor(0.2, 0.5, 0.9, 1.0)
    else:
        glClearColor(0.02, 0.02, 0.06, 1.0)

    setupCamera()

    # Lighting
    glEnable(GL_LIGHTING)
    setup_global_light()
    spot_light_1()
    spot_light_2()
    spot_light_3()
    spot_light_4()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)

    # World
    ground_plane()

    # Benches like original ranges
    benches_row(-70, -10, 20, 55, color_variant=0)
    benches_row(-60, -20, 20, 55, color_variant=1)
    benches_row(30, 100, 20, 55, color_variant=0)
    benches_row(40, 90, 20, 55, color_variant=1)

    # Rides placement
    glPushMatrix()
    glTranslatef(65, 0, -30)
    ferris_wheel()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(75, 0, 20)
    orbiter()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-50, 0, -30)
    complex_orbiter()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-50, 0, 10)
    pirate_boat()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-20, -20, -40)
    sky_drop()
    glPopMatrix()

    # HUD text
    glDisable(GL_LIGHTING)
    draw_text(10, 770, "Amusement Park 3D - Python (PyOpenGL)")
    draw_text(10, 740, f"Toggles: 1-Orbiter 2-FerrisWheel 3-SkyDrop 4-ComplexOrbiter 5-PirateBoat")
    draw_text(10, 715, f"Lights: 6/7/8/9 | Day/Night: 0 | Move: WASD / I/O / arrows")
    draw_text(10, 690, f"rand_var: {rand_var}")

    glutSwapBuffers()


# ---------------------------
# Main
# ---------------------------

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"3D OpenGL Amusement Park - PyOpenGL")

    glShadeModel(GL_SMOOTH)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    setup_global_light()
    glEnable(GL_LIGHT0)

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()


if __name__ == "__main__":
    main()

