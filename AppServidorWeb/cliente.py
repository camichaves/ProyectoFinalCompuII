import socket
import imageio
import getopt
import numpy as np
import re
from ast import literal_eval
from matplotlib import pyplot as plt
import sys
import requests
try:
    config = open("servidor.conf", "r")
    host = config.readline()[:-1]
    puerto = int(config.readline()[:-1])
    ruta = config.readline()[:-1]
    config.close()
except:
    print("Problemas al cargar la configuracion desde el archivo :(")


def cliente():
    opc, argus = getopt.getopt(sys.argv[1:], 'a:')
    rutaarch = ""
    for o, a in opc:
        rutaarch = ruta + a
    # Enviamos el comando al servidor
    im = imageio.imread(a)
    print(im.shape)
    gray = np.dot(im[..., :3], [0.2989, 0.5870, 0.114])
    gray = np.transpose(gray)
    gray /= 255
    print(gray)
    mens = str(gray)
    URL = "http://" + host + ":" + str(puerto) + "/"
    PARAMS = {'img': mens}
    try:
        r = requests.post(url=URL, data=PARAMS)
        print("Peticiòn enviada")
        data = r.text
        print(data)
    except:
        print("Problemas al enviar la imagen al servidor")
# Recibimos la respuesta del servidor en data
    print("Conexión cerrada")

if __name__ == "__main__":
    cliente()

