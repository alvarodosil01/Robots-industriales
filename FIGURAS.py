# Programa Tarea01.py
# Etapa. Dibujo de figuras geométricas con el robot Niryo
# Realizado por: Alvaro Dosil, Lucia Pardo , Santiago Santos , Ignacio 
# Fecha: 08/10/2026

# Bibliotecas y módulos
from pyniryo import NiryoRobot, PoseObject

# -------------------------------------------------
# Variables y constantes
# CONEXIÓN
# -------------------------------------------------
robot_ip_address = '10.10.13.221'
aproximacion = 0.035  # Altura Z absoluta sobre el origen (metros).
Raw = 1.257  # Giro roll; se conserva el nombre usado en el programa.
Pitch = 1.492
Yaw = 1.298
altura_inicial = 0.005  # Recogida y devolucion de las tres piezas en el origen.
altura_elevacion = 0.09
altura_traslado = 0.15  # Punto intermedio y aproximacion/recogida sobre el destino.
altura_destino = 0.061
altura_retirada = 0.12
altura_retirada_cuadrado = 0.2

# Posiciones X e Y en metros: pi = origen, pf = destino alto.
picuadrado = [0.254, 0.044]
pfcuadrado = [-0.057, -0.266]
pirombo = [0.260, -0.085]
pfrombo = [0.026, -0.268]
picirculo = [0.259, -0.02]
pfcirculo = [0.092, -0.268]
pintermedio = [0.00, -0.15]

# Orientacion del circulo en el destino, en radianes.
Raw_circulo = -0.945
Pitch_circulo = 1.494
Yaw_circulo = -0.8
# En la primera aproximacion al destino se conserva Pitch = 1.492.
# * delante de una posicion separa sus dos valores X e Y en PoseObject.


# Definiciones de Clases, Funciones y Procedimientos

# Recogida y colocación del cuadrado con la pinza.
# Posiciones en metros y orientaciones en radianes.
# aproximacion es una altura Z absoluta, no una distancia sobre la pieza.
# Verificar las poses con la herramienta y el TCP usados al enseñarlas.

def cuadrado(robot):
    # 1. Acercarse por encima de la pieza y abrir la pinza.
    robot.set_arm_max_velocity(100)
    robot.move(PoseObject(*picuadrado, aproximacion, Raw, Pitch, Yaw))
    robot.release_with_tool()   
    # 2. Bajar verticalmente y cerrar para coger la pieza.
    robot.set_arm_max_velocity(60)
    robot.move(PoseObject(*picuadrado, altura_inicial, Raw, Pitch, Yaw), linear=True)
    robot.grasp_with_tool()     
    robot.wait(1)
    # 3. Levantar antes de trasladar por el punto intermedio.
    robot.set_arm_max_velocity(75)
    robot.move(PoseObject(*picuadrado, altura_elevacion, Raw, Pitch, Yaw), linear=True)
    robot.move(PoseObject(*pintermedio, altura_traslado, Raw, Pitch, Yaw))
    robot.move(PoseObject(*pfcuadrado, altura_traslado, Raw, Pitch, Yaw))
    # # 4. Bajar verticalmente en el destino y soltar.
    robot.move(PoseObject(*pfcuadrado, altura_destino, Raw, Pitch, Yaw), linear=True)
    robot.release_with_tool()
    robot.wait(1)
    # # 5. Retirarse hasta la altura de aproximación con la pinza abierta.
    robot.move(PoseObject(*pfcuadrado, altura_retirada_cuadrado, Raw, Pitch, Yaw), linear=True)
    robot.grasp_with_tool()
    robot.move_to_home_pose()
    
