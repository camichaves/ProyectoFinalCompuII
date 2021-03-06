import socket
import numpy as np
import re
from predictOneVsAll import predictOneVsAll
import concurrent.futures
import multiprocessing as mp
from datetime import datetime
import getopt
import sys
import os
from filelock import FileLock
from configparser import ConfigParser


def conexion(all_theta, guardar, recibido):
    with _COUNTER.get_lock():
        _COUNTER.value += 1
        print("Cantidad de numeros calculados:")
        print(_COUNTER.value)
    # Recibimos el mensaje, con el metodo recv recibimos datos y como parametro
    # la cantidad de bytes para recibir
    try:
        mat = re.sub("\s+", ",", recibido)
        mat = mat.replace('[,', '[')
        matriz = eval(mat)
        matriz = np.asarray(matriz)
        gray = np.dot(matriz[..., :3], [0.2989, 0.5870, 0.114])
        gray = np.transpose(gray)
        gray /= 255
    except:
        print("No se hizo el array")
        return -1
    pred = predictOneVsAll(all_theta, gray.ravel())
    print('Prediccion: {}'.format(*pred))
    print("Prediccion lista")
    result = pred
    if(guardar):
        print("guardando data...")
        linea = str(datetime.now()) + ", " + str(_COUNTER.value) + ", " + str(pred) + "\n"
        try:
            lock = FileLock("archivo.lock")
            with lock:
                    print("Lock acquired.")
                    open("historial.log", "a+").write(linea)
                    print("Listo")
        except:
            print("Ocurriò un problema al guardar la info en el archivo")
    # Respuesta al Cliente
    print("Calcule: ")
    print(pred)
    return str(result)


def servidor():
    try:
        parser = ConfigParser()
        parser.read('serv.conf')
        puerto = int(parser.get('SOCKET_CONF', 'puerto'))
        ipvnro = int(parser.get('SOCKET_CONF', 'ipv'))
        host=parser.get('SOCKET_CONF', 'host')
        rutaThetas = parser.get('FUNCION_PREDICTORA', 'thetas')
    except:
        print("Ocurriò un problema al leer el archivo de configuracion :(")
        return
    s = None
    try:
        opc, argus = getopt.getopt(sys.argv[1:], 's')
    except:
        print("Argumentos incorrectos :(")
        return
    guardarDatos = False
    for o, a in opc:
        guardarDatos = True
    global _COUNTER
    _COUNTER = mp.Value('i', 0)
    all_theta = np.loadtxt(
        os.path.join(rutaThetas, "thetas.txt"),
        comments="#", delimiter=" ", unpack=False)
    # Creamos el socket con la familia AF_INET y el tipo SOCK_STREAM
    socketFamily=''
    if(ipvnro == 6):
        socketFamily=socket.AF_INET6
    else:
        socketFamily=socket.AF_INET
    for res in socket.getaddrinfo(host, puerto, socketFamily):
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
            # for de 2 imgs
            recib = skt_cli.recv(243040)
            recib = recib.decode('utf-8')
            recibido = recib.split("--", 1)
            print(recibido[1])
            hh = []
            hh.append(hijos.submit(conexion, all_theta, guardarDatos, re.sub("--", "", recibido[0])))
            hh.append(hijos.submit(conexion, all_theta, guardarDatos, re.sub("-", "", recibido[1])))
            #as_completed(
            rta = []
            for f in concurrent.futures.as_completed(hh):
                #rta = rta + str(f.result()) + "-"
                rta.append(f.result())
            
            # Respuesta al Cliente
            print(str(rta))
            try:
                skt_cli.send(str(rta).encode('utf-8'))
                print("Respuesta enviada :)")
            except:
                print("Ocurriò un problema al enviar la respuesta :(")
            skt_cli.close()

            
    except KeyboardInterrupt:
        print("\n Servidor cerrado. Chauu.")
        s.close()
        
        
if __name__ == "__main__":
    servidor()

