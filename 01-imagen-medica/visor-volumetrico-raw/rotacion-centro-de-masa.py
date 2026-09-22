# Tarea 4
# Rotación de una pila de imágenes médicas alrededor de su centro de masa

import sys
import os
import time
import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Variables globales
tamX = 0
tamY = 0
tamZ = 0

bytes_por_pixel = 1

fp = ""

imagen = None

corte_actual = 0

val_max_global = 1.0

angulo = 0.0

INTERVALO_MS = 100


#-------------------------------------------------------
def normalizar_ruta(ruta):

    ruta = ruta.strip().strip('"').strip("'")

    ruta = os.path.normpath(ruta)

    return ruta


#-------------------------------------------------------
def detectar_bytes_por_pixel(tam_real, pixeles_totales):

    for bpp in (1, 2):

        if tam_real == pixeles_totales * bpp:

            return bpp

    return None


#-------------------------------------------------------
def leer_imagen():

    global imagen
    global val_max_global
    global bytes_por_pixel

    if not os.path.isfile(fp):

        print("\nNo se encontró el archivo.")
        print(fp)

        sys.exit(1)

    tam_real = os.path.getsize(fp)

    pixeles_totales = tamX * tamY * tamZ

    bpp_auto = detectar_bytes_por_pixel(
        tam_real,
        pixeles_totales
    )

    if bpp_auto is None:

        print("No se pudo determinar el tamaño del pixel")

        sys.exit(1)

    bytes_por_pixel = bpp_auto

    if bytes_por_pixel == 1:

        dtype = np.uint8

    else:

        dtype = np.uint16

    try:

        with open(fp, 'rb') as f:

            datos = np.frombuffer(
                f.read(),
                dtype=dtype
            )

    except IOError:

        print("Error de lectura")

        sys.exit(1)

    imagen = datos.reshape(
        (tamZ, tamY, tamX)
    )

    if bytes_por_pixel == 1:

        val_max_global = 255.0

    else:

        val_max_global = float(imagen.max())


#-------------------------------------------------------
def forma_listas():

    print("Construyendo listas...")

    for z in range(tamZ):

        glNewList(z + 1, GL_COMPILE)

        glBegin(GL_POINTS)

        for y in range(tamY):

            for x in range(tamX):

                intensidad = float(
                    imagen[z, y, x]
                ) / val_max_global

                glColor3f(
                    intensidad,
                    intensidad,
                    intensidad
                )

                glVertex2i(
                    x,
                    tamY - 1 - y
                )

        glEnd()

        glEndList()

    print("Listas construidas.")


#-------------------------------------------------------
def display():

    glClearColor(0.0,0.0,0.0,0.0)

    glClear(GL_COLOR_BUFFER_BIT)

    # MATRIZ DE PROYECCION
    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    glOrtho(
        0,
        tamX - 1,
        0,
        tamY - 1,
        0,
        1
    )

    # MATRIZ DE TRANSFORMACIONES
    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()

    # Trasladar al centro
    glTranslated(
        tamX / 2,
        tamY / 2,
        0
    )

    # Rotación alrededor del eje z
    glRotatef(
        angulo,
        0,
        0,
        1
    )

    # Regresar a la posición original
    glTranslated(
        -tamX / 2,
        -tamY / 2,
        0
    )

    glCallList(
        corte_actual + 1
    )

    glutSwapBuffers()


#-------------------------------------------------------
def timer(value):

    global corte_actual

    corte_actual = (corte_actual + 1) % tamZ

    glutPostRedisplay()

    glutTimerFunc(
        INTERVALO_MS,
        timer,
        0
    )


#-------------------------------------------------------
def teclado(key, x, y):

    if key == b'q' or key == b'Q' or key == b'\x1b':

        sys.exit()


#-------------------------------------------------------
def pedir_entero(mensaje):

    while True:

        try:

            valor = int(input(mensaje))

            if valor > 0:

                return valor

        except:

            pass


#-------------------------------------------------------
def main():

    global fp
    global tamX
    global tamY
    global tamZ
    global angulo

    print()

    fp = normalizar_ruta(
        input("Ruta del archivo RAW: ")
    )

    tamX = pedir_entero(
        "Tamano en X: "
    )

    tamY = pedir_entero(
        "Tamano en Y: "
    )

    tamZ = pedir_entero(
        "Numero de cortes Z: "
    )

    angulo = float(
        input(
            "Grado de rotacion: "
        )
    )

    leer_imagen()

    glutInit(sys.argv)

    glutInitDisplayMode(
        GLUT_DOUBLE |
        GLUT_RGB |
        GLUT_DEPTH
    )

    glutInitWindowPosition(
        100,
        100
    )

    glutInitWindowSize(
        tamX,
        tamY
    )

    glutCreateWindow(
        b"Tarea 4 - Rotacion del volumen"
    )

    forma_listas()

    glutDisplayFunc(
        display
    )

    glutKeyboardFunc(
        teclado
    )

    glutTimerFunc(
        INTERVALO_MS,
        timer,
        0
    )

    glutMainLoop()


#-------------------------------------------------------
if __name__ == "__main__":

    main()