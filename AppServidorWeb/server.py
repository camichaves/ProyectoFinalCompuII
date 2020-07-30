import flask
from flask import request, render_template
import threading
import socket
import imageio
import numpy as np
import sys
from configparser import ConfigParser
app = flask.Flask(__name__)
app.config["DEBUG"] = True


def conexion(puertoapp3, recibido, direccion, app3):
    # Me convierto en cliente de la app3
    skt = None
    if(ipvnro == 6):
        skt = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    else:
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Realizamos la conexion
        skt.connect((app3, puertoapp3))
        print("Se estableció conexión con el servidor")
    except:
        print("No se ha podido establecer la conexion con el servidor")
        return
    pet = direccion + "-" + str(recibido)
    try:
        skt.send(pet.encode('utf-8'))
    except:
        print("No se ha podido enviar la respuesta del servidor :(")
        return
    # Recibimos la respuesta del servidor en data
    data = skt.recv(12152)
    print(" >Respuesta de App3:", str(data.decode('utf-8')))
    skt.close()
    result = data

    # Respuesta al Cliente
    try:
        return result
        print("Respuesta enviada :)")
    except:
        print("Problemas al enviar la respuesta :(")


@app.route('/', methods=["GET", 'POST'])
def home():
    if request.method == 'POST':
        im = imageio.imread(request.files['img'])
        rta = conexion(
            puertoSocket, str(im) ,
            flask.request.remote_addr, hostSocket)
        return rta
    return render_template("form.html")


if __name__ == "__main__":
    try:
        parser = ConfigParser()
        parser.read('serv.conf')
        mipuerto = int(parser.get('SERVIDOR_WEB', 'puerto'))
        puertoSocket = int(parser.get('SOCKET', 'puerto'))
        hostSocket = parser.get('SOCKET', 'ip')
        ipvnro = int(parser.get('SOCKET', 'ipv'))
    except:
        print("Problemas al cargar la configuracion desde el archivo :(")
    np.set_printoptions(threshold=sys.maxsize)
    app.run(port=mipuerto)

