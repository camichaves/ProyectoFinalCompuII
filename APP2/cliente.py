import socket
import cv2


def cliente():
    host = "127.0.0.1"
    puerto = 5555
    # Creamos el socket para conectarnos
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Realizamos la conexion
        skt.connect((host, puerto))
        print("Se estableció conexión con el servidor")
    except:
        print("No se ha podido establecer la conexion con el servidor")
        return

    # print("--------------------Funciones--------------------")
    # print("    Envìa una img en escala de grises            ")
    # print("    Escribe close para cerrar xd                 ")
    # print("-------------------------------------------------")
    #
    # mens = input("Ingrese comando a enviar> ")
    # Enviamos el comando al servidor
    mens = cv2.imread('cuatro.jpg', cv2.IMREAD_GRAYSCALE)  # grayscale
    skt.send(mens.encode('utf-8'))
    # if mens == "op":
    #     op = input("Ingrese operación (Ej: 2+2, 3*5, etc)> ")
    #     # Le enviamos la operacion  (Podria esperar una respuesta del servidor pero lo hice asi para simplificar)
    #     skt.send(op.encode('utf-8'))

    # Recibimos la respuesta del servidor en data
    data = skt.recv(1024)
    print(" >Respuesta Server:", str(data.decode('utf-8')))
    skt.close()
    print("Conexión cerrada")


cliente()
