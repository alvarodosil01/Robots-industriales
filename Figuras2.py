# Control de figuras mediante botones externos y luces de estado.
from pyniryo import NiryoRobot, PoseObject, PinID, PinState
from time import sleep

# Constantes, poses y movimientos incluidos en este archivo.
robot_ip_address = '10.10.15.89'

# Orientacion en radianes y alturas base en metros.
Raw = 1.257
Pitch = 1.492
Yaw = 1.298
altura_inicial = 0.005 #Altura inicial en la mesa
altura_destino = 0.063  #Alrua destino en un altura (en clase caja de folios)

# Incrementos de Z respecto a la posicion recibida, no alturas absolutas.
# Z final = Z base de la posicion + offset (todo en metros).
# Un offset de 0.030 eleva 3 cm; un offset de 0 mantiene la altura base.
offset_aproximacion = 0.030  # Origen: 0.005 + 0.030 = 0.035.
offset_elevacion = 0.085    # Origen: 0.005 + 0.085 = 0.090.
offset_traslado = 0.089     # Destino/intermedio: 0.061 + 0.089 = 0.150.
offset_retirada = 0.059     # Destino: 0.061 + 0.059 = 0.120.

# Posiciones X, Y, Z base. pi = origen; pf = destino alto.
picuadrado = [0.254, 0.044, altura_inicial]
pfcuadrado = [-0.057, -0.266, altura_destino]
pirombo = [0.254, -0.085, altura_inicial]
pfrombo = [0.026, -0.268, altura_destino]
picirculo = [0.259, -0.02, altura_inicial]
pfcirculo = [0.092, -0.268, altura_destino]
# Referencia Z del punto intermedio antes de sumar el incremento de traslado.
pintermedio = [0.00, -0.15, altura_destino]
# Orientacion del circulo en el destino, en radianes.
Raw_circulo = -0.945
Pitch_circulo = 1.494
Yaw_circulo = -0.8
# En la primera aproximacion al destino se conserva Pitch = 1.492.
# Las funciones de pose reciben una posicion y devuelven un objeto PoseObject.


# Definiciones de Clases, Funciones y Procedimientos

# Recogida y colocación del cuadrado con la pinza.
# Posiciones en metros y orientaciones en radianes.
# Los offsets se suman a la Z base de la posicion; no se acumulan entre movimientos.
# Verificar las poses con la herramienta y el TCP usados al enseñarlas.

# Crear una pose nueva sin modificar la lista de posicion original.
# El incremento es vertical respecto al eje Z del robot.
def pose_con_offset(posicion, offset_z=0.0, orientacion=(Raw, Pitch, Yaw)):
    # Leer la posicion base; no se usa la altura actual del robot.
    x, y, z = posicion
    roll, pitch, yaw = orientacion
    # Crear el objeto de destino. El movimiento ocurre al llamar a robot.move().
    return PoseObject(x, y, z + offset_z, roll, pitch, yaw)


def pose_base(posicion, orientacion=(Raw, Pitch, Yaw)):
    # Mantener la Z base para recoger o soltar la pieza, sin incremento.
    return pose_con_offset(posicion, 0.0, orientacion)


def pose_aproximacion(posicion, orientacion=(Raw, Pitch, Yaw)):
    # Preparar una pose 3 cm sobre el origen para acercarse o retirarse.
    return pose_con_offset(posicion, offset_aproximacion, orientacion)


def pose_elevacion(posicion, orientacion=(Raw, Pitch, Yaw)):
    # Preparar una pose 8,5 cm sobre el origen para levantar la pieza antes del traslado.
    return pose_con_offset(posicion, offset_elevacion, orientacion)


def pose_traslado(posicion, orientacion=(Raw, Pitch, Yaw)):
    # Sumar 8,9 cm a la Z base del destino o punto intermedio: Z final de 15 cm.
    return pose_con_offset(posicion, offset_traslado, orientacion)


def pose_retirada(posicion, orientacion=(Raw, Pitch, Yaw)):
    # Preparar una pose 5,9 cm sobre el destino para apartar la pinza tras soltar.
    return pose_con_offset(posicion, offset_retirada, orientacion)
