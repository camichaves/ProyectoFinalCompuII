import socket
import imageio
import getopt
import numpy as np
import re
from ast import literal_eval
from matplotlib import pyplot as plt
import sys


def cliente():
    host = "127.0.0.1"
    puerto = 5555
    opc ,argus = getopt.getopt(sys.argv[1:],'a:')
    rutaarch = ""
    for o, a in opc:
        rutaarch = "/home/guille/Escritorio/TrabajoCompuII/ProyectoFinalCompuII/APP2/" + a
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
    # gray = np.dot(im[...,:3],[65536, 256, 1])
    gray = np.transpose(gray)
    gray /= 255
    mens = gray
    test = str(mens)
    mat = re.sub("\s+",",",test)
    #print(mat)
    arr = literal_eval(mat)
    testArray = np.asarray(arr)
    #print(testArray)
    gg = testArray[0]
    #print(gg)
    skt.send(str(mens).encode('utf-8'))
    # Recibimos la respuesta del servidor en data
    data = skt.recv(1024)
    print(" >Respuesta Server:", str(data.decode('utf-8')))
    skt.close()
    print("Conexión cerrada")


cliente()
