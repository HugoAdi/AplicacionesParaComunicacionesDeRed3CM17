import datetime
import socket
import os
import pickle

HOST = input("Ingrese la IP del servidor: ") 
PORT = int(input("Ingrese el puerto del servidor: "))
buffer_size = 1024 

############### FUNCIONES DEL CLIENTE ###############
def imprimirTablero(data):
    linea = "    "
    for i in range(0, 4*l - 3):
        linea += "_"

    letras ="    A   B   C"
    if(l == 5): 
        letras += "   D   E"
    print(letras)

    for i in range(0, l):
        print( i + 1, end='   ')
        for j in range(0, l):
            dato = " " if (data[i][j] == "") else data[i][j]
            barra = " | " if (j < l - 1) else "  " 
            print(dato + barra,end='')
        if i < l - 1:
            print("\n" + linea)
    print("\n")

def checarJugada(jugada_cliente,l,Tablero):
    coordenadas = jugada_cliente.split(',') #Convertimos nuestro string a una lista
    if(len(coordenadas)==2):
        if( set(coordenadas[0]).issubset(set(x_mov)) and coordenadas[0] != '' and set(coordenadas[1]).issubset(set(y_mov)) and coordenadas[1] != ''):
            if(Tablero[int( coordenadas[1] ) - 1][ord( coordenadas[0] ) - 65] == ''):
                return True
    else:
        print("Casilla ocupada")
        return False
    print("Intenta de nuevo")
    return False


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:

    TCPClientSocket.connect((HOST,PORT)) #Conexion del cliente

    print("Dificultades del juego \n1.Principiante (Tres en linea)\n2.Avanzado (cinco en linea)\n")
    dificultad = input("Ingresa la dificultad:")
    x_mov = ['A','B','C']
    y_mov = ['1','2','3']
    if(int(dificultad) == 1): 
        l=3
    elif(int(dificultad) == 2):
        l=5
        x_mov.append('D')
        x_mov.append('E')
        y_mov.append('4')
        y_mov.append('5')
    print("Envio del nivel")
    TCPClientSocket.sendall(str.encode(dificultad))
    os.system("cls") #despejamos la consola

    print("Comienzo del juego")
    while(True):
        data = pickle.loads(TCPClientSocket.recv(buffer_size)) #Recibimos el primer tablero
        if(data[l] == 'FIN'):
            os.system("cls")
            print(data[l+1]) #l+1 contiene el resultado de la partida
            print("Tiempo de juego:"+data[l+2]) #l+2 contiene el tiempo de la partida
            imprimirTablero(data)
            break
        if(not data[l]):
            while(True):
                os.system("cls")
                imprimirTablero(data)
                jugada_cliente = input("Ingrese coordenada (letra,numero): ")
                if(checarJugada(jugada_cliente,l,data)):
                    TCPClientSocket.sendall(pickle.dumps(jugada_cliente))
                    break
                else:
                    print("Intenta de nuevo...")
            

