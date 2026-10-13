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
robot_ip_address = '10.10.12.203'
aproximacion = 0.035



# Definiciones de Clases, Funciones y Procedimientos

# Recogida y colocación del cuadrado con la pinza.
# Posiciones en metros y orientaciones en radianes.
# aproximacion es una altura Z absoluta, no una distancia sobre la pieza.
# Verificar las poses con la herramienta y el TCP usados al enseñarlas.

def cuadrado(robot):
    # 1. Acercarse por encima de la pieza y abrir la pinza.
    robot.set_arm_max_velocity(100)
    robot.move(PoseObject(0.254, 0.044, aproximacion, 1.257, 1.492, 1.298))
    robot.release_with_tool()   
    # 2. Bajar verticalmente y cerrar para coger la pieza.
    robot.set_arm_max_velocity(60)
    robot.move(PoseObject(0.254, 0.044, 0.005, 1.257, 1.492, 1.298), linear=True)
    robot.grasp_with_tool()     
    robot.wait(1)
    # 3. Levantar antes de trasladar por el punto intermedio.
    robot.set_arm_max_velocity(75)
    robot.move(PoseObject(0.254, 0.044, 0.09, 1.257, 1.492, 1.298), linear=True)
    robot.move(PoseObject(0.00, -0.15, 0.15, 1.257, 1.492, 1.298))
    robot.move(PoseObject(-0.057, -0.266, 0.09, -0.945, 1.494, -3.3))
    # 4. Bajar verticalmente en el destino y soltar.
    robot.move(PoseObject(-0.057, -0.266, 0.061, -0.945, 1.494, -3.3), linear=True)
    robot.release_with_tool()
    robot.wait(1)
    # 5. Retirarse hasta la altura de aproximación con la pinza abierta.
    robot.move(PoseObject(-0.057, -0.266, 0.1, -0.945, 1.494, -3.3), linear=True)
    robot.grasp_with_tool()
    robot.move_to_home_pose()
    
def cuadrado_vuelta(robot):
    # 6. Volver al destino, abrir, bajar y recoger el cuadrado.
    robot.set_arm_max_velocity(60)
    robot.move(PoseObject(0.00, -0.15, 0.15, 1.257, 1.492, 1.298))
    robot.move(PoseObject(-0.057, -0.266, 0.1, -0.945, 1.494, -3.3))
    robot.release_with_tool()
    robot.move(PoseObject(-0.057, -0.266, 0.061, -0.945, 1.494, -3.3), linear=True)
    robot.grasp_with_tool()
    robot.wait(1)

    # 7. Subir y regresar por el punto intermedio hasta encima del origen.
    robot.move(PoseObject(-0.057, -0.266, 0.1, -0.945, 1.494, -3.3), linear=True)
    robot.move(PoseObject(0.00, -0.15, 0.15, 1.257, 1.492, 1.298))
    robot.move(PoseObject(0.254, 0.044, 0.09, 1.257, 1.492, 1.298))

    # 8. Bajar, dejar en la posición inicial y subir con la pinza abierta.
    robot.move(PoseObject(0.254, 0.044, 0.005, 1.257, 1.492, 1.298), linear=True)
    robot.release_with_tool()
    robot.wait(1)
    robot.move(PoseObject(0.254, 0.044, 0.035, 1.257, 1.492, 1.298), linear=True)
    robot.grasp_with_tool() 
    robot.move_to_home_pose()



def rombo(robot):
    # 1. Acercarse por encima de la pieza y abrir la pinza.
    robot.set_arm_max_velocity(100)
    robot.move(PoseObject(0.264, -0.085, aproximacion, 1.257, 1.492, 1.298))
    robot.release_with_tool()   
    # 2. Bajar verticalmente y cerrar para coger la pieza.
    robot.set_arm_max_velocity(60)
    robot.move(PoseObject(0.264, -0.085, 0.005, 1.257, 1.492, 1.298), linear=True)
    robot.grasp_with_tool()     
    robot.wait(1)
    # 3. Levantar antes de trasladar por el punto intermedio.
    robot.set_arm_max_velocity(75)
    robot.move(PoseObject(0.264, -0.085, 0.09, 1.257, 1.492, 1.298), linear=True)
    robot.move(PoseObject(0.00, -0.15, 0.15, 1.257, 1.492, 1.298))
    robot.move(PoseObject(0.026, -0.268, 0.15, -0.945, 1.494, -1.5)) # atencion
    # 4. Bajar verticalmente en el destino y soltar.
    robot.move(PoseObject(0.026, -0.268, 0.061, -0.945, 1.494, -1.5), linear=True)
    robot.release_with_tool()
    robot.wait(1)
    # 5. Retirarse hasta la altura de aproximación con la pinza abierta.
    robot.move(PoseObject(0.026, -0.268, 0.12, -0.945, 1.494, -1.5), linear=True)
    robot.grasp_with_tool()
    robot.move_to_home_pose()
    