# Cada nombre agrupa las posiciones y orientaciones de su figura.

figuras = {
    "cuadrado": {
        "origen": picuadrado, "destino": pfcuadrado,
        "orientacion": (Raw, Pitch, Yaw),
    },
    "circulo": {
        "origen": picirculo, "destino": pfcirculo,
        "orientacion": (Raw_circulo, Pitch_circulo, Yaw_circulo),
        "orientacion_aproximacion": (Raw_circulo, Pitch, Yaw_circulo),
    },
    "rombo": {
        "origen": pirombo, "destino": pfrombo,
        "orientacion": (Raw, Pitch, Yaw),
    },
}

def llevar(robot, datos):
    # 1. Acercarse por encima de la pieza y abrir la pinza.
    robot.set_arm_max_velocity(100)
    robot.move(pose_aproximacion(datos["origen"]))
    robot.release_with_tool()   
    # 2. Bajar verticalmente y cerrar para coger la pieza.
    robot.set_arm_max_velocity(60)
    robot.move(pose_base(datos["origen"]), linear=True)
    robot.grasp_with_tool()     
    robot.wait(1)
    # 3. Levantar antes de trasladar por el punto intermedio.
    robot.set_arm_max_velocity(75)
    robot.move(pose_elevacion(datos["origen"]), linear=True)
    robot.move(pose_traslado(pintermedio))
    # El circulo conserva su orientacion especial al aproximarse al destino.
    orientacion_aproximacion = datos.get("orientacion_aproximacion", datos["orientacion"])
    robot.move(pose_traslado(datos["destino"], orientacion_aproximacion))
    # # 4. Bajar verticalmente en el destino y soltar.
    robot.move(pose_base(datos["destino"], datos["orientacion"]), linear=True)
    robot.release_with_tool()
    robot.wait(1)
    # # 5. Retirarse hasta la altura de aproximación con la pinza abierta.
    robot.move(pose_retirada(datos["destino"], datos["orientacion"]), linear=True)
    robot.grasp_with_tool()
    robot.move_to_home_pose()
    
def devolver(robot, datos):
    # 6. Volver al destino, abrir, bajar y recoger la pieza.
    robot.set_arm_max_velocity(60)
    robot.move(pose_traslado(pintermedio))
    robot.move(pose_traslado(datos["destino"], datos["orientacion"]))
    robot.release_with_tool()
    robot.move(pose_base(datos["destino"], datos["orientacion"]), linear=True)
    robot.grasp_with_tool()
    robot.wait(1)

    # 7. Subir y regresar por el punto intermedio hasta encima del origen.
    robot.move(pose_traslado(datos["destino"], datos["orientacion"]), linear=True)
    robot.move(pose_traslado(pintermedio))
    robot.move(pose_elevacion(datos["origen"]))

    # 8. Bajar, dejar en la posición inicial y subir con la pinza abierta.
    robot.move(pose_base(datos["origen"]), linear=True)
    robot.release_with_tool()
    robot.wait(1)
    robot.move(pose_aproximacion(datos["origen"]), linear=True)
    robot.grasp_with_tool() 
    robot.move_to_home_pose()

# Cambiar estos pines si el cableado utiliza otras entradas/salidas.
# Botones: 1 cuadrado, 2 circulo y 3 rombo.
BOTON_CUADRADO = PinID.DI1
BOTON_CIRCULO = PinID.DI2
BOTON_ROMBO = PinID.DI3

# Estados: DO1 rojo (trabajando), DO3 verde (disponible).
# DO2 amarillo se mantiene apagado.
LUZ_DISPONIBLE = PinID.DO3 
LUZ_TRABAJANDO = PinID.DO1
LUZ_AMARILLA = PinID.DO2
# Se supone que al pulsar llega HIGH y que HIGH enciende la luz.
PULSADO = PinState.HIGH


# digital_write cambia una salida: HIGH enciende y LOW apaga.
def encender_luz(robot, luz):
    # Apagar las otras luces antes de encender la seleccionada.
    for salida in (LUZ_DISPONIBLE, LUZ_TRABAJANDO, LUZ_AMARILLA):
        if salida != luz:
            robot.digital_write(salida, PinState.LOW)
    robot.digital_write(luz, PinState.HIGH)


