import sys
import os
import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# ----------------------------------------
# Variables globales
# ----------------------------------------

tamX = 0
tamY = 0
tamZ = 0

imagen = None

corte = 0

radio = 50
centro_x = 128
centro_y = 128

alfa = 1.5

a = -0.2
b = 0.1
c = 0.1
d = -0.2

ESC = 255.0


# ----------------------------------------
# Transformación Castel & Angel
# ----------------------------------------
def castel_angel(vectt):

    x = vectt[0]
    y = vectt[1]

    lambdaa = math.sqrt((x-centro_x)**2 +
                        (y-centro_y)**2)/(math.sqrt(2)*radio)

    if lambdaa > 1:
        lambdaa = 1

    L = lambdaa**alfa

    xt = (1-L)*((1+a)*x + b*y) + L*x

    yt = (1-L)*(c*x + (1+d)*y) + L*y

    vectt[0] = xt
    vectt[1] = yt


# ----------------------------------------
# Construcción de imagen
# ----------------------------------------
def forma_imagen():

    glNewList(1, GL_COMPILE)

    for y in range(tamY):

        for x in range(tamX):

            intensidad = imagen[corte, y, x]/ESC

            glColor3f(intensidad,
                      intensidad,
                      intensidad)

            punto = [float(x), float(y)]

            castel_angel(punto)

            xt = int(punto[0])
            yt = int(punto[1])

            if 0 <= xt < tamX and 0 <= yt < tamY:

                glBegin(GL_POINTS)

                glVertex2i(xt, tamY-1-yt)

                glEnd()

    glEndList()


# ----------------------------------------
# Display
# ----------------------------------------
def display():

    glClear(GL_COLOR_BUFFER_BIT)

    glCallList(1)

    glutSwapBuffers()


# ----------------------------------------
# Lectura del archivo raw
# ----------------------------------------
def leer_imagen():

    global imagen
    global tamX
    global tamY
    global tamZ

    archivo = input("Archivo .raw: ")

    tamX = int(input("tamX: "))
    tamY = int(input("tamY: "))
    tamZ = int(input("tamZ: "))

    datos = np.fromfile(archivo, dtype=np.uint8)

    imagen = datos.reshape((tamZ, tamY, tamX))


# ----------------------------------------
# Programa principal
# ----------------------------------------
def main():

    global corte
    global radio
    global centro_x
    global centro_y

    global alfa
    global a,b,c,d

    leer_imagen()

    corte = int(input("Corte a visualizar: "))

    centro_x = int(input("Centro x: "))
    centro_y = int(input("Centro y: "))

    radio = float(input("Radio: "))

    alfa = float(input("Alfa (>1): "))

    print("\nCoeficientes")

    a = float(input("a = "))
    b = float(input("b = "))
    c = float(input("c = "))
    d = float(input("d = "))

    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

    glutInitWindowSize(tamX,tamY)

    glutCreateWindow(b"Transformacion Castel Angel")

    glClearColor(0,0,0,0)

    gluOrtho2D(0,tamX-1,0,tamY-1)

    forma_imagen()

    glutDisplayFunc(display)

    glutMainLoop()


if __name__ == "__main__":
    main()