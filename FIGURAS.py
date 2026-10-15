# Programa Tarea01.py
# Etapa. Dibujo de figuras geométricas con el robot Niryo
# Realizado por: Alvaro Dosil, Lucia Pardo , Santiago Santos , Ignacio 
# Fecha: 08/10/2026


from pyniryo import NiryoRobot, PoseObject

# -------------------------------------------------
# Variables y constantes
# CONEXIÓN
# -------------------------------------------------
robot_ip_address = '10.10.13.221'
# Orientacion en radianes y alturas base en metros.
Raw = 1.257
Pitch = 1.492
Yaw = 1.298
altura_inicial = 0.005
altura_destino = 0.061

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
pirombo = [0.260, -0.085, altura_inicial]
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


def cuadrado(robot):
    # 1. Acercarse por encima de la pieza y abrir la pinza.
    robot.set_arm_max_velocity(100)
    robot.move(pose_aproximacion(picuadrado))
    robot.release_with_tool()   
    # 2. Bajar verticalmente y cerrar para coger la pieza.
    robot.set_arm_max_velocity(60)
    robot.move(pose_base(picuadrado), linear=True)
    robot.grasp_with_tool()     
    robot.wait(1)
    # 3. Levantar antes de trasladar por el punto intermedio.
    robot.set_arm_max_velocity(75)
    robot.move(pose_elevacion(picuadrado), linear=True)
    robot.move(pose_traslado(pintermedio))
    robot.move(pose_traslado(pfcuadrado))
    # # 4. Bajar verticalmente en el destino y soltar.
    robot.move(pose_base(pfcuadrado), linear=True)
    robot.release_with_tool()
    robot.wait(1)
    # # 5. Retirarse hasta la altura de aproximación con la pinza abierta.
    robot.move(pose_retirada(pfcuadrado), linear=True)
    robot.grasp_with_tool()
    robot.move_to_home_pose()
    
def cuadrado_vuelta(robot):
    # 6. Volver al destino, abrir, bajar y recoger el cuadrado.
    robot.set_arm_max_velocity(60)
    robot.move(pose_traslado(pintermedio))
    robot.move(pose_traslado(pfcuadrado))
    robot.release_with_tool()
    robot.move(pose_base(pfcuadrado), linear=True)
    robot.grasp_with_tool()
    robot.wait(1)

    # 7. Subir y regresar por el punto intermedio hasta encima del origen.
    robot.move(pose_traslado(pfcuadrado), linear=True)
    robot.move(pose_traslado(pintermedio))
    robot.move(pose_elevacion(picuadrado))

    # 8. Bajar, dejar en la posición inicial y subir con la pinza abierta.
    robot.move(pose_base(picuadrado), linear=True)
    robot.release_with_tool()
    robot.wait(1)
    robot.move(pose_aproximacion(picuadrado), linear=True)
    robot.grasp_with_tool() 
    robot.move_to_home_pose()



def rombo(robot):
    # 1. Acercarse por encima de la pieza y abrir la pinza.
    robot.set_arm_max_velocity(100)
    robot.move(pose_aproximacion(pirombo))
    robot.release_with_tool()   
    # 2. Bajar verticalmente y cerrar para coger la pieza.
    robot.set_arm_max_velocity(60)
    robot.move(pose_base(pirombo), linear=True)
    robot.grasp_with_tool()     
    robot.wait(1)
    # 3. Levantar antes de trasladar por el punto intermedio.
    robot.set_arm_max_velocity(75)
    robot.move(pose_elevacion(pirombo), linear=True)
    robot.move(pose_traslado(pintermedio))
    robot.move(pose_traslado(pfrombo)) # atencion
    # 4. Bajar verticalmente en el destino y soltar.
    robot.move(pose_base(pfrombo), linear=True)
    robot.release_with_tool()
    robot.wait(1)
    # 5. Retirarse hasta la altura de aproximación con la pinza abierta.
    robot.move(pose_retirada(pfrombo), linear=True)
    robot.grasp_with_tool()
    robot.move_to_home_pose()
    
def rombo_vuelta(robot):
    # 6. Volver al destino, abrir, bajar y recoger el rombo.
    robot.set_arm_max_velocity(60)
    robot.move(pose_traslado(pintermedio))
    robot.move(pose_traslado(pfrombo))
    robot.release_with_tool()
    robot.move(pose_base(pfrombo), linear=True) 
    robot.grasp_with_tool()
    robot.wait(1)

    # 7. Subir y regresar por el punto intermedio hasta encima del origen.
    robot.move(pose_traslado(pfrombo), linear=True)
    robot.move(pose_traslado(pintermedio))
    robot.move(pose_elevacion(pirombo))

    # 8. Bajar, dejar en la posición inicial y subir con la pinza abierta.
    robot.move(pose_base(pirombo), linear=True)
    robot.release_with_tool()
    robot.wait(1)
    robot.move(pose_aproximacion(pirombo), linear=True)
    robot.grasp_with_tool() 
    robot.move_to_home_pose()
    
    


