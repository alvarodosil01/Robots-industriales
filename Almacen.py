# Almacen de 9 huecos: DI5 activa el guardado y el boton 1 solicita una pieza.
from pyniryo import NiryoRobot, PoseObject, PinID, PinState


robot_ip_address = '10.10.12.122'

# Orientacion tomada de la practica anterior; comprobar con la nueva pieza.
Raw = 1.257
Pitch = 1.492
Yaw = 1.298
offset_aproximacion = 0.030
altura_traslado = 0.150  # Altura absoluta de traslado: 15 cm.

# Alturas de contacto medidas con la herramienta, en metros.
altura_origen = 0.052  # Recogida en la plataforma del sensor.
altura_final =0.009 # Colocacion/recogida en los 9 huecos del almacen.
altura_salida = 0.009  # Colocacion en la plataforma de salida.

# Posiciones [x, y, z], en metros.
pentrada = [-0.0082, -0.2615, altura_origen]
psalida = [0.0071, 0.1925, altura_salida]

# Referencia: hueco 5. Pasos medios calculados a partir de los puntos actuales.
pcentro_almacen = [0.28, -0.002, altura_final]
paso_x = 0.0633  # Metros entre columnas; X disminuye hacia la derecha.
paso_y = 0.0992  # Metros entre filas; Y aumenta hacia abajo.

# Disposicion: 1 2 3 / 4 5 6 / 7 8 9. Una sola pieza por hueco.
# False: libre. True: ocupado. Al arrancar se supone que esta vacio.
almacen = {}
for fila in range(3):
    for columna in range(3):
        numero = fila * 3 + columna + 1
        almacen[numero] = {
            "posicion": [
                pcentro_almacen[0] + (1 - columna) * paso_x,
                pcentro_almacen[1] + (fila - 1) * paso_y,
                pcentro_almacen[2],
            ],
            "ocupado": False,
        }
# Si hay piezas al arrancar, marcar sus huecos aqui; por ejemplo:
# almacen[5]["ocupado"] = True

SENSOR_ENTRADA = PinID.DI5
# Cambiar a LOW si el sensor detecta la pieza con nivel bajo.
PIEZA_PRESENTE = PinState.LOW
BOTON_SACAR = PinID.DI1  # Boton 1, igual que en Figuras2.py.
PULSADO = PinState.HIGH

LUZ_DISPONIBLE = PinID.DO3  # Verde.
LUZ_TRABAJANDO = PinID.DO1  # Rojo.
LUZ_AMARILLA = PinID.DO2   # Se mantiene apagada.
LUCES = (LUZ_DISPONIBLE, LUZ_TRABAJANDO, LUZ_AMARILLA)


def pose_con_offset(posicion, offset_z=0.0):
    x, y, z = posicion
    return PoseObject(x, y, z + offset_z, Raw, Pitch, Yaw)


def pose_traslado(posicion):
    x, y, _ = posicion
    return PoseObject(x, y, altura_traslado, Raw, Pitch, Yaw)


def trasladar(robot, origen, destino):
    # Acercarse por arriba, abrir la pinza y bajar para recoger.
    robot.set_arm_max_velocity(55)
    robot.move(pose_con_offset(origen, offset_aproximacion))
    robot.release_with_tool()
    robot.set_arm_max_velocity(45)
    robot.move(pose_con_offset(origen), linear=True)
    robot.grasp_with_tool()
    robot.wait(1)

    # Subir verticalmente hasta 15 cm antes de trasladar la pieza.
    robot.move(pose_traslado(origen), linear=True)
    robot.set_arm_max_velocity(55)
    robot.move(pose_traslado(destino))

    # Bajar, soltar y retirarse antes de volver a home.
    robot.set_arm_max_velocity(35)
    robot.move(pose_con_offset(destino, offset_aproximacion), linear=True)
    robot.move(pose_con_offset(destino), linear=True)
    robot.release_with_tool()
    robot.wait(1)
    robot.move(pose_traslado(destino), linear=True)
    robot.move_to_home_pose()
    robot.grasp_with_tool()


