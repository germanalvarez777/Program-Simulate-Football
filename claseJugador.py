import re
from clasePersona import Persona
class Jugador (Persona):
    __nroCamiseta = None
    __posicionCampo = None
    __apodo = None
    __goles = []
    def __init__ (self,nom, apell, nac, edad, nroC = 0,posic='', apodo=''):
        super().__init__ (nom, apell, nac, edad)
        self.__nroCamiseta = nroC
        self.__posicionCampo = posic
        self.__apodo = apodo
        self.__goles = []           #clase que modela

    def mostrarPersona (self):
        super().mostrarPersona ()
        print("---------------------------------------------------")
        print("Numero Camiseta: {} - Posicion: {}\nApodo: {}".format(self.__nroCamiseta, self.__posicionCampo, self.__apodo))
        if len(self.__goles) > 0:
            print("Cantidad de goles convertidos: %d" %(len(self.__goles)))
        else:
            print("Todavia no ha convertido algun gol!\n")

    def getNroCamiseta (self):
        return self.__nroCamiseta
    def getPosicionCampo (self):
        return self.__posicionCampo
    def getApodo (self):
        return self.__apodo

    def getGolesJugador (self):
        return self.__goles
    
    def getCantGolesJug (self):
        cant = len(self.__goles)
        return cant

    def addGolJug (self, unGol):
        self.__goles.append(unGol)


    def __gt__ (self, otroJugador):
        return len(self.__goles) > otroJugador.getCantGolesJug()