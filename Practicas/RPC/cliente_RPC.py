import xmlrpc.client
import datetime
import os
host = input("Ingrese la IP del servidor: ")
aux = 'http://'
server = aux+str(host)+':8000' 
rpc = xmlrpc.client.ServerProxy(server)
#prueba = "prueba2"
#cambio = "nombre"
#print(rcp.system.listMethods())
#rcp.RENAME(str(prueba),str(cambio))
print("\nOperaciones de archivos:")
print("\t1. CREATE")
print("\t2. READ")
print("\t3. WRITE")
print("\t4. RENAME")
print("\t5. REMOVE")
print("\t6. MKDIR")
print("\t7. RMDIR")
print("\t8. READDIR")
print("\t9. CD")
print("\t10. Salir")
usuario = input("Ingresa tu nombre de usuario: ")
contraseña = input("Ingresa tu contraseña: ")
direccion = rpc.LOGGING(usuario,contraseña)
while True:
    #os.system("cls")
    print("\t")
    print("Te encuentras en ",str(direccion))
    opc = input("Ingresa una opción: ")
    if(opc == "1"):
        nombre = input("Ingresa el nombre del archivo a crear: ")
        rpc.CREATE(str(nombre),direccion)
    elif(opc == "2"):
        nombre = input("Ingresa el nombre del archivo a leer: ")
        cadena = rpc.READ(str(nombre),direccion)
        print(str(cadena))
    elif(opc == "3"):
        nombre = input("Ingresa el nombre del archivo en el que escribir: ")
        texto = input("Ingresa una cadena de texto: ")
        rpc.WRITE(str(nombre),str(texto),direccion)
    elif(opc == "4"):
        nombre = input("Ingrese el nombre original del archivo: ")
        nombre_nuevo = input("Ingrese el nombre nuevo del archivo: ")
        rpc.RENAME(str(nombre),str(nombre_nuevo),direccion)
    elif(opc == "5"):
        nombre = input("Ingrese el nombre del archivo a remover: ")
        rpc.REMOVE(str(nombre),direccion)
    elif(opc == "6"):
        nombre = input("Ingrese el nombre del fichero a crear: ")
        rpc.MKDIR(str(nombre),direccion)
    elif(opc == "7"):
        nombre = input("Ingrese el nombre del fichero a borrar: ")
        rpc.RMDIR(str(nombre),direccion)
    elif(opc == "8"):
        lista = rpc.READDIR(direccion)
        print(lista)
    elif(opc == "9"):
        aux = direccion
        directorio = input("Ingresa el directorio: ")
        direccion = rpc.CD(directorio,aux)
    elif(opc == "10"):
        break
    else:
        print("Operacion invalida !")
        input("Presione una tecla para continuar...")
print("Exit")