def encender_luz(robot, luz):
    for salida in LUCES:
        if salida != luz:
            robot.digital_write(salida, PinState.LOW)
    robot.digital_write(luz, PinState.HIGH)


def disponible(robot):
    encender_luz(robot, LUZ_DISPONIBLE)
    print("Disponible", flush=True)


def trabajando(robot):
    encender_luz(robot, LUZ_TRABAJANDO)
    print("Trabajando", flush=True)


def buscar_hueco(ocupado):
    # Seleccionar el primer hueco con el estado solicitado, del 1 al 9.
    for numero, datos in almacen.items():
        if datos["ocupado"] == ocupado:
            return numero
    return None


def hay_pieza_entrada(robot):
    return robot.digital_read(SENSOR_ENTRADA) == PIEZA_PRESENTE


def guardar_pieza(robot):
    if not hay_pieza_entrada(robot):
        print("Entrada vacia: DI5 no detecta ninguna pieza.", flush=True)
        return False
    numero = buscar_hueco(False)
    if numero is None:
        print("Almacen lleno: no se puede guardar otra pieza.", flush=True)
        return False
    # Guardar automaticamente cuando DI5 detecta una pieza y hay hueco libre.
    trabajando(robot)
    trasladar(robot, pentrada, almacen[numero]["posicion"])
    almacen[numero]["ocupado"] = True
    print(f"Pieza guardada en el hueco {numero}.", flush=True)
    disponible(robot)
    return True


def sacar_pieza(robot):
    numero = buscar_hueco(True)
    if numero is None:
        print("Almacen vacio: no hay piezas para sacar.", flush=True)
        return
    # La bandeja de salida debe estar libre antes de solicitar una pieza.
    trabajando(robot)
    trasladar(robot, almacen[numero]["posicion"], psalida)
    almacen[numero]["ocupado"] = False
    print(f"Pieza retirada del hueco {numero}.", flush=True)
    disponible(robot)


if __name__ == "__main__":
    robot = NiryoRobot(robot_ip_address)
    try:
        for luz in LUCES:
            robot.digital_write(luz, PinState.LOW)
        robot.calibrate_auto()
        robot.update_tool()
        robot.set_arm_max_velocity(30)
        robot.move_to_home_pose()
        print('Listo: DI5 guardado automatico. Pulsa el boton 1 (DI1) para sacar una pieza.', flush=True)
        disponible(robot)
        entrada_lista = True
        aviso_lleno = False
        # Al arrancar, esperar a detectar el boton suelto antes de aceptar una orden.
        boton_listo = False

        while True:
            # Una retirada por pulsacion, sin bloquear la vigilancia de DI5.
            if robot.digital_read(BOTON_SACAR) != PULSADO:
                robot.wait(0.05)  # Antirrebote sencillo al soltar.
                if robot.digital_read(BOTON_SACAR) != PULSADO:
                    boton_listo = True
            elif boton_listo:
                boton_listo = False
                sacar_pieza(robot)

            if not hay_pieza_entrada(robot):
                entrada_lista = True
            elif entrada_lista and buscar_hueco(False) is not None:
                if guardar_pieza(robot):
                    # Si sigue detectando, esperar a que se libere antes de otra recogida.
                    entrada_lista = not hay_pieza_entrada(robot)

            lleno = buscar_hueco(False) is None
            if lleno and not aviso_lleno:
                print('Almacen lleno (9/9). Pulsa el boton 1 para liberar un hueco.', flush=True)
            aviso_lleno = lleno
            robot.wait(0.05)
    finally:
        try:
            for luz in LUCES:
                try:
                    robot.digital_write(luz, PinState.LOW)
                except Exception as error:
                    print(f"No se pudo apagar {luz}: {error}")
        finally:
            robot.close_connection()
