from pyniryo import *

# 1. Conexión y calibración
robot = NiryoRobot("10.10.12.99")
robot.calibrate_auto() 
# robot.update_tool()
print(robot.get_sounds())

# 2. Liberar motores (Modo Aprendizaje)

# robot.set_learning_mode(True)
# robot.release_with_tool()
 

# print("==================================================")
# print(" MOTORES LIBERADOS ")
# print("==================================================")
# input("1. Mueve el rotulador a la posición deseada.\n2. Presiona ENTER para capturar las coordenadas...")

# # 3. Leer la posición exacta
# pos = robot.get_pose() 

# # 4. Bloquear motores de nuevo
# robot.set_learning_mode(False) 

# # 5. Imprimir el resultado en formato código Python listo para copiar
# print("\n¡Posición capturada! Copia la siguiente línea en tu programa de dibujo:")
# print("--------------------------------------------------")
# print(f"mi_posicion = PoseObject(x={pos.x:.4f}, y={pos.y:.4f}, z={pos.z:.4f}, roll={pos.roll:.4f}, pitch={pos.pitch:.4f}, yaw={pos.yaw:.4f})")
# print("--------------------------------------------------\n")

# 6. Cerrar conexión
robot.move_to_home_pose()
robot.close_connection()