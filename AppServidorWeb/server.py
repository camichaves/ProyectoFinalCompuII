import flask
from flask import request
import threading
import socket
import time
app = flask.Flask(__name__)
app.config["DEBUG"] = True
config = open("servidor.conf", "r")
host = config.readline()[:-1]
mipuerto = config.readline()[:-1]
config.readline()
puertoapp3 = int(config.readline()[:-1])
config.close()
server3 = "127.0.0.1"


def conexion(host, puertoapp3, recibido, direccion):
    # Me convierto en cliente de la app3
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #try:
        # Realizamos la conexion
    skt.connect(('127.0.0.1',puertoapp3))
    print("Se estableció conexión con el servidor")
    #except:
    print("No se ha podido establecer la conexion con el servidor")
        #return
    pet = direccion + "-" + str(recibido)
    skt.send(pet.encode('utf-8'))
    # Recibimos la respuesta del servidor en data
    data = skt.recv(4660)
    print(" >Respuesta de App3:", str(data.decode('utf-8')))
    skt.close()
    result = data

    # Respuesta al Cliente
    try:
        return result
        print("Respuesta enviada :)")
    except:
        print("Problemas al enviar la respuesta :(")


@app.route('/', methods=['POST'])
def home():
    rta = conexion(
        host, puertoapp3, flask.request.form['img'],
        flask.request.remote_addr)
    return rta

if __name__ == "__main__":
    app.run(port=mipuerto)