def cuadrado_vuelta(robot):
    # 6. Volver al destino, abrir, bajar y recoger el cuadrado.
    robot.set_arm_max_velocity(60)
    robot.move(PoseObject(*pintermedio, altura_traslado, Raw, Pitch, Yaw))
    robot.move(PoseObject(*pfcuadrado, altura_traslado, Raw, Pitch, Yaw))
    robot.release_with_tool()
    robot.move(PoseObject(*pfcuadrado, altura_destino, Raw, Pitch, Yaw), linear=True)
    robot.grasp_with_tool()
    robot.wait(1)

    # 7. Subir y regresar por el punto intermedio hasta encima del origen.
    robot.move(PoseObject(*pfcuadrado, altura_traslado, Raw, Pitch, Yaw), linear=True)
    robot.move(PoseObject(*pintermedio, altura_traslado, Raw, Pitch, Yaw))
    robot.move(PoseObject(*picuadrado, altura_elevacion, Raw, Pitch, Yaw))

    # 8. Bajar, dejar en la posición inicial y subir con la pinza abierta.
    robot.move(PoseObject(*picuadrado, altura_inicial, Raw, Pitch, Yaw), linear=True)
    robot.release_with_tool()
    robot.wait(1)
    robot.move(PoseObject(*picuadrado, aproximacion, Raw, Pitch, Yaw), linear=True)
    robot.grasp_with_tool() 
    robot.move_to_home_pose()



def rombo(robot):
    # 1. Acercarse por encima de la pieza y abrir la pinza.
    robot.set_arm_max_velocity(100)
    robot.move(PoseObject(*pirombo, aproximacion, Raw, Pitch, Yaw))
    robot.release_with_tool()   
    # 2. Bajar verticalmente y cerrar para coger la pieza.
    robot.set_arm_max_velocity(60)
    robot.move(PoseObject(*pirombo, altura_inicial, Raw, Pitch, Yaw), linear=True)
    robot.grasp_with_tool()     
    robot.wait(1)
    # 3. Levantar antes de trasladar por el punto intermedio.
    robot.set_arm_max_velocity(75)
    robot.move(PoseObject(*pirombo, altura_elevacion, Raw, Pitch, Yaw), linear=True)
    robot.move(PoseObject(*pintermedio, altura_traslado, Raw, Pitch, Yaw))
    robot.move(PoseObject(*pfrombo, altura_traslado, Raw, Pitch, Yaw)) # atencion
    # 4. Bajar verticalmente en el destino y soltar.
    robot.move(PoseObject(*pfrombo, altura_destino, Raw, Pitch, Yaw), linear=True)
    robot.release_with_tool()
    robot.wait(1)
    # 5. Retirarse hasta la altura de aproximación con la pinza abierta.
    robot.move(PoseObject(*pfrombo, altura_retirada, Raw, Pitch, Yaw), linear=True)
    robot.grasp_with_tool()
    robot.move_to_home_pose()
    
def rombo_vuelta(robot):
    # 6. Volver al destino, abrir, bajar y recoger el rombo.
    robot.set_arm_max_velocity(60)
    robot.move(PoseObject(*pintermedio, altura_traslado, Raw, Pitch, Yaw))
    robot.move(PoseObject(*pfrombo, altura_traslado, Raw, Pitch, Yaw))
    robot.release_with_tool()
    robot.move(PoseObject(*pfrombo, altura_destino, Raw, Pitch, Yaw), linear=True) 
    robot.grasp_with_tool()
    robot.wait(1)

    # 7. Subir y regresar por el punto intermedio hasta encima del origen.
    robot.move(PoseObject(*pfrombo, altura_traslado, Raw, Pitch, Yaw), linear=True)
    robot.move(PoseObject(*pintermedio, altura_traslado, Raw, Pitch, Yaw))
    robot.move(PoseObject(*pirombo, altura_elevacion, Raw, Pitch, Yaw))

    # 8. Bajar, dejar en la posición inicial y subir con la pinza abierta.
    robot.move(PoseObject(*pirombo, altura_inicial, Raw, Pitch, Yaw), linear=True)
    robot.release_with_tool()
    robot.wait(1)
    robot.move(PoseObject(*pirombo, aproximacion, Raw, Pitch, Yaw), linear=True)
    robot.grasp_with_tool() 
    robot.move_to_home_pose()
    
    


