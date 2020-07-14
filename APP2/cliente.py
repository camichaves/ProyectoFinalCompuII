import socket
import imageio
import numpy as np
from matplotlib import pyplot as plt


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
    # print("    Envìa una img para predecir                  ")
    # print("    Escribe close para cerrar xd                 ")
    # print("-------------------------------------------------")
    #
    # mens = input("Ingrese comando a enviar> ")
    # Enviamos el comando al servidor
    im = imageio.imread("/home/camila/Documentos/Proyecto/ProyectoFinalCompuII/APP2/laimg.png")
        #"C:\\Users\Camila\Documents\FACULTAD\FINAL COMPU II\Andrew-NG-ML-Python-Solutions\Exercise3\laimg.png")
    gray = np.dot(im[..., :3], [0.2989, 0.5870, 0.114])
    # gray = np.dot(im[...,:3],[65536, 256, 1])
    gray /= 255
    mens = gray
    print(str(mens))
    skt.send(str(mens).encode('utf-8'))
    # if mens == "op":
    #     op = input("Ingrese operación (Ej: 2+2, 3*5, etc)> ")
    #     # Le enviamos la operacion  (Podria esperar una respuesta del servidor pero lo hice asi para simplificar)
    #     skt.send(op.encode('utf-8'))

    # Recibimos la respuesta del servidor en data
    data = skt.recv(1024)
    print(" >Respuesta Server:", str(data))
    skt.close()
    print("Conexión cerrada")


cliente()
