from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer
import shutil
import sys
import os
#directorio = os.getcwd()
host = input("Ingrese la IP del servidor: ")
usuarios = {'Eduardo':['Eduardo','eduardo123'],'Juan':['Juan','juan123'],'Sofia':['Sofia','sofia123']}
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
with SimpleXMLRPCServer((host, 8000),requestHandler=RequestHandler,allow_none=True) as server:
    server.register_introspection_functions()
    print(os.getcwd())
    class Operaciones:
        def LOGGING(self, usuario, contraseña):
            data = usuarios.get(usuario)
            if data[1] == contraseña:
                print("Ok")
                return data[0]
            else:
                print("Usuario y/o contraseña invalidos")
        def CREATE(self,nombre,directorio):
            path = os.path.join(directorio,nombre)
            file = open(path,"w")
            print("Ok")
            file.close()
        def READ(self,nombre,directorio):
            path = os.path.join(directorio,nombre)
            file = open(path,"r")
            file_user = file.read()
            print("Ok")
            file.close()
            return file_user
        def WRITE(self,nombre,texto,directorio):
            path = os.path.join(directorio,nombre)
            file = open(path,"a")
            file.write(texto)
            print("Ok")
            file.close()
        def RENAME(self,nombre,nombre_nuevo,directorio):
            path = os.path.join(directorio,nombre)
            path2 = os.path.join(directorio,nombre_nuevo)
            print(path)
            try:
                os.rename(path,path2)
                print("Ok")
            except IsADirectoryError:
                print("El origen es un archivo pero el destino es un directorio")
            except NotADirectoryError:
                print("El origen es un directorio pero el destino es un archivo")
            except OSError as error:
                print(error)
        def REMOVE(self,nombre,directorio):
            path = os.path.join(directorio,nombre)
            try:
                os.remove(path)
                print("Ok")
            except OSError as error:
                print(error)
        def MKDIR(self,nombre,directorio):
            path = os.path.join(directorio,nombre)
            try:
                os.mkdir(path)
                print("Ok")
            except OSError as error:
                print(error)
        def RMDIR(self,nombre,directorio):
            path = os.path.join(directorio,nombre)
            try:
                os.rmdir(path)
                print("Ok")
            except OSError as error:
                print(error)
        def READDIR(self,directorio):
            path = os.path.join(directorio)
            try:
                lista = os.listdir(path)
                print("Ok")
            except OSError as error:
                print(error)
            #print("Archivos y ficheros en '",directorio,"' :")
            #print(lista)
            return lista
        def CD(self,directorio_nuevo,directorio):
            path = os.path.join(directorio,directorio_nuevo)
            try:
                os.chdir(path)
                print("Ok")
            except OSError as error:
                print(error)
            return path
        def getDir(self):
            return path
    server.register_instance(Operaciones())
    server.serve_forever()

