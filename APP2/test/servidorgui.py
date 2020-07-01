import socket
import threading
import time 

def conexion(skt_cli,direccion,port):
	while True:
		# Recibimos el mensaje, con el metodo recv recibimos datos y como parametro
		# la cantidad de bytes para recibir
		recibido = skt_cli.recv(1024)
		result= 'No se ingreso comando valido'
		if recibido == b'close':
		    print("[*] %s:%d se desconectó. " % (direccion, port))
		    skt_cli.close()
		    break		
		elif recibido == b'hora':
		    print("Hora " + time.strftime("%X"))
		    result = time.strftime("%X")
		elif recibido == b'op':
			#Esperamos la operacion que reciba del cliente
		    recibido = skt_cli.recv(1024)
		    operation = recibido.decode('utf-8')
		    try:
		        result = eval(operation)
		    except:
		        result= "Operación no reconocida"

		#Respuesta al Cliente
		skt_cli.send(str(result).encode('utf-8'))
	skt_cli.close()

            


def servidor():

	host = "127.0.0.1"
	puerto = 5555

	max_conexiones = 5
	#Creamos el socket con la familia AF_INET y el tipo SOCK_STREAM
	skt_ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	#Bindeamos la direccion y puerto
	skt_ser.bind((host, puerto))

	#Lo abrimos para que quede a la escucha de clientes
	skt_ser.listen(max_conexiones)
	print ("[*] Esperando conexiones en %s:%d" % (host, puerto))
	try:
		while True:

			# Acepta una conexion y crea un nuevo socket para la comunicacion
			skt_cli, direccion = skt_ser.accept()
			print("[*] Conexion establecida con %s:%d" % (direccion[0], direccion[1]))

			# Creo hilos para poder atender a varios clientes al mismo tiempo
			hilo = threading.Thread(target=conexion,args=(skt_cli, direccion[0],direccion[1]))
			hilo.start()
	except KeyboardInterrupt:
		print("\n Servidor cerrado. Chauu.")
		skt_ser.close()

	


servidor()