# -------------------------------------------------
# CÍRCULO
# -------------------------------------------------

def circulo(robot):
    # 1. Acercarse por encima de la pieza y abrir la pinza.
        robot.set_arm_max_velocity(100)
        robot.move(PoseObject(*picirculo, aproximacion, Raw, Pitch, Yaw))
        robot.release_with_tool()   
        # 2. Bajar verticalmente y cerrar para coger la pieza.
        robot.set_arm_max_velocity(60)
        robot.move(PoseObject(*picirculo, altura_inicial, Raw, Pitch, Yaw), linear=True)
        robot.grasp_with_tool()     
        robot.wait(1)
        # 3. Levantar antes de trasladar por el punto intermedio.
        robot.set_arm_max_velocity(75)
    
        robot.move(PoseObject(*picirculo, altura_elevacion, Raw, Pitch, Yaw), linear=True)
        robot.move(PoseObject(*pintermedio, altura_traslado, Raw, Pitch, Yaw))
        robot.move(PoseObject(*pfcirculo, altura_traslado, Raw_circulo, Pitch, Yaw_circulo))
        # # 4. Bajar verticalmente en el destino y soltar.
        robot.move(PoseObject(*pfcirculo, altura_destino, Raw_circulo, Pitch_circulo, Yaw_circulo),linear=True)
        robot.release_with_tool()
        robot.wait(1)
        # # 5. Retirarse hasta la altura de aproximación con la pinza abierta.
        robot.move(PoseObject(*pfcirculo, altura_retirada, Raw_circulo, Pitch_circulo, Yaw_circulo),linear=True)
        robot.grasp_with_tool()
        robot.move_to_home_pose()
        
def circulo_vuelta(robot):
        # 6. Volver al destino, abrir, bajar y recoger el círculo.
        robot.set_arm_max_velocity(60)
        robot.move(PoseObject(*pintermedio, altura_traslado, Raw, Pitch, Yaw))
        robot.move(PoseObject(*pfcirculo, altura_traslado, Raw_circulo, Pitch_circulo, Yaw_circulo))
        robot.release_with_tool()
        robot.move(PoseObject(*pfcirculo, altura_destino, Raw_circulo, Pitch_circulo, Yaw_circulo), linear=True)
        robot.grasp_with_tool()
        robot.wait(1)

        # 7. Subir y regresar por el punto intermedio hasta encima del origen.
        robot.move(PoseObject(*pfcirculo, altura_traslado, Raw_circulo, Pitch_circulo, Yaw_circulo), linear=True)
        robot.move(PoseObject(*pintermedio, altura_traslado, Raw, Pitch, Yaw))
        robot.move(PoseObject(*picirculo, altura_elevacion, Raw, Pitch, Yaw))

        # 8. Bajar, dejar en la posición inicial y subir con la pinza abierta.
        robot.move(PoseObject(*picirculo, altura_inicial, Raw, Pitch, Yaw), linear=True)
        robot.release_with_tool()
        robot.wait(1)
        robot.move(PoseObject(*picirculo, aproximacion, Raw, Pitch, Yaw), linear=True)
        robot.grasp_with_tool() 
        robot.move_to_home_pose()
        

# -------------------------------------------------
# PROGRAMA PRINCIPAL
# -------------------------------------------------

if __name__ == "__main__":
    figura = input(
        "¿Qué quieres coger? (cuadrado / circulo /rombo/todos): "
    ).strip().lower().replace("í", "i")

    if figura not in ("cuadrado", "circulo", "rombo","todos"):
        print("Figura no válida. Elige todos cuadrado , circulo o rombo.")
        raise SystemExit(0)

  

    robot = NiryoRobot(robot_ip_address)

    try:
        robot.calibrate_auto()
        robot.update_tool()
        robot.set_arm_max_velocity(100)
        robot.move_to_home_pose()

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
        robot.close_connection()