def rombo_vuelta(robot):
    # 6. Volver al destino, abrir, bajar y recoger el rombo.
    robot.set_arm_max_velocity(60)
    robot.move(PoseObject(0.00, -0.15, 0.15, 1.257, 1.492, 1.298))
    robot.move(PoseObject(0.026, -0.268, 0.15, -0.945, 1.494, -1.5))
    robot.release_with_tool()
    robot.move(PoseObject(0.026, -0.268, 0.061, -0.945, 1.494, -1.5), linear=True)
    robot.grasp_with_tool()
    robot.wait(1)

    # 7. Subir y regresar por el punto intermedio hasta encima del origen.
    robot.move(PoseObject(0.026, -0.268, 0.15, -0.945, 1.494, -1.5), linear=True)
    robot.move(PoseObject(0.00, -0.15, 0.15, 1.257, 1.492, 1.298))
    robot.move(PoseObject(0.264, -0.085, 0.09, 1.257, 1.492, 1.298))

    # 8. Bajar, dejar en la posición inicial y subir con la pinza abierta.
    robot.move(PoseObject(0.264, -0.085, 0.005, 1.257, 1.492, 1.298), linear=True)
    robot.release_with_tool()
    robot.wait(1)
    robot.move(PoseObject(0.264, -0.085, 0.035, 1.257, 1.492, 1.298), linear=True)
    robot.grasp_with_tool() 
    robot.move_to_home_pose()
    
    


# -------------------------------------------------
# CÍRCULO
# -------------------------------------------------

def circulo(robot):
    # 1. Acercarse por encima de la pieza y abrir la pinza.
        robot.set_arm_max_velocity(100)
        robot.move(PoseObject(0.259, -0.02, aproximacion, 1.257, 1.492, 1.298))
        robot.release_with_tool()   
        # 2. Bajar verticalmente y cerrar para coger la pieza.
        robot.set_arm_max_velocity(60)
        robot.move(PoseObject(0.259, -0.02, 0.004, 1.257, 1.492, 1.298), linear=True)
        robot.grasp_with_tool()     
        robot.wait(1)
        # 3. Levantar antes de trasladar por el punto intermedio.
        robot.set_arm_max_velocity(75)
    
        robot.move(PoseObject(0.259, -0.02, 0.09, 1.257, 1.492, 1.298), linear=True)
        robot.move(PoseObject(0.00, -0.15, 0.15, 1.257, 1.492, 1.298))
        robot.move(PoseObject(0.092, -0.268, 0.15, -0.945, 1.492, -0.8))
        # # 4. Bajar verticalmente en el destino y soltar.
        robot.move(PoseObject(0.092, -0.268, 0.061, -0.945, 1.494, -0.8),linear=True)
        robot.release_with_tool()
        robot.wait(1)
        # # 5. Retirarse hasta la altura de aproximación con la pinza abierta.
        robot.move(PoseObject(0.092, -0.268, 0.12, -0.945, 1.494, -0.8),linear=True)
        robot.grasp_with_tool()
        robot.move_to_home_pose()
        
def circulo_vuelta(robot):
        # 6. Volver al destino, abrir, bajar y recoger el círculo.
        robot.set_arm_max_velocity(60)
        robot.move(PoseObject(0.00, -0.15, 0.15, 1.257, 1.492, 1.298))
        robot.move(PoseObject(0.092, -0.268, 0.15, -0.945, 1.494, -0.8))
        robot.release_with_tool()
        robot.move(PoseObject(0.092, -0.268, 0.061, -0.945, 1.494, -0.8), linear=True)
        robot.grasp_with_tool()
        robot.wait(1)

        # 7. Subir y regresar por el punto intermedio hasta encima del origen.
        robot.move(PoseObject(0.092, -0.268, 0.15, -0.945, 1.494, -0.8), linear=True)
        robot.move(PoseObject(0.00, -0.15, 0.15, 1.257, 1.492, 1.298))
        robot.move(PoseObject(0.259, -0.02, 0.09, 1.257, 1.492, 1.298))

        # 8. Bajar, dejar en la posición inicial y subir con la pinza abierta.
        robot.move(PoseObject(0.259, -0.02, 0.004, 1.257, 1.492, 1.298), linear=True)
        robot.release_with_tool()
        robot.wait(1)
        robot.move(PoseObject(0.259, -0.02, 0.035, 1.257, 1.492, 1.298), linear=True)
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

