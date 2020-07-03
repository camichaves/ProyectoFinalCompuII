import socket
import threading

puertoapp3 = 5556
host = "127.0.0.1"


def conexion(skt_cli, direccion, port):
    # Recibimos el mensaje, con el metodo recv recibimos datos y como parametro
    # la cantidad de bytes para recibir
    recibido = skt_cli.recv(1024)
    print("[*] %s:%d Se conecto. " % (direccion, port))
    # Me convierto en cliente de la app3
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Realizamos la conexion
        skt.connect((host, puertoapp3))
        print("Se estableció conexión con el servidor")
    except:
        print("No se ha podido establecer la conexion con el servidor")
        return
    skt.send(recibido)

    # Recibimos la respuesta del servidor en data
    data = skt.recv(1024)
    print(" >Respuesta de App3:", data)
    skt.close()
    result = data

    # Respuesta al Cliente
    skt_cli.send(str(result))
    skt_cli.close()


def servidor():
    puerto = 5555

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
            hilo = threading.Thread(target=conexion, args=(skt_cli, direccion[0], direccion[1]))
            hilo.start()
    except KeyboardInterrupt:
        print("\n Servidor cerrado. Chauu.")
        skt_ser.close()


servidor()
