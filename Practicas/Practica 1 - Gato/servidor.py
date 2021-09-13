import datetime
import socket
import os
import pickle
import random

HOST = input("Ingrese la IP del servidor: ") 
PORT = int(input("Ingrese el puerto del servidor: "))
buffer_size = 1024 

############### FUNCIONES DEL SERVIDOR ###############
def inicTablero(lineas):
    for i in range (0,lineas):
        aux = []
        for j in range (0,lineas):
            aux.append('')
        Tablero.append(aux)

def imprimirTablero():
    linea = ""
    for i in range(0, 4*l - 3):
        linea += "_"

    for i in range(0, l):
        for j in range(0, l):
            dato = " " if (Tablero[i][j] == "") else Tablero[i][j]
            barra = " | " if (j < l - 1) else "  " 
            print(dato + barra,end='')
        if i < l - 1:
            print("\n" + linea)
    print("\n")

def checarJugada(jugada_cliente,l):
    coordenadas = jugada_cliente.split(',') #Convertimos nuestro string a una lista
    if(len(coordenadas)==2):
        if( set(coordenadas[0]).issubset(set(x_mov)) and coordenadas[0] != '' and set(coordenadas[1]).issubset(set(y_mov)) and coordenadas[1] != ''):
            return declararCoordenadas(int(coordenadas[1])-1,ord(coordenadas[0])-65, l)
    else:
        return False

def declararCoordenadas(x,y,l):
    if(Tablero[x][y]==''):
        Tablero[x][y] = "X" if (turno_Servidor) else "O"
        pos = y + 1 + l * x
        if(pos in posLibres):
            posLibres.remove(pos)
        return checarTablero(x,y,l)
    else:
        return False

def checarTablero(x,y,l):
    if(turno_Servidor):
        sym = "X"
    else:
        sym = "O"
    filaRecorrida = True

    for j in range(0,l):
        if(Tablero[x][j] != sym):
            filaRecorrida = False
            break
    
    for i in range(0,l):
        if(Tablero[i][y] != sym):
            filaRecorrida = False
            break
    
    for i in range(0,l):
        if(Tablero[i][i] != sym):
            filaRecorrida = False
            break

    for i in range(0,l):
        if(Tablero[i][l-1-i] != sym):
            filaRecorrida = False
            break

    if(not filaRecorrida and len(posLibres)>0): #Significa que el juego sigue
        return True
    
    os.system("cls")
    if(turno_Servidor and filaRecorrida):
        res = "El servidor gano la partida"
        print("El servidor gano la partida")
    elif(not turno_Servidor and filaRecorrida):
        res = "El usuario gano la partida"
        print("El usuario gano la partida")
    if(not filaRecorrida):
        res = "El juego ha empatado"
        print("El juego ha empatado")
    
    hora_fin = datetime.datetime.now()
    tiempo_final = hora_fin - hora_inicio

    data = []
    data = Tablero.copy()
    data.append("FIN")
    data.append(res)
    data.append(str(tiempo_final))
    Client_conn.sendall(pickle.dumps(data))
    global juego_Finalizado
    juego_Finalizado = True
    return juego_Finalizado

def jugarServidor(l):
    jugada_Servidor = random.choice(posLibres)
    x = ( l if (jugada_Servidor % l == 0) else jugada_Servidor % l ) - 1
    y =  int( (jugada_Servidor - 1) / l) 
    if( not declararCoordenadas(y, x, l) ):
        jugarServidor( l )
    

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen()
    print("El servidor TCP está disponible y en espera de solicitudes")

    while True:
        Client_conn, Client_addr = TCPServerSocket.accept()
        with Client_conn:
            print("Conectado a", Client_addr)
            dificultad = Client_conn.recv(buffer_size)
            print("Dificultad: ",dificultad)
            hora_inicio = datetime.datetime.now()
            posLibres = []
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
            for i in range (1, l* l + 1):
                posLibres.append(i)
            Tablero = []
            inicTablero(l)
            numCeldas = 0
            juego_Finalizado = 0
            turno_Servidor = 0
            while (not juego_Finalizado):
                os.system("cls")
                imprimirTablero()
                if(turno_Servidor):
                    jugarServidor(l)
                    turno_Servidor = not turno_Servidor
                    numCeldas += 1
                else:
                    data = []
                    data = Tablero.copy()
                    data.append(turno_Servidor)
                    Client_conn.sendall(pickle.dumps(data))
                    jugada_cliente = Client_conn.recv(buffer_size)
                    if (checarJugada(pickle.loads(jugada_cliente),l)):
                        imprimirTablero()
                        turno_Servidor = not turno_Servidor
                        numCeldas += 1
