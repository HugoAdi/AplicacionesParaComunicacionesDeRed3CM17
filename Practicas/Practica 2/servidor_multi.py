import datetime
import socket
import os
import pickle
import random
import threading


HOST = input("Ingrese la IP del servidor: ") 
PORT = int(input("Ingrese el puerto del servidor: "))
num_Conexiones = int(input("Ingrese la cantidad de conexiones: "))
buffer_size = 1024
hora_inicio = datetime.datetime.now()
l = 0
posLibres = []
conexiones = []
identificaciones = []
Tablero = []
juego_Finalizado = 0
fin = ""
usuario_ganador = ""
x_mov = ['A','B','C']
y_mov = ['1','2','3']


############### FUNCIONES DEL SERVIDOR ###############
def inicTablero(lineas):
    Tablero.clear()
    for i in range (0,lineas):
        aux = []
        for j in range (0,lineas):
            aux.append('')
        Tablero.append(aux)

def imprimirTablero():
    linea = "    "
    for i in range(0, 4*l - 3):
        linea += "_"
    letras = "    A   B   C"
    if(l == 5):
        letras += "   D   E"
    print(letras)
    for i in range(0, l):
        print(i+1,end='   ')
        for j in range(0, l):
            dato = " " if (Tablero[i][j] == "") else Tablero[i][j]
            barra = " | " if (j < l - 1) else "  " 
            print(dato + barra,end='')
        if i < l - 1:
            print("\n" + linea)
    print("\n")

def checarJugada(jugada_cliente,ident):
    coordenadas = jugada_cliente.split(',') #Convertimos nuestro string a una lista
    if(len(coordenadas)==2):
        if( set(coordenadas[0]).issubset(set(x_mov)) and coordenadas[0] != '' and set(coordenadas[1]).issubset(set(y_mov)) and coordenadas[1] != ''):
            return declararCoordenadas(int(coordenadas[1])-1,ord(coordenadas[0])-65, l,ident)
    else:
        return False

def declararCoordenadas(x,y,l,ident):
    if(Tablero[x][y]==''):
        Tablero[x][y] = ident
        pos = y + 1 + l * x
        if(pos in posLibres):
            posLibres.remove(pos)
        return True#checarTablero(x,y,l)
    else:
        return False

def checarTablero(x,y,ident):
    sym = ident
    filaRecorrida = True
    print(posLibres)

    for j in range(0,l):
        if(Tablero[x][j] != sym):
            filaRecorrida = False
            break
    if(not filaRecorrida):
        filaRecorrida = True
        for i in range(0,l):
            if(Tablero[i][y] != sym):
                filaRecorrida = False
                break

    if(not filaRecorrida and x == y):
        filaRecorrida = True
        for i in range(0,l):
            if(Tablero[i][i] != sym):
                filaRecorrida = False
                break
    if(not filaRecorrida and (x+y) == (l-1)):
        filaRecorrida = True
        for i in range(0,l):
            if(Tablero[i][l-1-i] != sym):
                filaRecorrida = False
                break

    if(not filaRecorrida and len(posLibres)>0): #Significa que el juego sigue
        return False
    
    global usuario_ganador
    if(not filaRecorrida):
        usuario_ganador = "-1"
        return True
    usuario_ganador = ident
    return True
    #os.system("cls")
    #if(turno_Servidor and filaRecorrida):
    #    res = "El servidor gano la partida"
    #    print("El servidor gano la partida")
    #elif(not turno_Servidor and filaRecorrida):
    #    res = "El usuario gano la partida"
    #    print("El usuario gano la partida")
    #if(not filaRecorrida):
    #    res = "El juego ha empatado"
    #    print("El juego ha empatado")
    
    #hora_fin = datetime.datetime.now()
    #tiempo_final = hora_fin - hora_inicio

    #data = []
    #data = Tablero.copy()
    #data.append("FIN")
    #data.append(res)
    #data.append(str(tiempo_final))
    #Client_conn.sendall(pickle.dumps(data))
    #global juego_Finalizado
    #juego_Finalizado = True
    #return juego_Finalizado

#def jugarServidor(l):
#    jugada_Servidor = random.choice(posLibres)
#    x = ( l if (jugada_Servidor % l == 0) else jugada_Servidor % l ) - 1
#    y =  int( (jugada_Servidor - 1) / l) 
#    if( not declararCoordenadas(y, x, l) ):
#        jugarServidor( l )

def Tablero_A_Clientes(juego_Finalizado = 0):
    cont = 0
    for conect in conexiones:
        data = []
        data = Tablero.copy()
        if(juego_Finalizado == 1):
            data.append('FIN')
            if(usuario_ganador == "-1"):
                data.append("Empate")
            elif(usuario_ganador == identificaciones[cont]):
                data.append("Ganaste ! ")
            else:
                data.append("Eres un perdedor :(")
            print(hora_inicio)
            tiempo_final = str(datetime.datetime.now() - hora_inicio)
            data.append("Tiempo: "+tiempo_final)
            cont+=1
        else:
            data.append(juego_Finalizado)
        print(data)
        conect.sendall(pickle.dumps(data))

def ServirPorSiempre(TCPServerSocket, num_Conexiones):
    try:
        while True:
            Client_conn, Client_addr = TCPServerSocket.accept() #Conexion al cliente
            dificultad = Client_conn.recv(buffer_size)

            global l
            if(l == 0):
                hora_inicio = datetime.datetime.now()
                if(int(dificultad) == 1):
                    l=3
                else:
                    l=5
                    x_mov.append('D')
                    x_mov.append('E')
                    y_mov.append('4')
                    y_mov.append('5')
                posLibres.clear()
                for i in range (1, l* l + 1):
                    posLibres.append(i)
                for i in range (1, l* l + 1):
                    identificaciones.append(str(i))
                inicTablero(l)
            conexiones.append(Client_conn)
            #print(len(conexiones))
            ident = identificaciones[ len(conexiones) - 1 ]
            thread_read = threading.Thread(target=recibir_jugada,args=[Client_conn, Client_addr,ident])
            thread_read.start()
            gestionan_conexiones()
    except Exception as e:
        print(e)


def recibir_jugada(conn,addr,ident):
    try:
        actual_thread = threading.current_thread()
        juego_Finalizado = 0
        while (juego_Finalizado != 1):
            data = []
            data = Tablero.copy()
            data.append(juego_Finalizado)
            Tablero_A_Clientes()
            #se recibe jugada del cliente
            jugada_cliente = conn.recv(buffer_size)
            if(checarJugada(pickle.loads(jugada_cliente),ident)):
                coords = pickle.loads(jugada_cliente).split(',')
                juego_Finalizado = checarTablero(int(coords[1]) -1, ord(coords[0])-65,ident)
        Tablero_A_Clientes(juego_Finalizado)
    except Exception as e:
        print(e)
    finally:
        #print(conn)
        #print(conexiones)
        conexiones.remove(conn)
        #print(conexiones)
        conn.close()
        if(len(conexiones) == 0):
            Tablero.clear()
            global l
            l = 0

def gestionan_conexiones():
    for conect in conexiones:
        if (conect.fileno() == -1): 
            conexiones.remove(conn)
    print("Hilos activos:",threading.active_count())
    #print("enum",threading.enumerate())
    print("conexiones: ", len(conexiones))



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen(num_Conexiones)
    print("El servidor TCP está disponible y en espera de solicitudes")
    ServirPorSiempre(TCPServerSocket,num_Conexiones)

    