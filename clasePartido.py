from datetime import date
class Partido(object):
    identificador = 0
    __nombre = None
    __instancia = None
    __duracion = None
    __fecha = None
    __equipos = []      #lista con 2 elementos
    __goles = []
    __arbitro = None

    def __init__ (self, nom, inst, arbitro):        
        self.__nombre = nom
        self.__instancia = inst
        self.__duracion = 90
        self.__fecha = str(date.today())
        self.__arbitro = arbitro

        i = self.__fecha.find('-')          #!= -1 encontro el char
        j = self.__fecha.rfind ('-')        #rfind hace la busqueda desde el final hacia adelante
        anio = self.__fecha[:i]
        mes = self.__fecha[i+1:j]
        dia = self.__fecha[j+1:]
        self.__fecha = str(dia+'-'+mes+'-'+anio)

        self.__equipos = []
        self.__goles = []
        #convierto la fecha en formato ARG

    def addEquipo (self, unEquip):
        if len(self.__equipos) < 2:
            self.__equipos.append (unEquip)
            unEquip.partidoJugado (self)        #agregamos para la inst equipo el partido
        else:
            print("\nYa estan seleccionados los dos Equipos a jugar!\n")
    
    def getEquipo1 (self):
        return self.__equipos[0]
    def getEquipo2 (self):
        return self.__equipos[1]

    def getNombrePartido (self):
        return self.__nombre
    def getFechaPartido (self):
        return self.__fecha

    def getDuracionPartido (self):
        return self.__duracion
    def tiempoExtra (self):
        self.__duracion += 30
    
    def anotarGol (self, unGol):
        self.__goles.append(unGol)
    def getGolesPartido (self):
        return self.__goles
    def getFechaPartido (self):
        return self.__fecha
    def getInstancia (self):
        return self.__instancia

    def getArbitroPartido (self):
        return self.__arbitro

    #Estos dos metodos son para guardar resultado de partido en la base de datos
    def getGolesA (self):
        result_part = self.__arbitro.getResultPartido()
        goles = 0
        for rp in result_part:
            if rp.getPartido_Result().getNombrePartido() == self.__nombre:
                goles = rp.getCantGolesEqA()
        
        return goles

    def getGolesB (self):
        result_part = self.__arbitro.getResultPartido()
        goles = 0
        for rp in result_part:
            if rp.getPartido_Result().getNombrePartido() == self.__nombre:
                goles = rp.getCantGolesEqB()
        
        return goles


    def mostrarPartido (self):
        print("\nNombre del Partido: {} - Instancia: {}\nDuracion: {} min - Fecha: {}".format(self.__nombre, self.__instancia, self.__duracion, self.__fecha))
        print("\n----Datos de los 2 Equipos----")
        for equip in self.__equipos:
            print("".center(45,'='))
            equip.mostrarEquipo()
        print("\n----Datos de los goles anotados----")
        if len(self.__goles) == 0:
            print("\nEl partido termino sin goles!\n")
        else:
            print("\nArbitro del Partido: {}".format(self.__arbitro.getNombre()+' '+self.__arbitro.getApellido()))
            print ("\nCantidad de goles: %d"%(len(self.__goles)))
            self.__arbitro.mostrarResultado (self)
            
            input("\nMostramos info de los goles:")
            for gol in self.__goles:
                print("".center(35,'-'))
                gol.mostrarGol()

#"""
from claseJugador import Jugador
from claseEquipo import Equipo
from claseArbitro import Arbitro
from claseEstadio import Estadio

from claseResultPartido import ResultPartido
from claseGol import Gol

if __name__ == '__main__':
    
    eq1 = Equipo ('Barcelona','Cataluña, España')
    jug2 = Jugador ('Rogelio','Funes','Arg',22, 42,'Defensa','Roger')
    eq1.addJugador(jug2)
    jug1 = Jugador ('Cristian','Eriksen','Din',29, 10,'Mediocampista','Eriksen')
    eq1.addJugador(jug1)
    eq1.addCuerpoTec('Xavier','Hernandez','Esp',42,'Entrenador')

    eq2 = Equipo ('Real Madrid', 'Madrid, España')
    jug3 = Jugador('Antonio','Kroos','Alemania',32, 8,'Centrocampista','Toni Kroos')
    eq2.addJugador (jug3)
    jug = Jugador ('Karim','Benzema','Francia',24, 9,'Delantero','Karim')
    eq2.addJugador (jug)
    eq2.addCuerpoTec('Carlo','Anchelotti','Ita',54,'Entrenador')

    arb = Arbitro ('Rogelio','Cesar','Brasil',44,'2003')
    est = Estadio ('Wanda Metropolitano','Madrid',80000)

    partido = Partido ('Amistoso Internacional Barcelona vs Real Madrid','Amistoso',arb)
    partido.addEquipo (eq1)
    partido.addEquipo (eq2)

    est.addCapacidadEstadio (partido, 23300,69766)

    contGolesEqA = 0
    contGolesEqB = 0

    
    unGol = Gol(42,'Primer Tiempo',partido, jug)
    band = eq1.buscarJugador(jug)        #bandera para saber de que equipo es el gol
    if band == True:
        contGolesEqA += 1
    else:
        band = eq2.buscarJugador(jug)
        if band == True:
            contGolesEqB += 1

    
    otroGol = Gol (66,'2do Tiempo',partido,jug2)
    band = eq1.buscarJugador (jug2)
    if band == True:
        contGolesEqA += 1
    else:
        band = eq2.buscarJugador(jug2)
        if band == True:
            contGolesEqB += 1
    
    newGol =Gol (79,'2do Tiempo',partido,jug2)
    band = eq1.buscarJugador (jug2)
    if band == True:
        contGolesEqA += 1
    else:
        band = eq2.buscarJugador(jug2)
        if band == True:
            contGolesEqB += 1

    #cuando ya no se anotan mas goles, guardo el resultado
    arb.guardarResultado(partido, contGolesEqA, contGolesEqB)
    partido.mostrarPartido()

    #"""
