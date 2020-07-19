import socket
import threading
import numpy as np
import re
from ast import literal_eval
from predictOneVsAll import predictOneVsAll
import sys
sys.path.insert(1,"/home/camila/Documentos/Proyecto/ProyectoFinalCompuII/Global")
import Global

def conexion(skt_cli, direccion, port, all_theta):
    # Recibimos el mensaje, con el metodo recv recibimos datos y como parametro
    # la cantidad de bytes para recibir
    recibido = skt_cli.recv(4660)
    print("[*] %s:%d Se conecto. " % (direccion, port))
    #print(str(recibido))
    #print(str(recibido.decode('utf-8').replace('[[','[').replace(']]',']')))
    mat = re.sub("\s+",",",recibido.decode('utf-8'))
    arr = literal_eval(mat)
    # Me convierto en cliente de la app3
    print(np.asarray(arr))
    pred = predictOneVsAll(all_theta, np.asarray(arr).ravel())
    print('Prediccion: {}'.format(*pred))
    result = pred
    # Respuesta al Cliente
    skt_cli.send(str(result).encode('utf-8'))
    skt_cli.close()


def servidor():
    host = "127.0.0.1"
    puerto = 5556
    all_theta = np.loadtxt("thetas.txt", comments="#", delimiter=" ", unpack=False)
    print(Global.test)

    max_conexiones = 5
    # Creamos el socket con la familia AF_INET y el tipo SOCK_STREAM
    skt_ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bindeamos la direccion y puerto
    skt_ser.bind((host, puerto))

    # Lo abrimos para que quede a la escucha de clientes
    skt_ser.listen(max_conexiones)
    print("[*] Esperando conexiones en %s:%d" % (host, puerto))
    try:
        while True:
            # Acepta una conexion y crea un nuevo socket para la comunicacion
            skt_cli, direccion = skt_ser.accept()
            print("[*] Conexion establecida con %s:%d" % (direccion[0], direccion[1]))

            # Creo hilos para poder atender a varios clientes al mismo tiempo
            hilo = threading.Thread(target=conexion, args=(skt_cli, direccion[0], direccion[1], all_theta))
            hilo.start()
    except KeyboardInterrupt:
        print("\n Servidor cerrado. Chauu.")
        skt_ser.close()


servidor()
