from pyniryo import NiryoRobot, PoseObject
import math

# -------------------------------------------------
# CONEXIÓN
# -------------------------------------------------
robot_ip_address = '10.10.10.10'
# Connect to robot & calibrate
robot = NiryoRobot(robot_ip_address)

robot.calibrate_auto()
robot.clear_collision_detected()

# TCP DEL ROTULADOR
robot.set_tcp(
    TCP_X,
    TCP_Y,
    TCP_Z,
    TCP_ROLL,
    TCP_PITCH,
    TCP_YAW
)
robot.set_arm_max_velocity(45)


# Orientación del rotulador mientras dibuja
ROLL = 2.063
PITCH = 7.506
YAW = -3.209


# -------------------------------------------------
# CUADRADO
# -------------------------------------------------

def cuadrado():

    # Nos colocamos encima del papel
    robot.move_to_home_pose


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
            0.290, -0.006, 0.0005,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    robot.move(
        PoseObject(
            0.365, -0.006, 0.0005,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    # Línea derecha
    robot.move(
        PoseObject(
            0.365, -0.081, 0.0005,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    robot.move(
        PoseObject(
            0.365, -0.156, 0.0005,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    # Línea inferior
    robot.move(
        PoseObject(
            0.290, -0.156, 0.0005,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    robot.move(
        PoseObject(
            0.215, -0.156, 0.0005,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    # Lado izquierdo
    robot.move(
        PoseObject(
            0.215, -0.081, -0.003,
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

    robot.move_to_home_pose



# -------------------------------------------------
# TRIÁNGULO
# -------------------------------------------------

def triangulo():

    robot.move_to_home_pose


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
            0.290, -0.006, 0.0005,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    robot.move(
        PoseObject(
            0.365, -0.006, 0.001,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    # Diagonal
    robot.move(
        PoseObject(
            0.215, -0.156, -0.005,
            ROLL, PITCH, YAW
        ),
        linear=True
    )

    # Subimos por el lado izquierdo
    robot.move(
        PoseObject(
            0.215, -0.081, -0.003,
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

    robot.move_to_home_pose



# -------------------------------------------------
# CÍRCULO
# -------------------------------------------------

def circulo():

    robot.move_to_home_pose


    # Centro aproximado de vuestra zona de dibujo
    centro_x = 0.315
    centro_y = -0.106

    # 7.5 cm
    radio = 0.075

    # Número de puntos
    puntos = 50

    # Altura provisional
    z = 0.

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

        robot.move_to_home_pose



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


