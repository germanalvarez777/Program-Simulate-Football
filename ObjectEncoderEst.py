import json
from claseListaEstadios import ListaEstadios
from claseNodo import Nodo
from claseEstadio import Estadio

class ObjectEncoderEst:                #clase sin atributos
    def guardarArchJSON (self, dicc, archivo):
        with open(archivo, 'w', encoding = "UTF-8") as destino:
            json.dump (dicc, destino, indent = 4)
            destino.close()
    
    def leerArchJSON (self, archivo):
        with open (archivo, encoding = "UTF-8") as fuente:
            dicc = json.load(fuente)
            fuente.close()
            return dicc
        
    def decodificarDicc (self, dicc):
        if "__class__" not in dicc:
            return dicc
        else:
            class_name = dicc["__class__"]
            class_= eval(class_name)
            if class_name == "ListaEstadios":
                estadios = dicc["estadios"]
                manejador = class_()
                for i in range(len(estadios)):
                    dEst = estadios[i]
                    class_name = dEst.pop("__class__")
                    class_= eval(class_name)
                    atributos = dEst["__atributos__"]
                    unEstadio = class_(**atributos)

                    manejador.agregarElemento (unEstadio)       #inserto cada estadio al final de la lista enlazada
                
                return manejador