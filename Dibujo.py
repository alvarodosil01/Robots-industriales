# Programa Tarea01.py
# Etapa. Dibujo de figuras geométricas con el robot Niryo
# Realizado por: Alvaro Dosil, Lucia Pardo , Santiago Santos , Ignacio 
# Fecha: 08/10/2026

# Bibliotecas y módulos
from pyniryo import NiryoRobot, PoseObject
import math

# -------------------------------------------------
# Variables y constantes
# CONEXIÓN
# -------------------------------------------------
robot_ip_address = '10.10.13.190'



# Definiciones de Clases, Funciones y Procedimientos

# Cuadrado y triángulo: referencia superior de la captura.
# Incrementos de 0.075 m: dos tramos por lado (0.15 m).
# Alturas Z de 0.13 y 0.14 m según el punto; orientación fija del rotulador.
# Inicio superior izquierdo: abajo = -X, derecha = -Y.
# Cuadrado: abajo, derecha, arriba, izquierda (plano XY).

def cuadrado(robot):
    # Dibuja los cuatro lados del cuadrado, pasando por un punto medio en cada lado.
    # PoseObject contiene la posición X, Y, Z (metros) y la orientación (radianes).
    # linear=True realiza cada tramo en línea recta hasta la pose indicada.
    # Los números con .5 señalan puntos medios; los enteros, finales de lado.

    robot.move(PoseObject(0.412, 0.089, 0.14, 0.092, -0.041, 0.118))  # Posición inicial

    robot.move(PoseObject(0.337, 0.089, 0.13, 0.092, -0.041, 0.118), linear=True)  # Línea 1.5

    robot.move(PoseObject(0.262, 0.089, 0.13, 0.092, -0.041, 0.118), linear=True)  # Línea 1

    robot.move(PoseObject(0.262, 0.014, 0.13, 0.092, -0.041, 0.118), linear=True)  # Línea 2.5

    robot.move(PoseObject(0.262, -0.061, 0.14, 0.092, -0.041, 0.118), linear=True)  # Línea 2

    robot.move(PoseObject(0.337, -0.061, 0.14, 0.092, -0.041, 0.118), linear=True)  # Línea 3.5

    robot.move(PoseObject(0.412, -0.061, 0.14, 0.092, -0.041, 0.118), linear=True)  # Línea 3

    robot.move(PoseObject(0.412, 0.014, 0.14, 0.092, -0.041, 0.118), linear=True)  # Línea 4.5

    robot.move(PoseObject(0.412, 0.089, 0.14, 0.092, -0.041, 0.118), linear=True)  # Línea 4

    robot.move_to_home_pose()


def triangulo(robot):
    # Dibuja los tres lados del triángulo y termina en el punto de partida.
    # Los lados 1 y 3 tienen un punto medio; el lado 2 se recorre directamente.
    # Mantiene la orientación del rotulador y une las poses con movimientos rectos.

    robot.move(PoseObject(0.412, 0.089, 0.14, 0.092, -0.041, 0.118))  # Posición inicial

    robot.move(PoseObject(0.337, 0.089, 0.14, 0.092, -0.041, 0.118), linear=True)  # Línea 1.5

    robot.move(PoseObject(0.262, 0.089, 0.13, 0.092, -0.041, 0.118), linear=True)  # Línea 1

    robot.move(PoseObject(0.412, -0.061, 0.14, 0.092, -0.041, 0.118), linear=True)  # Línea 2

    robot.move(PoseObject(0.412, 0.014, 0.14, 0.092, -0.041, 0.118), linear=True)  # Línea 3.5

    robot.move(PoseObject(0.412, 0.089, 0.14, 0.092, -0.041, 0.118), linear=True)  # Línea 3

    robot.move_to_home_pose()


# -------------------------------------------------
# CÍRCULO
# -------------------------------------------------

def circulo(robot):
    # Calcula una circunferencia en el plano XY y reúne sus poses en una trayectoria.
    # El punto de partida está en el extremo de mayor X; Z fija la altura en metros.
    inicio_x = 0.397
    inicio_y = 0.028
    z = 0.14

    # Ángulos de orientación del rotulador, en radianes, constantes durante el dibujo.
    roll = 0.031
    pitch = 0.037
    yaw = -0.013

    # Radio de 7.5 cm. El centro está un radio hacia -X desde el punto inicial.
    radio = 0.075
    centro_x = inicio_x - radio
    centro_y = inicio_y
    # Divide la vuelta en 150 tramos; se guardan 151 poses contando el cierre.
    puntos = 150
    trayectoria = []

    for i in range(puntos + 1):
        # Convierte el índice en un ángulo de 0 a 2*pi radianes (una vuelta completa).
        angulo = 2 * math.pi * i / puntos

        # Usa las mismas coordenadas al empezar y terminar para cerrar el círculo.
        if i == 0 or i == puntos:
            x = inicio_x
            y = inicio_y
        else:
            # Coseno y seno dan los desplazamientos X e Y respecto al centro.
            x = centro_x + radio * math.cos(angulo)
            y = centro_y + radio * math.sin(angulo)

        # Combina cada posición calculada con la altura y orientación constantes.
        pose = PoseObject(x, y, z, roll, pitch, yaw)

        # Movimiento anterior, punto a punto:
        # if i == 0:
        #     robot.move(pose)
        # else:
        #     robot.move(pose, linear=True)

        # Añade la pose a la lista; aquí todavía no se mueve el robot.
        trayectoria.append(pose)

    # Primero coloca el robot en el punto de partida de la circunferencia.
    robot.move(trayectoria[0])
    # Ejecuta todas las poses juntas, con 1 mm de suavizado entre puntos.
    # Esto reduce las frenadas de los movimientos separados y puede variar algo el trazo.
    robot.execute_trajectory(trayectoria, dist_smoothing=0.001)

    # Una vez completado el círculo, regresa a la posición home del robot.
    robot.move_to_home_pose()


# -------------------------------------------------
# PROGRAMA PRINCIPAL
# -------------------------------------------------

if __name__ == "__main__":
    robot = NiryoRobot(robot_ip_address)
    try:
        robot.set_arm_max_velocity(40)
        robot.set_tcp(0.022, 0, 0.074, 0, 0, 0)
        robot.calibrate_auto()
        robot.move_to_home_pose()
      
        # Porcentaje de la velocidad máxima del brazo.


        figura = input(
            "¿Qué quieres dibujar? "
            "(cuadrado / triangulo / circulo): "
        ).strip().lower()


        if figura == "cuadrado":
            cuadrado(robot)

        elif figura == "triangulo":
            triangulo(robot)

        elif figura == "circulo":
            circulo(robot)

        else:
            print("Figura no válida")


    finally:
        robot.close_connection()