# -------------------------------------------------
# CÍRCULO
# -------------------------------------------------

def circulo(robot):
    # 1. Acercarse por encima de la pieza y abrir la pinza.
        robot.set_arm_max_velocity(100)
        robot.move(pose_aproximacion(picirculo))
        robot.release_with_tool()   
        # 2. Bajar verticalmente y cerrar para coger la pieza.
        robot.set_arm_max_velocity(60)
        robot.move(pose_base(picirculo), linear=True)
        robot.grasp_with_tool()     
        robot.wait(1)
        # 3. Levantar antes de trasladar por el punto intermedio.
        robot.set_arm_max_velocity(75)
    
        robot.move(pose_elevacion(picirculo), linear=True)
        robot.move(pose_traslado(pintermedio))
        robot.move(pose_traslado(pfcirculo, (Raw_circulo, Pitch, Yaw_circulo)))
        # # 4. Bajar verticalmente en el destino y soltar.
        robot.move(pose_base(pfcirculo, (Raw_circulo, Pitch_circulo, Yaw_circulo)),linear=True)
        robot.release_with_tool()
        robot.wait(1)
        # # 5. Retirarse hasta la altura de aproximación con la pinza abierta.
        robot.move(pose_retirada(pfcirculo, (Raw_circulo, Pitch_circulo, Yaw_circulo)),linear=True)
        robot.grasp_with_tool()
        robot.move_to_home_pose()
        
def circulo_vuelta(robot):
        # 6. Volver al destino, abrir, bajar y recoger el círculo.
        robot.set_arm_max_velocity(60)
        robot.move(pose_traslado(pintermedio))
        robot.move(pose_traslado(pfcirculo, (Raw_circulo, Pitch_circulo, Yaw_circulo)))
        robot.release_with_tool()
        robot.move(pose_base(pfcirculo, (Raw_circulo, Pitch_circulo, Yaw_circulo)), linear=True)
        robot.grasp_with_tool()
        robot.wait(1)

        # 7. Subir y regresar por el punto intermedio hasta encima del origen.
        robot.move(pose_traslado(pfcirculo, (Raw_circulo, Pitch_circulo, Yaw_circulo)), linear=True)
        robot.move(pose_traslado(pintermedio))
        robot.move(pose_elevacion(picirculo))

        # 8. Bajar, dejar en la posición inicial y subir con la pinza abierta.
        robot.move(pose_base(picirculo), linear=True)
        robot.release_with_tool()
        robot.wait(1)
        robot.move(pose_aproximacion(picirculo), linear=True)
        robot.grasp_with_tool() 
        robot.move_to_home_pose()
        

# -------------------------------------------------
# PROGRAMA PRINCIPAL
# -------------------------------------------------

if __name__ == "__main__":
    print("Escribe cuadrado, circulo, rombo o todos y pulsa Enter en la terminal.", flush=True)
    try:
        figura = input("¿Qué quieres coger?: ").strip().lower().replace("í", "i")
    except EOFError:
        raise SystemExit(
            "No se puede leer el teclado. Ejecuta este archivo en una terminal interactiva."
        )

    if figura not in ("cuadrado", "circulo", "rombo","todos"):
        print("Figura no válida. Elige todos cuadrado , circulo o rombo.")
        raise SystemExit(0)

    robot = NiryoRobot(robot_ip_address)
    try:
        robot.calibrate_auto()
        robot.update_tool()
        robot.set_arm_max_velocity(100)
        robot.move_to_home_pose()
    
        print(f"Ejecutando: {figura}", flush=True)
        if figura == "cuadrado":
            cuadrado(robot)
            cuadrado_vuelta(robot)
        elif figura == "circulo":
            circulo(robot)
            circulo_vuelta(robot)
        elif figura == "rombo":
            rombo(robot)
            rombo_vuelta(robot)
        elif figura == "todos":
            cuadrado(robot)
            circulo(robot)
            rombo(robot)
            cuadrado_vuelta(robot)
            circulo_vuelta(robot)
            rombo_vuelta(robot)
            

    finally:
        # Cerrar la conexion tanto al terminar como si falla un movimiento.
        print("Cerrando la conexion...", flush=True)
        robot.close_connection()

