# Tarea 3 - Visualizador de pila de imágenes médicas en formato crudo (.raw)

import sys
import os
import time
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Variables globales
tamX = 0             # Tamaño en pixeles en X (columnas)
tamY = 0             # Tamaño en pixeles en Y (renglones)
tamZ = 0             # Número de cortes (imágenes) en Z
bytes_por_pixel = 1  # Longitud del pixel en bytes: 1 (uint8) o 2 (uint16)
fp = ""              # Ruta del archivo .raw
imagen = None        # Arreglo numpy 3D con la pila: índices [z, y, x]
corte_actual = 0     # Índice del corte que se está mostrando actualmente
val_max_global = 1.0 # Valor máximo para normalización de intensidad

INTERVALO_MS = 100   # Retardo entre cortes en ms (= time.sleep(0.1) del Ejemplo 4)


# Normalización de la ruta del archivo
def normalizar_ruta(ruta):
    """
    Limpia la ruta que escribe el usuario:
      - Elimina comillas simples o dobles que VS Code/Explorer pegan al copiar.
      - Convierte barras invertidas a la forma que acepta Python en Windows.
      - Resuelve rutas relativas respecto al directorio de trabajo actual.
    """
    ruta = ruta.strip().strip('"').strip("'")
    ruta = os.path.normpath(ruta)   # normaliza separadores y '..' etc.
    return ruta


# Detección automática de bytes por pixel
def detectar_bytes_por_pixel(tam_real, pixeles_totales):
    """
    Divide el tamaño real del archivo entre el total de pixeles.
    Si el resultado es 1 o 2 lo retorna; de lo contrario retorna None
    para que el usuario lo especifique manualmente.
    """
    for bpp in (1, 2):
        if tam_real == pixeles_totales * bpp:
            return bpp
    return None


# Lectura del archivo crudo
def leer_imagen():
    """
    Lee el archivo .raw y lo almacena en el arreglo numpy global 'imagen'.
    Valida existencia, tamaño y coherencia con las dimensiones dadas.
    """
    global imagen, val_max_global, bytes_por_pixel

    # --- Validar existencia del archivo ---
    if not os.path.isfile(fp):
        # Mostrar ayuda para diagnosticar el problema de ruta
        print("\nError: No se encontró el archivo.")
        print(f"  Ruta buscada : {fp}")
        print(f"  Directorio actual: {os.getcwd()}")
        print("  Sugerencias:")
        print("    - Usa la ruta completa, p.ej.:  C:\\Users\\PC\\imagen.raw")
        print("    - O copia el archivo a la misma carpeta del script y escribe")
        print("      solo el nombre:  imagen.raw")
        sys.exit(1)

    tam_real = os.path.getsize(fp)
    pixeles_totales = tamX * tamY * tamZ

    # --- Detectar bytes por pixel automáticamente si es posible ---
    bpp_auto = detectar_bytes_por_pixel(tam_real, pixeles_totales)
    if bpp_auto is not None:
        bytes_por_pixel = bpp_auto
        tipo = 'uint8' if bytes_por_pixel == 1 else 'uint16'
        print(f"\nBytes por pixel detectados automáticamente: "
              f"{bytes_por_pixel} ({tipo})")
    else:
        # El tamaño no coincide con 1 ni con 2 bytes — informar al usuario
        print("\nError: No se pudo determinar bytes por pixel automáticamente.")
        print(f"  Tamaño real del archivo : {tam_real:,} bytes")
        print(f"  Píxeles totales (X*Y*Z) : {pixeles_totales:,}")
        print(f"  Esperado para 1 byte    : {pixeles_totales:,} bytes")
        print(f"  Esperado para 2 bytes   : {pixeles_totales * 2:,} bytes")
        print("  Verifique que tamX, tamY y tamZ sean correctos.")
        sys.exit(1)

    # --- Determinar tipo de dato numpy ---
    dtype = np.uint8 if bytes_por_pixel == 1 else np.uint16

    # --- Leer el archivo completo ---
    try:
        t_inicio = time.time()
        with open(fp, 'rb') as f:
            datos = np.frombuffer(f.read(), dtype=dtype)
        t_fin = time.time()
    except IOError as e:
        print(f"\nError al leer el archivo: {e}")
        sys.exit(1)

    # --- Reorganizar en arreglo 3D (z, y, x) con orden C ---
    # imagen[z, y, x] == índice plano x + tamX*y + tamX*tamY*z
    imagen = datos.reshape((tamZ, tamY, tamX))

    # --- Calcular valor máximo para normalización ---
    if bytes_por_pixel == 1:
        val_max_global = 255.0
    else:
        val_max_real = float(imagen.max())
        val_max_global = val_max_real if val_max_real > 0 else 65535.0

    print(f"Archivo leído en {t_fin - t_inicio:.2f} s: {os.path.basename(fp)}")
    print(f"  Dimensiones : {tamX} x {tamY} x {tamZ} pixeles")
    print(f"  Valor mín.  : {imagen.min()}  |  Valor máx.: {imagen.max()}")
    print(f"  Normalización con val_max = {val_max_global:.0f}")


