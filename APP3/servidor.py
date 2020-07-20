import socket
import threading
import numpy as np
import re
from ast import literal_eval
from predictOneVsAll import predictOneVsAll
import concurrent.futures
import multiprocessing as mp

def conexion(skt_cli, direccion, port, all_theta):
    with _COUNTER.get_lock():
        _COUNTER.value += 1
        print("Cantidad de numeros calculados:")
        print(_COUNTER.value)
    # Recibimos el mensaje, con el metodo recv recibimos datos y como parametro
    # la cantidad de bytes para recibir
    recibido = skt_cli.recv(4660)
    print("[*] %s:%d Se conecto. " % (direccion, port))
    mat = re.sub("\s+",",",recibido.decode('utf-8'))
    arr = literal_eval(mat)
    # Me convierto en cliente de la app3
    pred = predictOneVsAll(all_theta, np.asarray(arr).ravel())
    print('Prediccion: {}'.format(*pred))
    result = pred
    # Respuesta al Cliente
    skt_cli.send(str(result).encode('utf-8'))
    skt_cli.close()


def servidor():
    host = "127.0.0.1"
    puerto = 5556
    global _COUNTER
    _COUNTER = mp.Value('i', 0)
    all_theta = np.loadtxt("/home/guille/Escritorio/TrabajoCompuII/ProyectoFinalCompuII/APP1/thetas.txt", comments="#", delimiter=" ", unpack=False)

    max_conexiones = 5
    # Creamos el socket con la familia AF_INET y el tipo SOCK_STREAM
    skt_ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bindeamos la direccion y puerto
    skt_ser.bind((host, puerto))

    # Lo abrimos para que quede a la escucha de clientes
    skt_ser.listen(max_conexiones)
    print("[*] Esperando conexiones en %s:%d" % (host, puerto))
    hijos = concurrent.futures.ProcessPoolExecutor()

    try:
        while True:
            # Acepta una conexion y crea un nuevo socket para la comunicacion
            skt_cli, direccion = skt_ser.accept()
            print("[*] Conexion establecida con %s:%d" % (direccion[0], direccion[1]))

            # Creo hilos para poder atender a varios clientes al mismo tiempo
            hijos.submit(conexion, skt_cli, direccion[0], direccion[1], all_theta)
    except KeyboardInterrupt:
        print("\n Servidor cerrado. Chauu.")
        skt_ser.close()


servidor()
