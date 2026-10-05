from pyniryo import NiryoRobot, PoseObject
import math

# -------------------------------------------------
# CONEXIÓN
# -------------------------------------------------
robot_ip_address = '10.10.13.190'


# Orientación del rotulador mientras dibuja
ROLL = 0.035
PITCH = 0.635
YAW = -0.042


# Cuadrado y triángulo: referencia superior de la captura.
# Incrementos de 0.075 m: dos tramos por lado (0.15 m).
# Z = 0.17 m; orientación del punto de referencia.
# Inicio superior izquierdo: abajo = -X, derecha = -Y.
# Cuadrado: abajo, derecha, arriba, izquierda (plano XY).

def cuadrado(robot):
    # Inicio del dibujo.

    robot.move(
        PoseObject(
            0.412, 0.089, 0.14,
            0.092, -0.041, 0.118
        )
    )

    robot.move(
        PoseObject(
            0.337, 0.089, 0.13,
            0.092, -0.041, 0.118
        ),
        linear=True
    )

    robot.move(
        PoseObject(
            0.262, 0.089, 0.13,
            0.092, -0.041, 0.118
        ),
        linear=True
    )

    robot.move(
        PoseObject(
            0.262, 0.014, 0.13,
            0.092, -0.041, 0.118
        ),
        linear=True
    )

    robot.move(
        PoseObject(
            0.262, -0.061, 0.14,
            0.092, -0.041, 0.118
        ),
        linear=True
    )

    robot.move(
        PoseObject(
            0.337, -0.061, 0.14,
            0.092, -0.041, 0.118
        ),
        linear=True
    )

    robot.move(
        PoseObject(
            0.412, -0.061, 0.14,
            0.092, -0.041, 0.118
        ),
        linear=True
    )

    robot.move(
        PoseObject(
            0.412, 0.014, 0.14,
            0.092, -0.041, 0.118
        ),
        linear=True
    )

    robot.move(
        PoseObject(
            0.412, 0.089, 0.14,
            0.092, -0.041, 0.118
        ),
        linear=True
    )

    robot.move_to_home_pose()


def triangulo(robot):
    # Inicio del dibujo.

    robot.move(
        PoseObject(
            0.412, 0.089, 0.14,
            0.092, -0.041, 0.118
        )
    )

    robot.move(
        PoseObject(
            0.337, 0.089, 0.14,
            0.092, -0.041, 0.118
        ),
        linear=True
    )

    robot.move(
        PoseObject(
            0.262, 0.089, 0.13,
            0.092, -0.041, 0.118
        ),
        linear=True
    )

    robot.move(
        PoseObject(
            0.412, -0.061, 0.14,
            0.092, -0.041, 0.118
        ),
        linear=True
    )

    robot.move(
        PoseObject(
            0.412, 0.014, 0.14,
            0.092, -0.041, 0.118
        ),
        linear=True
    )

    robot.move(
        PoseObject(
            0.412, 0.089, 0.14,
            0.092, -0.041, 0.118
        ),
        linear=True
    )

    robot.move_to_home_pose()


# -------------------------------------------------
# CÍRCULO
# -------------------------------------------------

def circulo(robot):
    inicio_x = 0.397
    inicio_y = 0.028
    z = 0.14

    roll = 0.031
    pitch = 0.037
    yaw = -0.013

    radio = 0.075
    centro_x = inicio_x - radio
    centro_y = inicio_y
    puntos = 150

    for i in range(puntos + 1):
        angulo = 2 * math.pi * i / puntos

        if i == 0 or i == puntos:
            x = inicio_x
            y = inicio_y
        else:
            x = centro_x + radio * math.cos(angulo)
            y = centro_y + radio * math.sin(angulo)

        pose = PoseObject(x, y, z, roll, pitch, yaw)

        if i == 0:
            robot.move(pose)
        else:
            robot.move(pose, linear=True)

    robot.move_to_home_pose()


# -------------------------------------------------
# PROGRAMA PRINCIPAL
# -------------------------------------------------

if __name__ == "__main__":
    robot = NiryoRobot(robot_ip_address)
    try:
        robot.set_arm_max_velocity(40)
        robot.set_tcp(0.022, 0, 0.070, 0, 0, 0)
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