# Verde: el movimiento ha terminado. Para otra orden hay que soltar los botones.
def disponible(robot):
    encender_luz(robot, LUZ_DISPONIBLE)  # DO3: verde.
    print("Disponible", flush=True)


# Rojo durante los movimientos de una figura seleccionada con un boton.
def trabajando(robot):
    encender_luz(robot, LUZ_TRABAJANDO)  # DO1: rojo.
    print("Trabajando", flush=True)


# digital_read consulta el estado de cada entrada digital.
def esperar_botones_sueltos(robot):
    # Evita repetir un ciclo por mantener pulsado un boton.
    while True:
        while (robot.digital_read(BOTON_CUADRADO) == PULSADO
               or robot.digital_read(BOTON_ROMBO) == PULSADO
               or robot.digital_read(BOTON_CIRCULO) == PULSADO):
            # Pausa de 50 ms entre consultas para no consultar continuamente sin descanso.
            sleep(0.05)
        sleep(0.05)  # Antirrebote sencillo al soltar.
        if (robot.digital_read(BOTON_CUADRADO) != PULSADO
                and robot.digital_read(BOTON_ROMBO) != PULSADO
                and robot.digital_read(BOTON_CIRCULO) != PULSADO):
            return


# Ejecutar este bloque solo al iniciar el archivo directamente.
if __name__ == "__main__":
    # Al iniciar, las tres piezas deben estar en sus posiciones de origen.
    # Cada figura recuerda por separado si ya se llevo a la posicion alta.
    # False significa origen; True significa destino alto. Se reinician al arrancar.
    arriba = {
        "cuadrado": False,
        "rombo": False,
        "circulo": False,
    }
    botones = {
        "cuadrado": BOTON_CUADRADO,
        "rombo": BOTON_ROMBO,
        "circulo": BOTON_CIRCULO,
    }
    # Abrir la conexion TCP con el robot.
    robot = NiryoRobot(robot_ip_address)
    try:
        # DI son entradas y DO salidas: no necesitan set_pin_mode().
        robot.digital_write(LUZ_DISPONIBLE, PinState.LOW)
        robot.digital_write(LUZ_TRABAJANDO, PinState.LOW)
        robot.digital_write(LUZ_AMARILLA, PinState.LOW)
        # La preparacion inicial no es una orden de los botones.
        print("Inicializando robot...", flush=True)
        # Calibrar si hace falta y detectar la herramienta instalada.
        robot.calibrate_auto()
        robot.update_tool()
        # Velocidad expresada como porcentaje de la maxima del brazo.
        robot.set_arm_max_velocity(100)
        robot.move_to_home_pose()
        esperar_botones_sueltos(robot)
        print("Listo: DI1 cuadrado, DI2 circulo, DI3 rombo.")
        disponible(robot)

        # Consultar los botones continuamente; ejecutar una sola figura cada vez.
        while True:
            for nombre, boton in botones.items():
                if robot.digital_read(boton) == PULSADO:
                    trabajando(robot)
                    # Alternar ida y vuelta; actualizar el estado tras el movimiento.
                    if not arriba[nombre]:
                        llevar(robot, figuras[nombre])
                    else:
                        devolver(robot, figuras[nombre])
                    arriba[nombre] = not arriba[nombre]
                    disponible(robot)
                    esperar_botones_sueltos(robot)
                    break

            # Pausa de 50 ms entre consultas para no consultar continuamente sin descanso.
            sleep(0.05)

    # Ejecutar la limpieza tambien si se produce un error o se interrumpe el programa.
    finally:
        # Intenta apagar cada luz incluso si falla otra salida.
        try:
            for luz in (LUZ_DISPONIBLE, LUZ_TRABAJANDO, LUZ_AMARILLA):
                try:
                    robot.digital_write(luz, PinState.LOW)
                except Exception as error:
                    print(f"No se pudo apagar {luz}: {error}")
        finally:
            # Cerrar la conexion aunque no se hayan podido apagar todas las luces.
            robot.close_connection()
