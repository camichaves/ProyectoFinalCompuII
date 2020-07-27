import socket
import threading
import numpy as np
import re
from ast import literal_eval
from predictOneVsAll import predictOneVsAll
import concurrent.futures
import multiprocessing as mp
from datetime import datetime
import getopt
import sys
import os
from filelock import FileLock


def conexion(skt_cli, direccion, port, all_theta, guardar):
    with _COUNTER.get_lock():
        _COUNTER.value += 1
        print("Cantidad de numeros calculados:")
        print(_COUNTER.value)
    # Recibimos el mensaje, con el metodo recv recibimos datos y como parametro
    # la cantidad de bytes para recibir
    recib = skt_cli.recv(4660)
    recib = recib.decode('utf-8')
    recibido = recib.split("-", 1)
    print("[*] %s:%d Se conecto. " % (direccion, port))
    mat = re.sub("\s+", ",", recibido[1])
    arr = literal_eval(mat)
    # Me convierto en cliente de la app3
    pred = predictOneVsAll(all_theta, np.asarray(arr).ravel())
    print('Prediccion: {}'.format(*pred))
    result = pred
    if(guardar):
        print("guardando data...")
        linea = str(datetime.now()) + ", " + str(_COUNTER.value) + ", " + str(recibido[0]) + ", " + str(pred) + "\n"
        try:
            lock = FileLock("archivo.lock")
            with lock:
                    print("Lock acquired.")
                    open("historial.log", "a+").write(linea)
                    print("Listo")
        except:
            print("Ocurriò un problema al guardar la info en el archivo")
    # Respuesta al Cliente
    try:
        skt_cli.send(str(result).encode('utf-8'))
        print("Respuesta enviada :)")
    except:
        print("Ocurriò un problema al enviar la respuesta :(")
    skt_cli.close()


def servidor():
    config = open("servidor.conf", "r")
    host = config.readline()[:-1]
    puerto = int(config.readline()[:-1])
    rutaThetas = config.readline()[:-1]
    s = None
    config.close()
    opc, argus = getopt.getopt(sys.argv[1:], 'v')
    guardarDatos = False
    for o, a in opc:
        guardarDatos = True
    global _COUNTER
    _COUNTER = mp.Value('i', 0)
    all_theta = np.loadtxt(
        os.path.join(rutaThetas, "thetas.txt"),
        comments="#", delimiter=" ", unpack=False)
    max_conexiones = 5
    # Creamos el socket con la familia AF_INET y el tipo SOCK_STREAM
    for res in socket.getaddrinfo(host, puerto):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error:
            s = None
            continue
        try:
            print(sa)
            s.bind(sa)
            s.listen(1)
            hijos = concurrent.futures.ProcessPoolExecutor()
        except socket.error:
           
            s.close()
            s = None
            continue
        break
    if s is None:
        print ('could not open socket')
        sys.exit(1)
    try:
        while True:
            # Acepta una conexion y crea un nuevo socket para la comunicacion
            skt_cli, direccion = s.accept()
            print("[*] Conexion establecida con %s:%d" % (
                direccion[0], direccion[1]))

            # Creo hilos para poder atender a varios clientes al mismo tiempo
            hijos.submit(
                conexion, skt_cli, direccion[0], direccion[1],
                all_theta, guardarDatos)
    except KeyboardInterrupt:
        print("\n Servidor cerrado. Chauu.")
        s.close()
if __name__ == "__main__":
    servidor()

