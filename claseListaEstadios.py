import csv
import re
import json
from zope.interface import implementer
from claseNodo import Nodo
from claseEstadio import Estadio
from claseIElemento import IElemento

@implementer(IElemento)     #implementamos la interfaz en esta clase, ofrecemos implementacion a todos sus metodos

class ListaEstadios (object):
    __actual = None
    __comienzo = None
    __indice = None
    __tope = None
    def __init__ (self):
        self.__comienzo = None
        self.__actual = None
        self.__indice = 0
        self.__tope = 0
    
    def __iter__ (self):
        return self
    
    def __next__ (self):
        if self.__indice == self.__tope:
            self.__indice = 0
            self.__actual = self.__comienzo
            raise StopIteration
        else:
            self.__indice += 1
            dato = self.__actual.getDato()
            self.__actual = self.__actual.getSiguiente()
            return dato

    def insertarElemento (self, pos, estadio):
        pos = pos-1
        if pos >= 0 and pos <= self.__tope:     #<= tope por si la lista esta vacia
            if pos == 0:
                nodo = Nodo (estadio)
                nodo.setSiguiente(self.__comienzo)
                self.__comienzo = nodo
                self.__actual = nodo
                self.__tope += 1
            else:
                ant = self.__comienzo
                aux = ant           #aqui debia colocarlo asi, sino error
                cont = 0
                band = False
                while (aux != None and band == False):
                    if cont == pos:
                        band = True
                    else:
                        cont += 1
                        ant = aux
                        aux = aux.getSiguiente()
                if band == True or cont == pos:
                    nodo = Nodo (estadio)
                    ant.setSiguiente(nodo)
                    nodo.setSiguiente(aux)
                    self.__tope += 1
        else:
            raise Exception ('Posicion a insertar estadio no es valida!')

    def agregarElemento (self, estadio):    #agregar estadio al final de la lista
        if self.__comienzo == None:
            nodo = Nodo (estadio)
            nodo.setSiguiente(self.__comienzo)
            self.__comienzo = nodo
            self.__actual = nodo
            self.__tope += 1
        else:
            ant = self.__comienzo
            aux = ant.getSiguiente()
            while (aux != None):
                ant = aux
                aux = aux.getSiguiente()
            
            nodo = Nodo (estadio)
            ant.setSiguiente(nodo)
            nodo.setSiguiente(aux)      #igual a: nodo.setSiguiente(None)
            self.__tope += 1


    def mostrarElemento (self, pos):
        pos = pos - 1
        if pos >= 0 and pos < self.__tope:
            if pos == 0:
                aux = self.__comienzo
                print("\n-----El estadio a mostrar es----")
                aux.getDato().mostrarEstadio()
            else:
                cont = 0
                aux = self.__comienzo
                band == False
                while (aux != None and band == False):
                    if cont == pos:
                        band = True
                    else:
                        aux = aux.getSiguiente()
                        cont += 1
                
                if cont == pos or band == True:
                    print("\n-----El estadio a mostrar es----")
                    aux.getDato().mostrarEstadio()

        else:
            raise Exception ('Posicion a mostrar estadio no es valida!')

    """
    def testListaEstadio (self):
        archivo = open ('estadios.csv', 'r')
        Reader = csv.reader (archivo, delimiter=';')
        band = True
        i = 1
        for fila in Reader:
            if band:
                #Nombre;Ciudad;Capac Maxima
                band = not band     #salteamos cabecera
            else:
                if re.search ('fin', fila[0]):
                    print("\nDatos de un estadio invalidos")
                else:
                    nom = fila[0]
                    ciudad = fila[1]
                    capacM = int(fila[2].replace('.',''))
                    unEstadio = Estadio (nom,ciudad,capacM)
                    #self.agregarElemento(unEstadio)     #(Funciona bien)los añado al final de la lista enlazada
                    self.insertarElemento(i, unEstadio)
                    i += 1

        archivo.close()     """

    def toJSON (self):
        dicc = dict(
            __class__ = self.__class__.__name__,
            estadios = [dato.toJSON() for dato in self]
        )
        return dicc


    def mostrarEstadios (self):
        print("\nMostramos el listado de Estadios disponibles: ")
        for dato in self:
            print('/'.center(45,'/'))
            dato.mostrarEstadio()

    def nombresEstadios (self):
        print("Mostramos el nombre de todos los estadios: ")
        for dato in self:
            nom = dato.getNombre()
            print("----->[%s]"%(nom))

    def buscarEstadio (self, nomEst):
        band = False
        aux = self.__comienzo
        estadio = None
        while (aux != None and band == False):
            if aux.getDato().getNombre().lower() == nomEst.lower():
                band = True
                estadio = aux.getDato()
            else:
                aux = aux.getSiguiente()

        return estadio      #si lo encuentra lo retorna, sino retorna None

    def getListaEstadios (self):
        return self.__tope
    
    def obtenerUnEstadio (self, posicion):
        estadio = None
        if posicion >= 1 and posicion <= self.__tope:
            if posicion == 1:
                estadio = self.__comienzo.getDato()
            else:
                aux = self.__comienzo
                i = 1
                band = False
                while (aux != None and band == False):
                    if i == posicion:
                        band = True
                        estadio = aux.getDato()
                    else:
                        i += 1
                        aux = aux.getSiguiente()

        return estadio
