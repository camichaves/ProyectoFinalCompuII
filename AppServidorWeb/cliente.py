import socket
import imageio
import getopt
import numpy as np
import re
from ast import literal_eval
from matplotlib import pyplot as plt
import sys


def cliente():
    config = open("servidor.conf", "r") 
    host = config.readline()
    puerto = config.readline()
    ruta = config.readline()
    config.close()
    opc ,argus = getopt.getopt(sys.argv[1:],'a:')
    rutaarch = ""
    for o, a in opc:
        rutaarch = ruta + a
    # Creamos el socket para conectarnos
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Realizamos la conexion
        skt.connect((host, puerto))
        print("Se estableció conexión con el servidor")
    except:
        print("No se ha podido establecer la conexion con el servidor")
        return
    # Enviamos el comando al servidor
    im = imageio.imread(rutaarch)
    gray = np.dot(im[..., :3], [0.2989, 0.5870, 0.114])
    gray = np.transpose(gray)
    gray /= 255
    mens = gray
    try:
        skt.send(str(mens).encode('utf-8'))
        print("Peticiòn enviada")
    except:
        print("Problemas al enviar la imagen al servidor")
    # Recibimos la respuesta del servidor en data
    data = skt.recv(1024)
    print(" >Respuesta Server:", str(data.decode('utf-8')))
    skt.close()
    print("Conexión cerrada")

if __name__ == "__main__":
    cliente()