# Construcción de listas de despliegue OpenGL
def forma_listas():
    """
    Crea una lista de despliegue (glNewList) por cada corte z.
    Cada lista dibuja el corte con GL_POINTS en escala de grises.
    """
    print("\nConstruyendo listas de despliegue OpenGL...")

    for z in range(tamZ):
        glNewList(z + 1, GL_COMPILE)  # listas numeradas desde 1
        glBegin(GL_POINTS)
        for y in range(tamY):
            for x in range(tamX):
                intensidad = float(imagen[z, y, x]) / val_max_global
                glColor3f(intensidad, intensidad, intensidad)
                # Invertir eje Y: renglón 0 del archivo = parte superior
                glVertex2i(x, tamY - 1 - y)
        glEnd()
        glEndList()

        if (z + 1) % 10 == 0 or z == tamZ - 1:
            print(f"  Corte {z + 1:4d} / {tamZ} procesado.")

    print("Listas de despliegue construidas.\n")


# Callbacks de GLUT
def display():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glOrtho(0, tamX - 1, 0, tamY - 1, 0, 1)
    glCallList(corte_actual + 1)
    glutSwapBuffers()


def timer(value):
    global corte_actual
    corte_actual = (corte_actual + 1) % tamZ
    glutPostRedisplay()
    glutTimerFunc(INTERVALO_MS, timer, 0)


def teclado(key, x, y):
    if key in (b'\x1b', b'q', b'Q'):
        print("Saliendo del visualizador.")
        sys.exit(0)


# Entrada de datos del usuario
def pedir_entero(mensaje, minimo=1):
    while True:
        try:
            valor = int(input(mensaje))
            if valor < minimo:
                print(f"  El valor debe ser al menos {minimo}.")
            else:
                return valor
        except ValueError:
            print("  Ingrese un número entero válido.")


# Función principal
def main():
    global fp, tamX, tamY, tamZ, corte_actual

    print("=" * 60)
    print("  Visualizador de imágenes médicas en formato crudo (.raw)")
    print("  Presione 'q' o Escape dentro de la ventana para salir.")
    print("=" * 60)
    print()
    print("Consejo para la ruta: puedes pegar la ruta completa del archivo,")
    print('por ejemplo:  C:\\Users\\PC\\Documentos\\imagen.raw')
    print("o arrastrar el archivo al terminal para obtener su ruta.")
    print()

    # Ruta del archivo (se limpia automáticamente)
    fp = normalizar_ruta(input("Ruta del archivo .raw: "))

    tamX = pedir_entero("Tamaño en X (columnas, pixeles)  : ")
    tamY = pedir_entero("Tamaño en Y (renglones, pixeles) : ")
    tamZ = pedir_entero("Número de cortes en Z (imágenes) : ")

    # Los bytes por pixel se detectan solos; no se pregunta al usuario

    # --- Leer la pila ---
    leer_imagen()

    # --- Inicializar GLUT ---
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowPosition(100, 100)
    glutInitWindowSize(tamX, tamY)
    glutCreateWindow(f"Imagenes medicas - {os.path.basename(fp)}".encode())

    # --- Construir listas (requiere contexto OpenGL activo) ---
    forma_listas()

    # --- Registrar callbacks ---
    glutDisplayFunc(display)
    glutKeyboardFunc(teclado)
    glutTimerFunc(INTERVALO_MS, timer, 0)

    corte_actual = 0
    print(f"Desplegando {tamZ} cortes.")
    glutMainLoop()


if __name__ == "__main__":
    main()
