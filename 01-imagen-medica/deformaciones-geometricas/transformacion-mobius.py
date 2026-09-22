# --------------------------------------------------------
# TAREA 5
# Transformación de Möbius modificada recursiva
# aplicada a imágenes médicas (.raw)
# --------------------------------------------------------

import sys
import os
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# --------------------------------------------------------
# Variables globales
# --------------------------------------------------------

tamX = 0
tamY = 0
tamZ = 0

imagen = None

corte = 0

# coeficientes de Möbius
a = 0.1 + 0j
b = 1e4 + 0j
c = 1 + 5j
d = 1 + 0j

orden = 30

ESC = 255.0


# --------------------------------------------------------
# Lectura del archivo RAW
# --------------------------------------------------------
def leer_imagen():

    global imagen

    archivo = input("Nombre del archivo .raw: ")

    if not os.path.isfile(archivo):
        print("No existe el archivo")
        sys.exit()

    global tamX, tamY, tamZ

    tamX = int(input("Tamaño X: "))
    tamY = int(input("Tamaño Y: "))
    tamZ = int(input("Número de imágenes Z: "))

    datos = np.fromfile(archivo, dtype=np.uint8)

    imagen = datos.reshape((tamZ, tamY, tamX))

    print("Imagen cargada correctamente")


# --------------------------------------------------------
# Transformación de Möbius modificada
# con valor absoluto
# --------------------------------------------------------
def moebius_recursiva(vectt, a, b, c, d, n):

    x = vectt[0]
    y = vectt[1]

    zx = complex(x, 0)
    zy = complex(y, 0)

    # transformación modificada con valor absoluto
    zx = abs((a*zx + b)/(c*zx + d))
    zy = abs((a*zy + b)/(c*zy + d))

    vectt[0] = zx
    vectt[1] = zy

    n -= 1

    if n > 0:
        moebius_recursiva(vectt, a, b, c, d, n)


# --------------------------------------------------------
# Construcción de la imagen deformada
# --------------------------------------------------------
def forma_imagen():

    global corte

    glNewList(1, GL_COMPILE)

    for y in range(tamY):

        for x in range(tamX):

            intensidad = imagen[corte, y, x]/ESC

            glColor3f(intensidad,
                      intensidad,
                      intensidad)

            punto = [float(x), float(y)]

            # autocomposición recursiva
            moebius_recursiva(punto,
                              a,
                              b,
                              c,
                              d,
                              orden)

            xt = int(punto[0])
            yt = int(punto[1])

            if 0 <= xt < tamX and 0 <= yt < tamY:

                glBegin(GL_POINTS)

                glVertex2i(xt, tamY-1-yt)

                glEnd()

    glEndList()


# --------------------------------------------------------
# Inicialización
# --------------------------------------------------------
def inicializa():

    glClearColor(0,0,0,0)

    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    gluOrtho2D(0,
               tamX-1,
               0,
               tamY-1)


# --------------------------------------------------------
# Display
# --------------------------------------------------------
def display():

    glClear(GL_COLOR_BUFFER_BIT)

    glCallList(1)

    glutSwapBuffers()


# --------------------------------------------------------
# Programa principal
# --------------------------------------------------------
def main():

    global corte
    global a,b,c,d
    global orden

    leer_imagen()

    corte = int(input("Corte a visualizar (0 a {}): ".format(tamZ-1)))

    print("\nCoeficientes de Möbius")

    ar = float(input("Parte real de a: "))
    ai = float(input("Parte imaginaria de a: "))

    br = float(input("Parte real de b: "))
    bi = float(input("Parte imaginaria de b: "))

    cr = float(input("Parte real de c: "))
    ci = float(input("Parte imaginaria de c: "))

    dr = float(input("Parte real de d: "))
    di = float(input("Parte imaginaria de d: "))

    a = complex(ar, ai)
    b = complex(br, bi)
    c = complex(cr, ci)
    d = complex(dr, di)

    orden = int(input("Orden de recursividad: "))

    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

    glutInitWindowSize(tamX, tamY)

    glutInitWindowPosition(100,100)

    glutCreateWindow(b"Tarea 5 - Transformacion de Moebius")

    inicializa()

    forma_imagen()

    glutDisplayFunc(display)

    glutMainLoop()


if __name__ == "__main__":
    main()