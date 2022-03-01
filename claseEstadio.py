from os import curdir
from claseCapacEstadio import CapacEstadio

class Estadio (object):
    __nombre = None
    __ciudad = None
    __capacMax = None
    __capacEstadio = []       #clase asociacion, que contiene como atributo lista de partidos
    def __init__ (self,nom, ciudad,capacMax):
        self.__nombre = nom
        self.__ciudad = ciudad
        self.__capacMax = capacMax
        self.__capacEstadio = []

    def mostrarEstadio (self):
        print("\nDatos del Estadio: ")
        print("Nombre: {}\nCiudad: {} - Capacidad Max: {}".format(self.__nombre, self.__ciudad, self.__capacMax))
        if len(self.__capacEstadio) != 0:
            for capacE in self.__capacEstadio:
                capacE.mostrarCapacEstadio()
        else:
            print("{} no ha registrado un partido en el dia de hoy!\n".format(self.__nombre))

    def getNombre (self):
        return self.__nombre
    def getCiudad (self):
        return self.__ciudad
    def getCapacMax (self):
        return self.__capacMax
    
    def addCapacidadEstadio (self, unPartido,cantPoli, cantHab):     #recibimos instancia de partido y params de clase asociacion
        #creamos la clase asociacion dentro del metodo
        capacEst = CapacEstadio (self, unPartido)
        capacEst.cantidadPolicias (cantPoli)
        capacEst.cantidadHabitantes (cantHab)

        self.__capacEstadio.append (capacEst)

    def toJSON (self):
        dicc = dict (
            __class__ = self.__class__.__name__,
            __atributos__ = dict (
                nom = self.__nombre,
                ciudad = self.__ciudad,
                capacMax = self.__capacMax
            )
        )
        return dicc