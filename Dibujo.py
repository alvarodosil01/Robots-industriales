from pyniryo import NiryoRobot, PoseObject
import math


# -------------------------------------------------
# CONEXIÓN
# -------------------------------------------------

IP_ROBOT = "IP_DEL_ROBOT"



# -------------------------------------------------
# POSE DE SEGURIDAD
# -------------------------------------------------

POSE_SEGURA = PoseObject(
    0.105,
    -0.002,
    0.140,
    0.035,
    0.635,
    -0.042
)


# Orientación del rotulador mientras dibuja
ROLL = 2.063
PITCH = 7.506
YAW = -3.209


# -------------------------------------------------
# CUADRADO
# -------------------------------------------------

def cuadrado():

    # Nos colocamos encima del papel
    robot.move(POSE_SEGURA)

    # Primer punto
    robot.move(
        PoseObject(
            0.215, -0.006, 0.0005,
            ROLL, PITCH, YAW
        )
    )

    # Línea superior
    robot.move(
        PoseObject(
            0.315, -0.006, 0.0005,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    robot.move(
        PoseObject(
            0.415, -0.006, 0.0005,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    # Línea derecha
    robot.move(
        PoseObject(
            0.415, -0.106, 0.0005,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    robot.move(
        PoseObject(
            0.415, -0.206, 0.0005,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    # Línea inferior
    robot.move(
        PoseObject(
            0.315, -0.206, 0.0005,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    robot.move(
        PoseObject(
            0.215, -0.206, 0.0005,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    # Lado izquierdo
    robot.move(
        PoseObject(
            0.215, -0.106, -0.003,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    robot.move(
        PoseObject(
            0.215, -0.006, -0.003,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    robot.move(POSE_SEGURA)


# -------------------------------------------------
# TRIÁNGULO
# -------------------------------------------------

def triangulo():

    robot.move(POSE_SEGURA)

    # Primer vértice
    robot.move(
        PoseObject(
            0.215, -0.006, 0.000,
            ROLL, PITCH, YAW
        )
    )

    # Línea superior
    robot.move(
        PoseObject(
            0.315, -0.006, 0.0005,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    robot.move(
        PoseObject(
            0.415, -0.006, 0.001,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    # Diagonal
    robot.move(
        PoseObject(
            0.215, -0.206, -0.005,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    # Subimos por el lado izquierdo
    robot.move(
        PoseObject(
            0.215, -0.106, -0.003,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    robot.move(
        PoseObject(
            0.215, -0.006, -0.003,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    robot.move(POSE_SEGURA)


# -------------------------------------------------
# CÍRCULO
# -------------------------------------------------

def circulo():

    robot.move(POSE_SEGURA)

    # Centro aproximado de vuestra zona de dibujo
    centro_x = 0.315
    centro_y = -0.106

    # 7.5 cm
    radio = 0.075

    # Número de puntos
    puntos = 50

    # Altura provisional
    z = -0.001

    for i in range(puntos + 1):

        angulo = 2 * math.pi * i / puntos

        x = centro_x + radio * math.cos(angulo)
        y = centro_y + radio * math.sin(angulo)

        pose = PoseObject(
            x,
            y,
            z,
            ROLL,
            PITCH,
            YAW
        )

        # El primer punto lo hacemos STANDARD
        if i == 0:
            robot.move(pose)

        # Los demás LINEAR
        else:
            robot.move(pose, linear=True)

    robot.move(POSE_SEGURA)


# -------------------------------------------------
# PROGRAMA PRINCIPAL
# -------------------------------------------------

if __name__ == "__main__":
    robot = NiryoRobot(IP_ROBOT)
    try:
        robot.calibrate_auto()
        # Porcentaje de la velocidad máxima del brazo.
        robot.set_arm_max_velocity(45)

        figura = input(
            "¿Qué quieres dibujar? "
            "(cuadrado / triangulo / circulo): "
        ).lower()


        if figura == "cuadrado":
            cuadrado()

        elif figura == "triangulo":
            triangulo()

        elif figura == "circulo":
            circulo()

        else:
            print("Figura no válida")


    finally:
        robot.close_connection()


