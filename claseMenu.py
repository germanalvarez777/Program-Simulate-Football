import os
import time
import csv
from claseManejaArbitros import ManejaArbitros
from claseListaEstadios import ListaEstadios
from claseManejaEquipos import ManejaEquipos

from ObjectEncoderEst import ObjectEncoderEst
from ObjectEncoderArb import ObjectEncoderArb
from claseEstadio import Estadio

from clasePartido import Partido
from claseGol import Gol
from datetime import date

from random import randint      #para generar nros aleatorios enteros

from models import db
from models import Arbitros,ResultPartido,Partidos


class Menu (object):
    __switcher = None
    __manejArb = None
    __objEncArb = None
    __listaEstadios = None
    __jsonEst = None
    __manejEst = None

    __manejEquip = None
    def __init__ (self):
        self.__switcher = {
            '1': self.opcion1,      #jugar amistoso
            '2': self.opcion2,      #jugar copa de 4 o 8 equipos
            '3': self.opcion3,      #añadir un equipo
            '4': self.opcion4,      #añadir a un jugador de algun equipo
            '5': self.opcion5,      #mostrar info de algun equipo
            '6': self.opcion6,      #mostrar partidos jugados hoy (crear un lista de partidos)
            '7': self.opcion7,      #mostrar info de los estadios, capacidad habitada,etc.
            '8': self.opcion8,      #mostrar info de los arbitros, resultado de los partidos
            '9': self.opcion9,    #añadir nuevo arbitro o estadio
            '10': self.opcion10,    #mostrar los jugadores con mas goles convertidos (osea en los partidos de hoy)
            '11': self.salir
        }
        self.__objEncArb = ObjectEncoderArb()
        dicc = self.__objEncArb.leerArchJSON('arbitros.json')
        self.__manejArb = self.__objEncArb.decodificarDicc(dicc)
        self.__manejArb.guardarArbitrosBD()
        
        self.__jsonEst = ObjectEncoderEst()
        dicc = self.__jsonEst.leerArchJSON('estadios.json')
        self.__manejEst = self.__jsonEst.decodificarDicc(dicc)

        self.__manejEquip = ManejaEquipos()
        self.__manejEquip.testListaEquipos()
        #self.__manejEquip.mostrarEquipos()

        self.__listaPartidos = []

    def getSwitcher (self):
        return self.__switcher

    def opcion (self, op):
        func = self.__switcher.get(op, lambda:print("\nOpcion no valida"))
        func()
    def salir (self):
        print("\nSalida del Programa")

    def opcion1 (self):
        os.system('clear')
        print("Se ejecuta la opcion 1 - Jugar Amistoso!\n")
        input("Deberá seleccionar los dos equipos a enfrentar: ")
        self.__manejEquip.mostrarNomEquipos()

        equipo_1 = input("\nIngrese el nombre del primer equipo: ")
        getEquipo_1 = self.__manejEquip.buscarEquipo(equipo_1)
        while getEquipo_1 == None:
                equipo_1 = input("\nIngrese nuevamente el nombre del primer equipo: ")
                getEquipo_1 = self.__manejEquip.buscarEquipo(equipo_1)      

        equipo_2 = input("\nIngrese el nombre del segundo equipo: ")
        getEquipo_2 = self.__manejEquip.buscarEquipo(equipo_2)
        while getEquipo_2 == None:
                equipo_2 = input("\nIngrese nuevamente el nombre del segundo equipo: ")
                getEquipo_2 = self.__manejEquip.buscarEquipo(equipo_2)

        #seleccionamos un arbitro a dirigir, como tambien un estadio a jugar
        os.system('clear')
        self.__manejArb.mostrarNombreArb()
        arbitro = input("\nIngrese el nombre de algun arbitro: ")
        getArbitro = self.__manejArb.buscarArbitro (arbitro)
        while getArbitro == None:
            arbitro = input("\nIngrese nuevamente el nombre de algun arbitro: ")
            getArbitro = self.__manejArb.buscarArbitro (arbitro)

        os.system('clear')
        self.__manejEst.nombresEstadios ()
        estadio = input("\nIngrese el nombre de algun estadio: ")
        getEstadio = self.__manejEst.buscarEstadio (estadio)
        while getEstadio == None:
            estadio = input("\nIngrese nuevamente,el nombre de algun estadio: ")
            getEstadio = self.__manejEst.buscarEstadio (estadio)

        #ahora podemos crear la instancia del partido
        os.system('clear')
        nombre_partido = input("\nIngrese el nombre del partido: ")
        instancia = 'Amistoso'
        partido = Partido (nombre_partido, instancia, getArbitro)
        #ahora agregamos el partido en la base de datos
        nuevo_partido = Partidos (
                nom = nombre_partido,
                inst = instancia
            )
        db.session.add (nuevo_partido)
        db.session.commit()



        partido.addEquipo (getEquipo_1)
        partido.addEquipo (getEquipo_2)

        cant_pol = int(input("\nIngrese la cantidad de policias presentes en el partido: \n"))
        cant_hab = int(input("\nIngrese la cantidad de espectadores presentes en el partido: \n"))
        getEstadio.addCapacidadEstadio (partido, cant_pol,cant_hab)

        cant_goles_A = 0
        cant_goles_B = 0
        for segundos in range(91):
            if segundos <= 45:
                tiempo = 'Primer Tiempo'
            else:
                tiempo = 'Segundo Tiempo'

            os.system('clear')
            print("Equipo 1                                        Equipo 2")
            print("[{}]                         [{}]\n".format(getEquipo_1.getNombreEq(),getEquipo_2.getNombreEq()))
            jugEquipo_1 = getEquipo_1.getJugadores()
            jugEquipo_2 = getEquipo_2.getJugadores()

            #la cantidad de jugadores en ambos equipos debe ser igual
            for i in range(len(jugEquipo_1)):
                nombreJug_eq1 = jugEquipo_1[i].getNombre() + ' '+jugEquipo_1[i].getApellido()
                nombreJug_eq2 = jugEquipo_2[i].getNombre() + ' '+jugEquipo_2[i].getApellido()
                print("{}                             {}".format(nombreJug_eq1, nombreJug_eq2))   #podria agregar otros atributos de cant goles de cada jugador

            #----------------------------------------------------------------------------
            eventoPartido = randint (1,44)       #1 golEquipo A, 2 golEquipoB, 3-43 Empate
            if eventoPartido == 1:
                cant_goles_A += 1
                longA = len(jugEquipo_1)  
                randomA = randint (2,longA)
                #no coloco randomA == 1, ya que no tiene sentido que un arquero haga gol
                if randomA == 2:
                    unGol = Gol (int(segundos),tiempo,partido, jugEquipo_1[1])
                    print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_1[1].getNombre() + ' '+jugEquipo_1[1].getApellido(),getEquipo_1.getNombreEq(),jugEquipo_1[1].getCantGolesJug()))
                elif randomA == 3:
                    unGol = Gol (int(segundos),tiempo,partido, jugEquipo_1[2])
                    print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_1[2].getNombre() + ' '+jugEquipo_1[2].getApellido(),getEquipo_1.getNombreEq(),jugEquipo_1[2].getCantGolesJug()))
                elif randomA == 4:
                    unGol = Gol (int(segundos),tiempo,partido, jugEquipo_1[3])
                    print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_1[3].getNombre() + ' '+jugEquipo_1[3].getApellido(),getEquipo_1.getNombreEq(),jugEquipo_1[3].getCantGolesJug()))
                elif randomA == 5:
                    unGol = Gol (int(segundos),tiempo,partido, jugEquipo_1[4])
                    print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_1[4].getNombre() + ' '+jugEquipo_1[4].getApellido(),getEquipo_1.getNombreEq(),jugEquipo_1[4].getCantGolesJug()))


            elif eventoPartido == 2:
                    cant_goles_B += 1
                    longB = (len(jugEquipo_2) + len(jugEquipo_1))               #si son 5 jug, 5+5= 10) para denotar el valor max
                    longA = (len(jugEquipo_1) + 1)                      #incrementamos 1 para anotar goles del sig equipo
                    randomB = randint (longA+1,longB)
                    #no coloco randomB == longA, ya que no tiene sentido que un arquero haga gol
                    if randomB == (longA+1):
                        unGol = Gol (int(segundos),tiempo,partido,jugEquipo_2[1])
                        print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_2[1].getNombre() + ' '+jugEquipo_2[1].getApellido(),getEquipo_2.getNombreEq(),jugEquipo_2[1].getCantGolesJug()))
                    elif randomB == (longA+2):
                        unGol = Gol (int(segundos),tiempo,partido,jugEquipo_2[2])
                        print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_2[2].getNombre() + ' '+jugEquipo_2[2].getApellido(),getEquipo_2.getNombreEq(),jugEquipo_2[2].getCantGolesJug()))
                    elif randomB == (longB-1):
                        unGol = Gol (int(segundos),tiempo,partido,jugEquipo_2[3])
                        print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_2[3].getNombre() + ' '+jugEquipo_2[3].getApellido(),getEquipo_2.getNombreEq(),jugEquipo_2[3].getCantGolesJug()))
                    elif randomB == longB:
                        unGol = Gol (int(segundos),tiempo,partido,jugEquipo_2[4])
                        print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_2[4].getNombre() + ' '+jugEquipo_2[4].getApellido(),getEquipo_2.getNombreEq(),jugEquipo_2[4].getCantGolesJug()))
            #----------------------------------------------------------------------------

            print("\n                       {}:{}  ".format(cant_goles_A, cant_goles_B))
            print("\n\n                     Minuto Partido: {} '".format(segundos))
            time.sleep(1)       #para pausar el tiempo cada seg
        

        if cant_goles_A > cant_goles_B:
            print("\nTRIUNFO DEL EQUIPO {}!! :D".format(getEquipo_1.getNombreEq()))
            getArbitro.guardarResultado (partido, cant_goles_A, cant_goles_B)
        
        elif cant_goles_B > cant_goles_A:
            print("\nTRIUNFO DEL EQUIPO {}!! xD".format(getEquipo_2.getNombreEq()))
            getArbitro.guardarResultado (partido, cant_goles_A, cant_goles_B)           
        else:
            os.system('clear')
            print("\nEMPATE ENTRE AMBOS EQUIPOS!! :S")
            print("\nVamos a tiempo extra: ")
            partido.tiempoExtra()
            for segundos in range(91,121):
                if segundos <= 105:
                    tiempo = 'Primer Tiempo Extra'
                else:
                    tiempo = 'Segundo Tiempo Extra'

                os.system('clear')
                print("Equipo 1                                        Equipo 2")
                print("[{}]                         [{}]\n".format(getEquipo_1.getNombreEq(),getEquipo_2.getNombreEq()))
                jugEquipo_1 = getEquipo_1.getJugadores()
                jugEquipo_2 = getEquipo_2.getJugadores()

                #la cantidad de jugadores en ambos equipos debe ser igual
                for i in range(len(jugEquipo_1)):
                    nombreJug_eq1 = jugEquipo_1[i].getNombre() + ' '+jugEquipo_1[i].getApellido()
                    nombreJug_eq2 = jugEquipo_2[i].getNombre() + ' '+jugEquipo_2[i].getApellido()
                    print("{}                             {}".format(nombreJug_eq1, nombreJug_eq2))   

                #----------------------------------------------------------------------------
                eventoPartido = randint (1,44)       #1 golEquipo A, 2 golEquipoB, 3-35 Empate
                if eventoPartido == 1:
                    cant_goles_A += 1
                    longA = len(jugEquipo_1)  
                    randomA = randint (2,longA)
                    #no coloco randomA == 1, ya que no tiene sentido que un arquero haga gol
                    if randomA == 2:
                        unGol = Gol (int(segundos),tiempo,partido, jugEquipo_1[1])
                        print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_1[1].getNombre() + ' '+jugEquipo_1[1].getApellido(),getEquipo_1.getNombreEq(),jugEquipo_1[1].getCantGolesJug()))
                    elif randomA == 3:
                        unGol = Gol (int(segundos),tiempo,partido, jugEquipo_1[2])
                        print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_1[2].getNombre() + ' '+jugEquipo_1[2].getApellido(),getEquipo_1.getNombreEq(),jugEquipo_1[2].getCantGolesJug()))
                    elif randomA == 4:
                        unGol = Gol (int(segundos),tiempo,partido, jugEquipo_1[3])
                        print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_1[3].getNombre() + ' '+jugEquipo_1[3].getApellido(),getEquipo_1.getNombreEq(),jugEquipo_1[3].getCantGolesJug()))
                    elif randomA == 5:
                        unGol = Gol (int(segundos),tiempo,partido, jugEquipo_1[4])
                        print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_1[4].getNombre() + ' '+jugEquipo_1[4].getApellido(),getEquipo_1.getNombreEq(),jugEquipo_1[4].getCantGolesJug()))


                elif eventoPartido == 2:
                    cant_goles_B += 1
                    longB = (len(jugEquipo_2) + len(jugEquipo_1))               #si son 5 jug, 5+5= 10) para denotar el valor max
                    longA = (len(jugEquipo_1) + 1)                      #incrementamos 1 para anotar goles del sig equipo
                    randomB = randint (longA+1,longB)
                    #no coloco randomB == longA, ya que no tiene sentido que un arquero haga gol
                    if randomB == (longA+1):
                        unGol = Gol (int(segundos),tiempo,partido,jugEquipo_2[1])
                        print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_2[1].getNombre() + ' '+jugEquipo_2[1].getApellido(),getEquipo_2.getNombreEq(),jugEquipo_2[1].getCantGolesJug()))
                    elif randomB == (longA+2):
                        unGol = Gol (int(segundos),tiempo,partido,jugEquipo_2[2])
                        print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_2[2].getNombre() + ' '+jugEquipo_2[2].getApellido(),getEquipo_2.getNombreEq(),jugEquipo_2[2].getCantGolesJug()))
                    elif randomB == (longB-1):
                        unGol = Gol (int(segundos),tiempo,partido,jugEquipo_2[3])
                        print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_2[3].getNombre() + ' '+jugEquipo_2[3].getApellido(),getEquipo_2.getNombreEq(),jugEquipo_2[3].getCantGolesJug()))
                    elif randomB == longB:
                        unGol = Gol (int(segundos),tiempo,partido,jugEquipo_2[4])
                        print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_2[4].getNombre() + ' '+jugEquipo_2[4].getApellido(),getEquipo_2.getNombreEq(),jugEquipo_2[4].getCantGolesJug()))
                #----------------------------------------------------------------------------

                print("\n                       {}:{}  ".format(cant_goles_A, cant_goles_B))
                print("\n\n                     Minuto Partido: {} '".format(segundos))
                time.sleep(1)

            if cant_goles_A > cant_goles_B:
                print("\nTRIUNFO DEL EQUIPO {} en tiempo Extra!! :D".format(getEquipo_1.getNombreEq()))
                getArbitro.guardarResultado (partido, cant_goles_A, cant_goles_B)
            elif cant_goles_B > cant_goles_A:
                print("\nTRIUNFO DEL EQUIPO {} en tiempo Extra!! xD".format(getEquipo_2.getNombreEq()))
                getArbitro.guardarResultado (partido, cant_goles_A, cant_goles_B)
            else:
                input("\nTermina en empate, hay penales!")
                evalPen = randint(1,2)
                if evalPen == 1:
                    resultPen = randint(1,4)
                    if resultPen == 1:
                        print("\nResultado de la Tanda de Penaltis: [O,O,O,O]  4-2  [O,X,O,X]")
                    elif resultPen == 2:
                        print("\nResultado de la Tanda de Penaltis: [O,O,O,O,O]   5-4  [O,O,O,X]")
                    elif resultPen == 3:
                        print("\nResultado de la Tanda de Penaltis:  [O,O,O,O,X,O,X,O]  6-5  [O,X,O,O,O,O,X,X]")
                    elif resultPen == 4:
                        print("\nResultado de la Tanda de Penaltis:  [O,X,O,O,O]  4-3 [O,O,X,O,X]")

                    input("\nGANADOR de la Tanda de PENALTIS: {}\n".format(getEquipo_1.getNombreEq()))
                    getArbitro.guardarResultado (partido, cant_goles_A, cant_goles_B)
                elif evalPen == 2:
                    resultPen = randint(1,4)
                    if resultPen == 1:
                        print("\nResultado de la Tanda de Penaltis: [O,X,O,X]  2-4  [O,O,O,O]")
                    elif resultPen == 2:
                        print("\nResultado de la Tanda de Penaltis: [O,O,O,X]  4-5  [O,O,O,O,O]")
                    elif resultPen == 3:
                        print("\nResultado de la Tanda de Penaltis: [O,X,O,O,O,O,X,X]  5-6  [O,O,O,O,X,O,X,O]")
                    elif resultPen == 4:
                        print("\nResultado de la Tanda de Penaltis: [O,O,X,O,X]  3-4  [O,X,O,O,O]")
                    input("\nGANADOR de la Tanda de PENALTIS: {}\n".format(getEquipo_2.getNombreEq()))
                    getArbitro.guardarResultado (partido, cant_goles_A, cant_goles_B)

        os.system('clear')
        input("El partido ha finalizado, mostramos sus detalles: ")
        getEstadio.mostrarEstadio()
        input("PRESIONE UNA TECLA,para continuar: ")
        partido.mostrarPartido()

        self.__listaPartidos.append(partido)

        #Finalizo el partido, guardo el resultado en la base de datos
        arbitroP = partido.getArbitroPartido()
        nuevo_rP = ResultPartido (
            arbitro = arbitroP.getNombre(),
            partido = nombre_partido,
            cantGolesEqA = partido.getGolesA(),
            cantGolesEqB = partido.getGolesB()
        )
        db.session.add (nuevo_rP)
        db.session.commit()


        input("\nPRESIONE UNA TECLA para finalizar la opcion 1: ")
        os.system('clear')

    def obtenerOtrosEq (self, grupo, otroEq, equipo):
        otros = []
        for equip in grupo:
            if equip.getNombreEq() != otroEq.getNombreEq() and equip.getNombreEq() != equipo.getNombreEq():
                if equip not in otros:
                    otros.append(equip)
        
        return otros

    def faseDeGrupo (self, equipo, grupo, arbitros, estadios):
        primero = None
        segundo = None
        
        if equipo != None:                  #pasaré None cuando el equipo no esté en dicho grupo
            for i in range(4):
                j = 1
                if grupo[i].getNombreEq() != equipo.getNombreEq():
                    cant_goles_A = 0
                    cant_goles_B = 0
                    
                    random_arb = randint (1,arbitros)
                    get_arbitro = self.__manejArb.obtenerUnArbitro (random_arb)
                    #print("Nro Random Arb: ", random_arb)
                    #print(get_arbitro)
                    input('Se juega '+ 'Fase de Grupos: '+equipo.getNombreEq() + ' vs '+grupo[i].getNombreEq()+'\n')
                    
                    nom = get_arbitro.getNombre() +' '+get_arbitro.getApellido()
                    print("\nNombre del Arbitro del partido: {}".format(nom))
                    
                    random_est = randint (1,estadios)
                    #print("Nro Random Est: ", random_est)
                    get_estadio = self.__manejEst.obtenerUnEstadio (random_est)
                    input("\nEstadio del partido: %s"%(get_estadio.getNombre()))

                    nom_partido = str('Fase de Grupos: '+equipo.getNombreEq() + ' vs '+grupo[i].getNombreEq())
                    instancia = 'Fase de Grupos'
                    partido = Partido (nom_partido,instancia,get_arbitro)

                    #ahora agregamos el partido en la base de datos
                    nuevo_partido = Partidos (
                        nom = nom_partido,
                        inst = instancia
                    )
                    db.session.add (nuevo_partido)
                    db.session.commit()

                    self.__listaPartidos.append(partido)

                    partido.addEquipo (equipo)
                    partido.addEquipo (grupo[i])

                    capacidad = get_estadio.getCapacMax()
                    cant_pol = randint (1000,capacidad-30000)
                    cant_hab = randint (22000,capacidad)
                    get_estadio.addCapacidadEstadio (partido, cant_pol,cant_hab)

                    jugEquipo_1 = equipo.getJugadores()
                    jugEquipo_2 = grupo[i].getJugadores()

                    for segundos in range(91):
                        if segundos <= 45:
                            tiempo = 'Primer Tiempo'
                        else:
                            tiempo = 'Segundo Tiempo'

                        os.system('clear')
                        print("Equipo 1                                        Equipo 2")
                        print("[{}]                         [{}]\n".format(equipo.getNombreEq(),grupo[i].getNombreEq()))

                        #la cantidad de jugadores en ambos equipos debe ser igual
                        for k in range(len(jugEquipo_1)):
                            nombreJug_eq1 = jugEquipo_1[k].getNombre() + ' '+jugEquipo_1[k].getApellido()
                            nombreJug_eq2 = jugEquipo_2[k].getNombre() + ' '+jugEquipo_2[k].getApellido()
                            print("{}                             {}".format(nombreJug_eq1, nombreJug_eq2))   #podria agregar otros atributos de cant goles de cada jugador

                        #----------------------------------------------------------------------------
                        eventoPartido = randint (1,44)       #1 golEquipo A, 2 golEquipoB, 3-43 Empate
                        if eventoPartido == 1:
                            cant_goles_A += 1
                            longA = len(jugEquipo_1)  
                            randomA = randint (2,longA)
                            #no coloco randomA == 1, ya que no tiene sentido que un arquero haga gol
                            if randomA == 2:
                                unGol = Gol (int(segundos),tiempo,partido, jugEquipo_1[1])
                                print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_1[1].getNombre() + ' '+jugEquipo_1[1].getApellido(),equipo.getNombreEq(),jugEquipo_1[1].getCantGolesJug()))
                            elif randomA == 3:
                                unGol = Gol (int(segundos),tiempo,partido, jugEquipo_1[2])
                                print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_1[2].getNombre() + ' '+jugEquipo_1[2].getApellido(),equipo.getNombreEq(),jugEquipo_1[2].getCantGolesJug()))
                            elif randomA == 4:
                                unGol = Gol (int(segundos),tiempo,partido, jugEquipo_1[3])
                                print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_1[3].getNombre() + ' '+jugEquipo_1[3].getApellido(),equipo.getNombreEq(),jugEquipo_1[3].getCantGolesJug()))
                            elif randomA == 5:
                                unGol = Gol (int(segundos),tiempo,partido, jugEquipo_1[4])
                                print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_1[4].getNombre() + ' '+jugEquipo_1[4].getApellido(),equipo.getNombreEq(),jugEquipo_1[4].getCantGolesJug()))


                        elif eventoPartido == 2:
                                cant_goles_B += 1
                                longB = (len(jugEquipo_2) + len(jugEquipo_1))               #si son 5 jug, 5+5= 10) para denotar el valor max
                                longA = (len(jugEquipo_1) + 1)                      #incrementamos 1 para anotar goles del sig equipo
                                randomB = randint (longA+1,longB)
                                #no coloco randomB == longA, ya que no tiene sentido que un arquero haga gol
                                if randomB == (longA+1):
                                    unGol = Gol (int(segundos),tiempo,partido,jugEquipo_2[1])
                                    print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_2[1].getNombre() + ' '+jugEquipo_2[1].getApellido(),grupo[i].getNombreEq(),jugEquipo_2[1].getCantGolesJug()))
                                elif randomB == (longA+2):
                                    unGol = Gol (int(segundos),tiempo,partido,jugEquipo_2[2])
                                    print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_2[2].getNombre() + ' '+jugEquipo_2[2].getApellido(),grupo[i].getNombreEq(),jugEquipo_2[2].getCantGolesJug()))
                                elif randomB == (longB-1):
                                    unGol = Gol (int(segundos),tiempo,partido,jugEquipo_2[3])
                                    print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_2[3].getNombre() + ' '+jugEquipo_2[3].getApellido(),grupo[i].getNombreEq(),jugEquipo_2[3].getCantGolesJug()))
                                elif randomB == longB:
                                    unGol = Gol (int(segundos),tiempo,partido,jugEquipo_2[4])
                                    print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_2[4].getNombre() + ' '+jugEquipo_2[4].getApellido(),grupo[i].getNombreEq(),jugEquipo_2[4].getCantGolesJug()))
                        #----------------------------------------------------------------------------

                        print("\n                       {}:{}  ".format(cant_goles_A, cant_goles_B))
                        print("\n\n                     Minuto Partido: {} '".format(segundos))
                        time.sleep(1)       #para pausar el tiempo cada seg
                    

                    if cant_goles_A > cant_goles_B:
                        print("\nTRIUNFO DEL EQUIPO {}!! :D".format(equipo.getNombreEq()))
                        equipo.acPuntos (3)
                        get_arbitro.guardarResultado (partido, cant_goles_A, cant_goles_B)
                        #Finalizo el partido, guardo el resultado en la base de datos
                        arbitroP = partido.getArbitroPartido()
                        nuevo_rP = ResultPartido (
                            arbitro = arbitroP.getNombre(),
                            partido = nom_partido,
                            cantGolesEqA = partido.getGolesA(),
                            cantGolesEqB = partido.getGolesB()
                        )
                        db.session.add (nuevo_rP)
                        db.session.commit()
                    
                    elif cant_goles_B > cant_goles_A:
                        print("\nTRIUNFO DEL EQUIPO {}!! xD".format(grupo[i].getNombreEq()))
                        grupo[i].acPuntos (3)
                        get_arbitro.guardarResultado (partido, cant_goles_A, cant_goles_B)   
                        #Finalizo el partido, guardo el resultado en la base de datos
                        arbitroP = partido.getArbitroPartido()
                        nuevo_rP = ResultPartido (
                            arbitro = arbitroP.getNombre(),
                            partido = nom_partido,
                            cantGolesEqA = partido.getGolesA(),
                            cantGolesEqB = partido.getGolesB()
                        )
                        db.session.add (nuevo_rP)
                        db.session.commit()        
                    else:
                        os.system('clear')
                        print("\nEMPATE ENTRE AMBOS EQUIPOS!! :S")
                        equipo.acPuntos (1)
                        grupo[i].acPuntos(1)
                        get_arbitro.guardarResultado (partido, cant_goles_A, cant_goles_B)
                        #Finalizo el partido, guardo el resultado en la base de datos
                        arbitroP = partido.getArbitroPartido()
                        nuevo_rP = ResultPartido (
                            arbitro = arbitroP.getNombre(),
                            partido = nom_partido,
                            cantGolesEqA = partido.getGolesA(),
                            cantGolesEqB = partido.getGolesB()
                        )
                        db.session.add (nuevo_rP)
                        db.session.commit()
                
                    #desde aqui debo obtener los otros dos equipos que no juegan, y hacer al azar quien gana y pierde
                    otros = self.obtenerOtrosEq (grupo,grupo[i], equipo)
                    random_sim = randint(1,3)
                    if random_sim == 1:
                        otros[0].acPuntos(3)
                        print("Fecha: {} - Victoria del Equipo: {}".format(j,otros[0].getNombreEq()))
                    elif random_sim == 2:
                        otros[1].acPuntos(3)
                        print("Fecha: {} - Victoria del Equipo: {}".format(j,otros[1].getNombreEq()))
                    elif random_sim == 3:
                        otros[0].acPuntos (1)
                        otros[1].acPuntos (1)
                        print("Fecha: {} - Empate entre ambos equipos".format(j))
                    
                    input("\nFinalizo la Fecha: {}".format(j))
                    os.system('clear')
                j += 1

            os.system('clear')
            grupo.sort(reverse = True)          #muestra descendentemente los equipos con mas puntaje
            print("\nTabla de posiciones\nEquipo| Games | Points") 
            for equip in grupo:
                print("[ {} | 3 | {} ]".format(equip.getNombreEq(),equip.getPuntos()))
            
            primero = grupo[0]
            segundo = grupo[1]

        else:
            random = randint(1,4)
            if random == 1:
                primero = grupo[0]
                random_2 = randint(1,3)
                if random_2 == 1:
                    segundo = grupo[1]
                elif random_2 == 2:
                    segundo = grupo[2]
                elif random_2 == 3:
                    segundo = grupo[3]
            elif random == 2:
                primero = grupo[1]
                random_2 = randint(1,3)
                if random_2 == 1:
                    segundo = grupo[0]
                elif random_2 == 2:
                    segundo = grupo[2]
                elif random_2 == 3:
                    segundo = grupo[3]
            elif random == 3:
                primero = grupo[2]
                random_2 = randint(1,3)
                if random_2 == 1:
                    segundo = grupo[0]
                elif random_2 == 2:
                    segundo = grupo[1]
                elif random_2 == 3:
                    segundo = grupo[3]
            elif random == 4:
                primero = grupo[3]
                random_2 = randint(1,3)
                if random_2 == 1:
                    segundo = grupo[0]
                elif random_2 == 2:
                    segundo = grupo[1]
                elif random_2 == 3:
                    segundo = grupo[2]

        return [primero, segundo]

    def eliminacionDirecta (self, equipo_1, equipo_2, bandera,arbitros, estadios, nombre_equipo):
        clasificado = None
        if bandera == True:
            cant_goles_A = 0
            cant_goles_B = 0
                    
            input('Se Juega: '+'Eliminacion Directa: '+equipo_1.getNombreEq() + ' vs '+equipo_2.getNombreEq() + '\n')
            
            random_arb = randint (1,arbitros)
            get_arbitro = self.__manejArb.obtenerUnArbitro (random_arb)
            nom = get_arbitro.getNombre() +' '+get_arbitro.getApellido()
            print("\nNombre del Arbitro del partido: {}\n".format(nom))
                    
            random_est = randint (1,estadios)
            get_estadio = self.__manejEst.obtenerUnEstadio (random_est)
            input("\nEstadio del partido: %s\n"%(get_estadio.getNombre()))

            nom_partido = str('Eliminacion Directa: '+equipo_1.getNombreEq() + ' vs '+equipo_2.getNombreEq())
            instancia = 'Eliminacion Directa'
            partido = Partido (nom_partido,instancia,get_arbitro)
            
            #ahora agregamos el partido en la base de datos
            nuevo_partido = Partidos (
                nom = nom_partido,
                inst = instancia
            )
            db.session.add (nuevo_partido)
            db.session.commit()

            self.__listaPartidos.append(partido)
            partido.addEquipo (equipo_1)
            partido.addEquipo (equipo_2)

            capacidad = get_estadio.getCapacMax()
            cant_pol = randint (1000,capacidad-30000)
            cant_hab = randint (22000,capacidad)
            get_estadio.addCapacidadEstadio (partido, cant_pol,cant_hab)

            jugEquipo_1 = equipo_1.getJugadores()
            jugEquipo_2 = equipo_2.getJugadores()

            for segundos in range(91):
                if segundos <= 45:
                    tiempo = 'Primer Tiempo'
                else:
                    tiempo = 'Segundo Tiempo'

                os.system('clear')
                print("Equipo 1                                        Equipo 2")
                print("[{}]                          [{}]\n".format(equipo_1.getNombreEq(),equipo_2.getNombreEq()))

                #la cantidad de jugadores en ambos equipos debe ser igual
                for k in range(len(jugEquipo_1)):
                    nombreJug_eq1 = jugEquipo_1[k].getNombre() + ' '+jugEquipo_1[k].getApellido()
                    nombreJug_eq2 = jugEquipo_2[k].getNombre() + ' '+jugEquipo_2[k].getApellido()
                    print("{}                             {}".format(nombreJug_eq1, nombreJug_eq2))   #podria agregar otros atributos de cant goles de cada jugador

                    #----------------------------------------------------------------------------
                eventoPartido = randint (1,44)       #1 golEquipo A, 2 golEquipoB, 3-43 Empate
                if eventoPartido == 1:
                        cant_goles_A += 1
                        longA = len(jugEquipo_1)  
                        randomA = randint (2,longA)
                        #no coloco randomA == 1, ya que no tiene sentido que un arquero haga gol
                        if randomA == 2:
                            unGol = Gol (int(segundos),tiempo,partido, jugEquipo_1[1])
                            print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_1[1].getNombre() + ' '+jugEquipo_1[1].getApellido(),equipo_1.getNombreEq(),jugEquipo_1[1].getCantGolesJug()))
                        elif randomA == 3:
                            unGol = Gol (int(segundos),tiempo,partido, jugEquipo_1[2])
                            print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_1[2].getNombre() + ' '+jugEquipo_1[2].getApellido(),equipo_1.getNombreEq(),jugEquipo_1[2].getCantGolesJug()))
                        elif randomA == 4:
                            unGol = Gol (int(segundos),tiempo,partido, jugEquipo_1[3])
                            print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_1[3].getNombre() + ' '+jugEquipo_1[3].getApellido(),equipo_1.getNombreEq(),jugEquipo_1[3].getCantGolesJug()))
                        elif randomA == 5:
                            unGol = Gol (int(segundos),tiempo,partido, jugEquipo_1[4])
                            print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_1[4].getNombre() + ' '+jugEquipo_1[4].getApellido(),equipo_1.getNombreEq(),jugEquipo_1[4].getCantGolesJug()))


                elif eventoPartido == 2:
                                cant_goles_B += 1
                                longB = (len(jugEquipo_2) + len(jugEquipo_1))               #si son 5 jug, 5+5= 10) para denotar el valor max
                                longA = (len(jugEquipo_1) + 1)                      #incrementamos 1 para anotar goles del sig equipo
                                randomB = randint (longA+1,longB)
                                #no coloco randomB == longA, ya que no tiene sentido que un arquero haga gol
                                if randomB == (longA+1):
                                    unGol = Gol (int(segundos),tiempo,partido,jugEquipo_2[1])
                                    print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_2[1].getNombre() + ' '+jugEquipo_2[1].getApellido(),equipo_2.getNombreEq(),jugEquipo_2[1].getCantGolesJug()))
                                elif randomB == (longA+2):
                                    unGol = Gol (int(segundos),tiempo,partido,jugEquipo_2[2])
                                    print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_2[2].getNombre() + ' '+jugEquipo_2[2].getApellido(),equipo_2.getNombreEq(),jugEquipo_2[2].getCantGolesJug()))
                                elif randomB == (longB-1):
                                    unGol = Gol (int(segundos),tiempo,partido,jugEquipo_2[3])
                                    print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_2[3].getNombre() + ' '+jugEquipo_2[3].getApellido(),equipo_2.getNombreEq(),jugEquipo_2[3].getCantGolesJug()))
                                elif randomB == longB:
                                    unGol = Gol (int(segundos),tiempo,partido,jugEquipo_2[4])
                                    print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_2[4].getNombre() + ' '+jugEquipo_2[4].getApellido(),equipo_2.getNombreEq(),jugEquipo_2[4].getCantGolesJug()))
                        #----------------------------------------------------------------------------

                print("\n                       {}:{}  ".format(cant_goles_A, cant_goles_B))
                print("\n\n                     Minuto Partido: {} '".format(segundos))
                time.sleep(1)       #para pausar el tiempo cada seg
                    

            if cant_goles_A > cant_goles_B:
                    print("\nTRIUNFO DEL EQUIPO {}!! :D".format(equipo_1.getNombreEq()))
                    clasificado = equipo_1
                    if nombre_equipo != None:
                        if nombre_equipo.lower() == equipo_2.getNombreEq():
                            print("\nNUESTRO equipo {} ha sido eliminado!\n".format(nombre_equipo))
                    
                    get_arbitro.guardarResultado (partido, cant_goles_A, cant_goles_B)
                    
            elif cant_goles_B > cant_goles_A:
                    print("\nTRIUNFO DEL EQUIPO {}!! xD".format(equipo_2.getNombreEq()))
                    clasificado = equipo_2
                    if nombre_equipo != None:
                        if nombre_equipo.lower() == equipo_1.getNombreEq():
                            print("\nNUESTRO equipo {} ha sido eliminado!\n".format(nombre_equipo))

                    get_arbitro.guardarResultado (partido, cant_goles_A, cant_goles_B)           
            else:
                    os.system('clear')
                    print("\nEMPATE ENTRE AMBOS EQUIPOS - SE RESUELVE POR TIEMPO EXTRA!! :S")
                    partido.tiempoExtra()
                    for segundos in range(91,121):
                        if segundos <= 105:
                            tiempo = 'Primer Tiempo Extra'
                        else:
                            tiempo = 'Segundo Tiempo Extra'

                        os.system('clear')
                        print("Equipo 1                                        Equipo 2")
                        print("[{}]                          [{}]\n".format(equipo_1.getNombreEq(),equipo_2.getNombreEq()))

                        jugEquipo_1 = equipo_1.getJugadores()
                        jugEquipo_2 = equipo_2.getJugadores()

                        #la cantidad de jugadores en ambos equipos debe ser igual
                        for i in range(len(jugEquipo_1)):
                            nombreJug_eq1 = jugEquipo_1[i].getNombre() + ' '+jugEquipo_1[i].getApellido()
                            nombreJug_eq2 = jugEquipo_2[i].getNombre() + ' '+jugEquipo_2[i].getApellido()
                            print("{}                             {}".format(nombreJug_eq1, nombreJug_eq2))   

                        #----------------------------------------------------------------------------
                        eventoPartido = randint (1,44)       #1 golEquipo A, 2 golEquipoB, 3-35 Empate
                        if eventoPartido == 1:
                            cant_goles_A += 1
                            longA = len(jugEquipo_1)  
                            randomA = randint (2,longA)
                            #no coloco randomA == 1, ya que no tiene sentido que un arquero haga gol
                            if randomA == 2:
                                unGol = Gol (int(segundos),tiempo,partido, jugEquipo_1[1])
                                print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_1[1].getNombre() + ' '+jugEquipo_1[1].getApellido(),equipo_1.getNombreEq(),jugEquipo_1[1].getCantGolesJug()))
                            elif randomA == 3:
                                unGol = Gol (int(segundos),tiempo,partido, jugEquipo_1[2])
                                print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_1[2].getNombre() + ' '+jugEquipo_1[2].getApellido(),equipo_1.getNombreEq(),jugEquipo_1[2].getCantGolesJug()))
                            elif randomA == 4:
                                unGol = Gol (int(segundos),tiempo,partido, jugEquipo_1[3])
                                print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_1[3].getNombre() + ' '+jugEquipo_1[3].getApellido(),equipo_1.getNombreEq(),jugEquipo_1[3].getCantGolesJug()))
                            elif randomA == 5:
                                unGol = Gol (int(segundos),tiempo,partido, jugEquipo_1[4])
                                print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_1[4].getNombre() + ' '+jugEquipo_1[4].getApellido(),equipo_1.getNombreEq(),jugEquipo_1[4].getCantGolesJug()))


                        elif eventoPartido == 2:
                            cant_goles_B += 1
                            longB = (len(jugEquipo_2) + len(jugEquipo_1))               #si son 5 jug, 5+5= 10) para denotar el valor max
                            longA = (len(jugEquipo_1) + 1)                      #incrementamos 1 para anotar goles del sig equipo
                            randomB = randint (longA+1,longB)
                            #no coloco randomB == longA, ya que no tiene sentido que un arquero haga gol
                            if randomB == (longA+1):
                                unGol = Gol (int(segundos),tiempo,partido,jugEquipo_2[1])
                                print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_2[1].getNombre() + ' '+jugEquipo_2[1].getApellido(),equipo_2.getNombreEq(),jugEquipo_2[1].getCantGolesJug()))
                            elif randomB == (longA+2):
                                unGol = Gol (int(segundos),tiempo,partido,jugEquipo_2[2])
                                print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_2[2].getNombre() + ' '+jugEquipo_2[2].getApellido(),equipo_2.getNombreEq(),jugEquipo_2[2].getCantGolesJug()))
                            elif randomB == (longB-1):
                                unGol = Gol (int(segundos),tiempo,partido,jugEquipo_2[3])
                                print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_2[3].getNombre() + ' '+jugEquipo_2[3].getApellido(),equipo_2.getNombreEq(),jugEquipo_2[3].getCantGolesJug()))
                            elif randomB == longB:
                                unGol = Gol (int(segundos),tiempo,partido,jugEquipo_2[4])
                                print("\nGol del Jugador: {}, Equipo {}, Goles: {}".format(jugEquipo_2[4].getNombre() + ' '+jugEquipo_2[4].getApellido(),equipo_2.getNombreEq(),jugEquipo_2[4].getCantGolesJug()))
                        #----------------------------------------------------------------------------

                        print("\n                       {}:{}  ".format(cant_goles_A, cant_goles_B))
                        print("\n\n                     Minuto Partido: {} '".format(segundos))
                        time.sleep(1)

                    if cant_goles_A > cant_goles_B:
                        print("\nTRIUNFO DEL EQUIPO {} en tiempo Extra!! :D".format(equipo_1.getNombreEq()))
                        clasificado = equipo_1
                        if nombre_equipo != None:
                            if nombre_equipo.lower() == equipo_2.getNombreEq():
                                print("\nNUESTRO equipo {} ha sido eliminado!\n".format(nombre_equipo))

                        get_arbitro.guardarResultado (partido, cant_goles_A, cant_goles_B)
                    elif cant_goles_B > cant_goles_A:
                        print("\nTRIUNFO DEL EQUIPO {} en tiempo Extra!! xD".format(equipo_2.getNombreEq()))
                        clasificado = equipo_2
                        if nombre_equipo != None:
                            if nombre_equipo.lower() == equipo_1.getNombreEq():
                                print("\nNUESTRO equipo {} ha sido eliminado!\n".format(nombre_equipo))                   

                        get_arbitro.guardarResultado (partido, cant_goles_A, cant_goles_B)
                    else:
                        input("\nTermina en empate, hay penales!")
                        evalPen = randint(1,2)
                        if evalPen == 1:
                            resultPen = randint(1,4)
                            if resultPen == 1:
                                print("\nResultado de la Tanda de Penaltis: [O,O,O,O]  4-2  [O,X,O,X]")
                            elif resultPen == 2:
                                print("\nResultado de la Tanda de Penaltis: [O,O,O,O,O]   5-4  [O,O,O,X]")
                            elif resultPen == 3:
                                print("\nResultado de la Tanda de Penaltis:  [O,O,O,O,X,O,X,O]  6-5  [O,X,O,O,O,O,X,X]")
                            elif resultPen == 4:
                                print("\nResultado de la Tanda de Penaltis:  [O,X,O,O,O]  4-3 [O,O,X,O,X]")

                            input("\nGANADOR de la Tanda de PENALTIS: {}\n".format(equipo_1.getNombreEq()))
                            clasificado = equipo_1
                            if nombre_equipo != None:
                                if nombre_equipo.lower() == equipo_2.getNombreEq():
                                    print("\nNUESTRO equipo {} ha sido eliminado!\n".format(nombre_equipo))

                            get_arbitro.guardarResultado (partido, cant_goles_A, cant_goles_B)
                        elif evalPen == 2:
                            resultPen = randint(1,4)
                            if resultPen == 1:
                                print("\nResultado de la Tanda de Penaltis: [O,X,O,X]  2-4  [O,O,O,O]")
                            elif resultPen == 2:
                                print("\nResultado de la Tanda de Penaltis: [O,O,O,X]  4-5  [O,O,O,O,O]")
                            elif resultPen == 3:
                                print("\nResultado de la Tanda de Penaltis: [O,X,O,O,O,O,X,X]  5-6  [O,O,O,O,X,O,X,O]")
                            elif resultPen == 4:
                                print("\nResultado de la Tanda de Penaltis: [O,O,X,O,X]  3-4  [O,X,O,O,O]")
                            input("\nGANADOR de la Tanda de PENALTIS: {}\n".format(equipo_2.getNombreEq()))
                            clasificado = equipo_2
                            if nombre_equipo != None:
                                if nombre_equipo.lower() == equipo_1.getNombreEq():
                                    print("\nNUESTRO equipo {} ha sido eliminado!\n".format(nombre_equipo))
                            
                            get_arbitro.guardarResultado (partido, cant_goles_A, cant_goles_B)                                

            arbitroP = partido.getArbitroPartido()
            nuevo_rP = ResultPartido (
                arbitro = arbitroP.getNombre(),
                partido = nom_partido,
                cantGolesEqA = partido.getGolesA(),
                cantGolesEqB = partido.getGolesB()
            )
            db.session.add (nuevo_rP)
            db.session.commit()

        else:
            random_pasa = randint(1,2)
            if random_pasa == 1:
                cant_goles_A = 0
                cant_goles_B = 0
                                        
                random_arb = randint (1,arbitros)
                get_arbitro = self.__manejArb.obtenerUnArbitro (random_arb)
                nom = get_arbitro.getNombre() +' '+get_arbitro.getApellido()
                        
                random_est = randint (1,estadios)
                get_estadio = self.__manejEst.obtenerUnEstadio (random_est)

                nom_partido = str('Eliminacion Directa: '+equipo_1.getNombreEq() + ' vs '+equipo_2.getNombreEq())
                instancia = 'Eliminacion Directa'
                partido = Partido (nom_partido,instancia,get_arbitro)
                
                #ahora agregamos el partido en la base de datos
                nuevo_partido = Partidos (
                    nom = nom_partido,
                    inst = instancia
                )
                db.session.add (nuevo_partido)
                db.session.commit()
                
                self.__listaPartidos.append(partido)
                partido.addEquipo (equipo_1)
                partido.addEquipo (equipo_2)

                capacidad = get_estadio.getCapacMax()
                cant_pol = randint (1000,capacidad-30000)
                cant_hab = randint (22000,capacidad)
                get_estadio.addCapacidadEstadio (partido, cant_pol,cant_hab)
                
                get_jugadores = equipo_1.getJugadores()
                random_goles = randint(3,5)
                if random_goles == 3:
                    for i in range (random_goles):
                        random_seg = randint(1,120)
                        random_jug = randint (1,4)
                        if random_jug == 1:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[1])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[1])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[1])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[1])
                        elif random_jug == 2:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[2])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[2])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[2])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[2])
                        elif random_jug == 3:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[3])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[3])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[3])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[3])
                        elif random_jug == 4:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[4])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[4])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[4])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[4])

                elif random_goles == 4:
                    for i in range (random_goles):
                        random_seg = randint(1,120)
                        random_jug = randint (1,4)
                        if random_jug == 1:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[1])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[1])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[1])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[1])
                        elif random_jug == 2:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[2])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[2])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[2])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[2])
                        elif random_jug == 3:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[3])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[3])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[3])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[3])
                        elif random_jug == 4:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[4])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[4])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[4])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[4])
                elif random_goles == 5:
                    for i in range (random_goles):
                        random_seg = randint(1,120)
                        random_jug = randint (1,4)
                        if random_jug == 1:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[1])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[1])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[1])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[1])
                        elif random_jug == 2:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[2])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[2])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[2])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[2])
                        elif random_jug == 3:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[3])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[3])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[3])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[3])
                        elif random_jug == 4:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[4])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[4])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[4])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[4])
                
                cant_goles_A = random_goles

                get_jugadores2 = equipo_2.getJugadores()            #goles por defecto del equipo que pierde
                random_goles2 = randint (1,3)
                if random_goles2 == 1:
                        #NO HACE FALTA UN FOR, PUES ES UN SOLO GOL
                        random_seg = randint(1,120)
                        random_jug = randint (1,4)
                        if random_jug == 1:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[1])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[1])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[1])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[1])
                        elif random_jug == 2:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[2])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[2])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[2])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[2])
                        elif random_jug == 3:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[3])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[3])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[3])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[3])
                        elif random_jug == 4:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[4])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[4])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[4])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[4])
                elif random_goles2 == 2:
                    for i in range (random_goles2):
                        random_seg = randint(1,120)
                        random_jug = randint (1,4)
                        if random_jug == 1:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[1])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[1])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[1])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[1])
                        elif random_jug == 2:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[2])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[2])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[2])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[2])
                        elif random_jug == 3:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[3])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[3])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[3])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[3])
                        elif random_jug == 4:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[4])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[4])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[4])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[4])
                elif random_goles2 == 3:
                    for i in range (random_goles2):
                        random_seg = randint(1,120)
                        random_jug = randint (1,4)
                        if random_jug == 1:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[1])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[1])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[1])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[1])
                        elif random_jug == 2:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[2])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[2])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[2])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[2])
                        elif random_jug == 3:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[3])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[3])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[3])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[3])
                        elif random_jug == 4:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[4])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[4])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[4])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[4])

                cant_goles_B = random_goles2
                get_arbitro.guardarResultado (partido, cant_goles_A, cant_goles_B)

                arbitroP = partido.getArbitroPartido()
                nuevo_rP = ResultPartido (
                    arbitro = arbitroP.getNombre(),
                    partido = nom_partido,
                    cantGolesEqA = partido.getGolesA(),
                    cantGolesEqB = partido.getGolesB()
                )
                db.session.add (nuevo_rP)
                db.session.commit()

                clasificado = equipo_1

            elif random_pasa == 2:
                cant_goles_A = 0
                cant_goles_B = 0
                                        
                random_arb = randint (1,arbitros)
                get_arbitro = self.__manejArb.obtenerUnArbitro (random_arb)
                nom = get_arbitro.getNombre() +' '+get_arbitro.getApellido()
                        
                random_est = randint (1,estadios)
                get_estadio = self.__manejEst.obtenerUnEstadio (random_est)

                nom_partido = str('Eliminacion Directa: '+equipo_1.getNombreEq() + ' vs '+equipo_2.getNombreEq())
                instancia = 'Eliminacion Directa'
                partido = Partido (nom_partido,instancia,get_arbitro)
                
                #ahora agregamos el partido en la base de datos
                nuevo_partido = Partidos (
                    nom = nom_partido,
                    inst = instancia
                )
                db.session.add (nuevo_partido)
                db.session.commit()
                        
                self.__listaPartidos.append(partido)
                partido.addEquipo (equipo_1)
                partido.addEquipo (equipo_2)

                capacidad = get_estadio.getCapacMax()
                cant_pol = randint (1000,capacidad-30000)
                cant_hab = randint (22000,capacidad)
                get_estadio.addCapacidadEstadio (partido, cant_pol,cant_hab)
                
                get_jugadores = equipo_2.getJugadores()
                random_goles = randint(3,5)
                if random_goles == 3:
                    for i in range (random_goles):
                        random_seg = randint(1,120)
                        random_jug = randint (1,4)
                        if random_jug == 1:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[1])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[1])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[1])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[1])
                        elif random_jug == 2:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[2])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[2])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[2])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[2])
                        elif random_jug == 3:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[3])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[3])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[3])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[3])
                        elif random_jug == 4:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[4])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[4])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[4])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[4])

                elif random_goles == 4:
                    for i in range (random_goles):
                        random_seg = randint(1,120)
                        random_jug = randint (1,4)
                        if random_jug == 1:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[1])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[1])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[1])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[1])
                        elif random_jug == 2:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[2])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[2])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[2])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[2])
                        elif random_jug == 3:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[3])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[3])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[3])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[3])
                        elif random_jug == 4:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[4])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[4])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[4])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[4])
                elif random_goles == 5:
                    for i in range (random_goles):
                        random_seg = randint(1,120)
                        random_jug = randint (1,4)
                        if random_jug == 1:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[1])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[1])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[1])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[1])
                        elif random_jug == 2:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[2])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[2])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[2])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[2])
                        elif random_jug == 3:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[3])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[3])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[3])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[3])
                        elif random_jug == 4:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores[4])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores[4])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores[4])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores[4])
                
                cant_goles_B = random_goles

                get_jugadores2 = equipo_1.getJugadores()        #goles por defecto del equipo que pierde
                random_goles2 = randint (1,3)
                if random_goles2 == 1:
                        #NO HACE FALTA UN FOR, PUES ES UN SOLO GOL
                        random_seg = randint(1,120)
                        random_jug = randint (1,4)
                        if random_jug == 1:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[1])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[1])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[1])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[1])
                        elif random_jug == 2:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[2])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[2])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[2])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[2])
                        elif random_jug == 3:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[3])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[3])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[3])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[3])
                        elif random_jug == 4:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[4])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[4])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[4])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[4])
                elif random_goles2 == 2:
                    for i in range (random_goles2):
                        random_seg = randint(1,120)
                        random_jug = randint (1,4)
                        if random_jug == 1:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[1])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[1])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[1])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[1])
                        elif random_jug == 2:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[2])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[2])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[2])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[2])
                        elif random_jug == 3:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[3])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[3])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[3])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[3])
                        elif random_jug == 4:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[4])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[4])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[4])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[4])
                elif random_goles2 == 3:
                    for i in range (random_goles2):
                        random_seg = randint(1,120)
                        random_jug = randint (1,4)
                        if random_jug == 1:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[1])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[1])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[1])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[1])
                        elif random_jug == 2:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[2])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[2])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[2])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[2])
                        elif random_jug == 3:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[3])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[3])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[3])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[3])
                        elif random_jug == 4:
                            if random_seg <= 45:
                                unGol = Gol (random_seg,'Primer Tiempo', partido, get_jugadores2[4])
                            elif random_seg <= 90:
                                unGol = Gol (random_seg,'Segundo Tiempo', partido, get_jugadores2[4])
                            elif random_seg <= 105:
                                unGol = Gol (random_seg,'Primer Tiempo Extra', partido, get_jugadores2[4])
                            elif random_seg <= 120:
                                unGol = Gol (random_seg,'Segundo Tiempo Extra', partido, get_jugadores2[4])

                cant_goles_A = random_goles2
                get_arbitro.guardarResultado (partido, cant_goles_A, cant_goles_B)

                arbitroP = partido.getArbitroPartido()
                nuevo_rP = ResultPartido (
                    arbitro = arbitroP.getNombre(),
                    partido = nom_partido,
                    cantGolesEqA = partido.getGolesA(),
                    cantGolesEqB = partido.getGolesB()
                )
                db.session.add (nuevo_rP)
                db.session.commit()

                clasificado = equipo_2

        return clasificado


    def opcion2 (self):
        print("\nSe ejecuta la opcion 2 - Jugamos copa con 8 Equipos\n")
        lista_Equipos = []
        totalEq = len(self.__manejEquip.getListaEquipos())
        while len(lista_Equipos) < 16:
            nroEq = randint (1,totalEq)
            get_equipo = self.__manejEquip.obtenerEquipo (nroEq)
            if get_equipo not in lista_Equipos:         #para que no se repitan los equipos
                lista_Equipos.append(get_equipo)
        
        input("\nYa estan seleccionados los equipos participantes!-> ")
        for equip in lista_Equipos:
            print("-->[%s]"%(equip.getNombreEq()))

        group_1 = []
        group_2 = []
        group_3 = []
        group_4 = []

        for i in range(4):
            group_1.append(lista_Equipos[i])
            group_2.append(lista_Equipos[i+4])      #grupo3.append(lista[i+8])   grupo4.append(lista[i+12])
            group_3.append(lista_Equipos[i+8])
            group_4.append(lista_Equipos[i+12])

        print("\n------Grupo 1------")
        for equip in group_1:
            print("-->[%s]"%(equip.getNombreEq()))
        print("\n------Grupo 2------")
        for equip in group_2:
            print("-->[%s]"%(equip.getNombreEq()))
        print("\n------Grupo 3------")
        for equip in group_3:
            print("-->[%s]"%(equip.getNombreEq()))
        print("\n------Grupo 4------")
        for equip in group_4:
            print("-->[%s]"%(equip.getNombreEq()))


        equipo = input("\nIngrese el equipo a jugar: ")
        get_equipo = self.__manejEquip.buscarEquipo(equipo)
        while get_equipo == None:
            equipo = input("\nIngrese de nuevo,el equipo a jugar: ")
            get_equipo = self.__manejEquip.buscarEquipo(equipo)

        total_arb = self.__manejArb.getListaArb()
        total_est = self.__manejEst.getListaEstadios ()

        #retorna el 1ero y 2do clasificado
        if get_equipo not in group_2:
            if get_equipo not in group_1:
                if get_equipo not in group_3:
                    [equip1, equip2] = self.faseDeGrupo (None, group_1,total_arb, total_est)
                    [equip3, equip4] = self.faseDeGrupo (None, group_2,total_arb, total_est)
                    [equip5, equip6] = self.faseDeGrupo (None, group_3,total_arb, total_est)   
                    [equip7, equip8] = self.faseDeGrupo (get_equipo, group_4,total_arb, total_est)
                else:
                    [equip1, equip2] = self.faseDeGrupo (None, group_1,total_arb, total_est)
                    [equip3, equip4] = self.faseDeGrupo (None, group_2,total_arb, total_est)
                    [equip5, equip6] = self.faseDeGrupo (get_equipo, group_3,total_arb, total_est)   
                    [equip7, equip8] = self.faseDeGrupo (None, group_4,total_arb, total_est)
            else:
                [equip1, equip2] = self.faseDeGrupo (get_equipo, group_1,total_arb, total_est)
                [equip3, equip4] = self.faseDeGrupo (None, group_2,total_arb, total_est)
                [equip5, equip6] = self.faseDeGrupo (None, group_3,total_arb, total_est)   
                [equip7, equip8] = self.faseDeGrupo (None, group_4,total_arb, total_est)  
        else:
            [equip1, equip2] = self.faseDeGrupo (None, group_1,total_arb, total_est)
            [equip3, equip4] = self.faseDeGrupo (get_equipo, group_2,total_arb, total_est)
            [equip5, equip6] = self.faseDeGrupo (None, group_3,total_arb, total_est)   
            [equip7, equip8] = self.faseDeGrupo (None, group_4,total_arb, total_est)

        input("\nCUARTOS DE FINAL\n     {} vs {}\n    {} vs {}\n    {} vs {}\n   {} vs {}".format(equip1.getNombreEq(),equip4.getNombreEq(), equip3.getNombreEq(), equip2.getNombreEq(), equip5.getNombreEq(), equip8.getNombreEq(), equip7.getNombreEq(), equip6.getNombreEq()))
        if get_equipo.getNombreEq() == equip1.getNombreEq():
            equip1 = self.eliminacionDirecta (equip1, equip4,True,total_arb, total_est,get_equipo.getNombreEq())
            equip2 = self.eliminacionDirecta (equip3, equip2, False,total_arb, total_est,None)
            equip3 = self.eliminacionDirecta (equip5, equip8, False,total_arb, total_est,None)
            equip4 = self.eliminacionDirecta (equip7, equip6, False,total_arb, total_est,None) 
        elif get_equipo.getNombreEq() == equip2.getNombreEq():
            equip1 = self.eliminacionDirecta (equip1, equip4,False,total_arb, total_est,None)
            equip2 = self.eliminacionDirecta (equip3, equip2, True,total_arb, total_est,get_equipo.getNombreEq())
            equip3 = self.eliminacionDirecta (equip5, equip8, False,total_arb, total_est,None)
            equip4 = self.eliminacionDirecta (equip7, equip6, False,total_arb, total_est,None)
        elif get_equipo.getNombreEq() == equip3.getNombreEq():
            equip1 = self.eliminacionDirecta (equip1, equip4,False,total_arb, total_est,None)
            equip2 = self.eliminacionDirecta (equip3, equip2, True,total_arb, total_est,get_equipo.getNombreEq())
            equip3 = self.eliminacionDirecta (equip5, equip8, False,total_arb, total_est,None)
            equip4 = self.eliminacionDirecta (equip7, equip6, False,total_arb, total_est,None)
        elif get_equipo.getNombreEq() == equip4.getNombreEq():
            equip1 = self.eliminacionDirecta (equip1, equip4,True,total_arb, total_est,get_equipo.getNombreEq())
            equip2 = self.eliminacionDirecta (equip3, equip2, False,total_arb, total_est,None)
            equip3 = self.eliminacionDirecta (equip5, equip8, False,total_arb, total_est,None)
            equip4 = self.eliminacionDirecta (equip7, equip6, False,total_arb, total_est,None)
        elif get_equipo.getNombreEq() == equip5.getNombreEq():
            equip1 = self.eliminacionDirecta (equip1, equip4,False,total_arb, total_est,None)
            equip2 = self.eliminacionDirecta (equip3, equip2, False,total_arb, total_est,None)
            equip3 = self.eliminacionDirecta (equip5, equip8, True,total_arb, total_est,get_equipo.getNombreEq())
            equip4 = self.eliminacionDirecta (equip7, equip6, False,total_arb, total_est,None)
        elif get_equipo.getNombreEq() == equip6.getNombreEq():
            equip1 = self.eliminacionDirecta (equip1, equip4,False,total_arb, total_est,None)
            equip2 = self.eliminacionDirecta (equip3, equip2, False,total_arb, total_est,None)
            equip3 = self.eliminacionDirecta (equip5, equip8, False,total_arb, total_est,None)
            equip4 = self.eliminacionDirecta (equip7, equip6, True,total_arb, total_est,get_equipo.getNombreEq())
        elif get_equipo.getNombreEq() == equip7.getNombreEq():
            equip1 = self.eliminacionDirecta (equip1, equip4,False,total_arb, total_est,None)
            equip2 = self.eliminacionDirecta (equip3, equip2, False,total_arb, total_est,None)
            equip3 = self.eliminacionDirecta (equip5, equip8, False,total_arb, total_est,None)
            equip4 = self.eliminacionDirecta (equip7, equip6, True,total_arb, total_est,get_equipo.getNombreEq())
        elif get_equipo.getNombreEq() == equip8.getNombreEq():
            equip1 = self.eliminacionDirecta (equip1, equip4,False,total_arb, total_est,None)
            equip2 = self.eliminacionDirecta (equip3, equip2, False,total_arb, total_est,None)
            equip3 = self.eliminacionDirecta (equip5, equip8, True,total_arb, total_est,get_equipo.getNombreEq())
            equip4 = self.eliminacionDirecta (equip7, equip6, False,total_arb, total_est,None)
        else:
            input("\nNuestro equipo seleccionado %s no clasificó a los Cuartos de final\n"%(get_equipo.getNombreEq()))
            equip1 = self.eliminacionDirecta (equip1, equip4,False,total_arb, total_est,None)
            equip2 = self.eliminacionDirecta (equip3, equip2, False,total_arb, total_est,None)
            equip3 = self.eliminacionDirecta (equip5, equip8, False,total_arb, total_est,None)
            equip4 = self.eliminacionDirecta (equip7, equip6, False,total_arb, total_est,None)


        input("\nSEMIFINALES\n      {} vs {}\n      {} vs {}".format(equip1.getNombreEq(),equip4.getNombreEq(), equip2.getNombreEq(), equip3.getNombreEq()))
        
        #averiguamos si nuestro equipo es alguno de los semifinalistas
        if get_equipo.getNombreEq() == equip1.getNombreEq():
            finalista_1 = self.eliminacionDirecta (equip1, equip4,True,total_arb, total_est,get_equipo.getNombreEq())
            finalista_2 = self.eliminacionDirecta (equip2, equip3, False,total_arb, total_est,None)
        elif get_equipo.getNombreEq() == equip2.getNombreEq():
            finalista_1 = self.eliminacionDirecta (equip1, equip4,False,total_arb, total_est,None)
            finalista_2 = self.eliminacionDirecta (equip2, equip3, True,total_arb, total_est,get_equipo.getNombreEq())
        elif get_equipo.getNombreEq() == equip3.getNombreEq():
            finalista_1 = self.eliminacionDirecta (equip1, equip4,False,total_arb, total_est,None)
            finalista_2 = self.eliminacionDirecta (equip2, equip3, True,total_arb, total_est,get_equipo.getNombreEq())
        elif get_equipo.getNombreEq() == equip4.getNombreEq():
            finalista_1 = self.eliminacionDirecta (equip1, equip4,True,total_arb, total_est,get_equipo.getNombreEq())
            finalista_2 = self.eliminacionDirecta (equip2, equip3, False,total_arb, total_est,None)
        else:
            #simulo las semifinales y solo obtengo los finalistas
            input("\nNuestro equipo seleccionado %s no clasificó a las Semifinales\n"%(get_equipo.getNombreEq()))
            finalista_1 = self.eliminacionDirecta (equip1, equip4,False,total_arb, total_est,None)
            finalista_2 = self.eliminacionDirecta (equip2, equip3, False,total_arb, total_est,None)


        input("\nFinal de la Copa: {} vs {}\n".format(finalista_1.getNombreEq(), finalista_2.getNombreEq()))
        
        if get_equipo.getNombreEq() == finalista_1.getNombreEq():
            campeon = self.eliminacionDirecta (finalista_1,finalista_2,True,total_arb, total_est,get_equipo.getNombreEq())
        elif get_equipo.getNombreEq() == finalista_2.getNombreEq():
            campeon = self.eliminacionDirecta (finalista_1,finalista_2,True,total_arb, total_est,get_equipo.getNombreEq())
        else:
            input("\nNuestro equipo seleccionado %s no clasificó a la final :(\n"%(get_equipo.getNombreEq()))
            campeon = self.eliminacionDirecta (finalista_1,finalista_2,True,total_arb, total_est,None)

        if campeon.getNombreEq() == get_equipo.getNombreEq():
            print("\n-----CAMPEON DE LA COPA es NUESTRO {}!!!-----".format(campeon.getNombreEq()))
            input("\n---Mostramos informacion del equipo consagrado---\n")
            campeon.mostrarEquipo()
        else:
            print("\n-----CAMPEON DE LA COPA es {}!!!-----".format(campeon.getNombreEq()))
            #creamos un metodo de la clase equipo para definir aleatoriamente la cantidad goles que hizo el equipo campeon (no es el seleccionado)
            #self.golesXDefecto (campeon)
            input("\n---Mostramos informacion del equipo consagrado---\n")
            campeon.mostrarEquipo()


        input("\nPRESIONE UNA TECLA para finalizar la opcion 2: ")
        os.system('clear')

    def opcion3 (self):
        print("\nSe ejecuta la opcion 3 - Creamos y guardamos un nuevo Equipo\n")  
        self.__manejEquip.mostrarNomEquipos()
        self.__manejEquip.cargaDeUnEquipoCSV()

        input("\nPRESIONE UNA TECLA para finalizar la opcion 3: ")
        os.system('clear')

    def opcion4 (self):
        print("\nSe ejecuta la opcion 4 - Añadimos un nuevo jugador a algún Equipo\n")
        fin = False
        self.__manejEquip.mostrarNomEquipos()
        
        equipo = input("\nIngrese el nombre del algún equipo con cant de jugadores < 5\n")
        getEquipo = self.__manejEquip.buscarEquipo(equipo)
        #cantJug = 5
        if getEquipo != None:
            cantJug = len(getEquipo.getJugadores())
        while getEquipo == None or cantJug >= 5:
                equipo = input("\nIngrese nuevamente el nombre del equipo con cant de jug < 5\n")
        
                if equipo.lower() == 'fin' or equipo.lower() == 'salir' or equipo.lower() =='salida':
                    fin = True
                    break
                getEquipo = self.__manejEquip.buscarEquipo(equipo)      #debo colocarlo despues del break, sino me salta error
                if getEquipo != None:
                    cantJug = len(getEquipo.getJugadores())

        if fin == False:
            nom = input("\nIngrese el nombre del jugador: ")
            apell = input("\nIngrese el apellido del jugador: ")
            #debemos asegurar que el jugador no se encuentra en otro equipo
            band = self.__manejEquip.verificarJug (nom, apell)
            while band == True:     #pues encontro el jugador
                nom = input("\nIngrese nuevamente el nombre del jugador: ")
                apell = input("\nIngrese nuevamente el apellido del jugador: ")
                band = self.__manejEquip.verificarJug (nom, apell)

            getEquipo.cargarUnJugador (nom, apell)
            totalEquipos = self.__manejEquip.getListaEquipos()

            archivo = open ('equipos.csv','w')
            Writer = csv.writer (archivo, delimiter=';')

            for equip in totalEquipos:
                Writer.writerow([equip.getNombreEq(), equip.getSede()])
                for jug in equip.getJugadores():
                    Writer.writerow([jug.getNombre(), jug.getApellido(), jug.getNacionalidad(),str(jug.getEdad()), str(jug.getNroCamiseta()), jug.getPosicionCampo(), jug.getApodo()])

                for ct in equip.getCuerpoTecnico():
                    Writer.writerow([ct.getNombre(),ct.getApellido(), ct.getNacionalidad(), str(ct.getEdad()), ct.getFuncion()])

        input("\nPRESIONE UNA TECLA para finalizar la opcion 4: ")
        os.system('clear')

    def opcion5 (self):
        print("\nSe ejecuta la opcion 5 - Mostrar info de algún equipo\n ")
        self.__manejEquip.mostrarNomEquipos()
        nom_equipo = input("\nIngrese el nombre de algun equipo existente\n")
        get_Equipo = self.__manejEquip.buscarEquipo(nom_equipo)
        while get_Equipo == None:
            nom_equipo = input("\nIngrese nuevamente el nombre de algun equipo existente\n")
            get_Equipo = self.__manejEquip.buscarEquipo(nom_equipo)

        get_Equipo.mostrarEquipo()

        input("\nPRESIONE UNA TECLA para finalizar la opcion 5: ")
        os.system('clear')

    def opcion6 (self):
        hoy = str(date.today())
        i = hoy.find('-')          
        j = hoy.rfind ('-')        
        anio = hoy[:i]
        mes = hoy[i+1:j]
        dia = hoy[j+1:]
        fecha= str(dia+'-'+mes+'-'+anio)

        print("\nSe ejecuta la opcion 6 - Mostramos toda la info de los partidos del hoy {}\n".format(fecha))
        i = 1
        if len(self.__listaPartidos) == 0:
            print ("\nNo se han registrado partidos el dia de hoy!\n")
        else:
            for partido in self.__listaPartidos:
                print(str(i).center(35,'-'))
                input("")
                partido.mostrarPartido()
                i += 1

        input("\nPRESIONE UNA TECLA para finalizar la opcion 6: ")
        os.system('clear')

    def opcion7 (self):
        print("\nSe ejecuta la opcion 7 - Mostramos informacion de un estadio leído")
        self.__manejEst.nombresEstadios ()
        nom_estadio = input("Ingrese el nombre de un estadio existente\n")
        get_estadio = self.__manejEst.buscarEstadio (nom_estadio)
        while get_estadio == None:
            nom_estadio = input("Ingrese de nuevo,el nombre de un estadio existente\n")
            get_estadio = self.__manejEst.buscarEstadio (nom_estadio)

        get_estadio.mostrarEstadio ()
        input("\nPRESIONE UNA TECLA para finalizar la opcion 7: ")
        os.system('clear')

    def opcion8 (self):
        print("\nSe ejecuta la opcion 8 - Mostramos informacion de un arbitro ingresado\n")
        self.__manejArb.mostrarNombreArb()
        nom_arbitro = input("Ingrese el nombre de un arbitro existente\n")
        get_arbitro = self.__manejArb.buscarArbitro (nom_arbitro)
        while get_arbitro == None:
            nom_arbitro = input("Ingrese de nuevo,el nombre de un arbitro existente\n")
            get_arbitro = self.__manejArb.buscarArbitro (nom_arbitro)

        get_arbitro.mostrarPersona ()
        input("\nPRESIONE UNA TECLA para finalizar la opcion 8: ")
        os.system('clear')

    def opcion9 (self):
        
        print("\nSe ejecuta la opcion 9 - Creamos y agregamos un nuevo arbitro o estadio\n")
        opcion = input("1-Añadir new Arbitro. 2-Añadir new Estadio: ")
        while (opcion != '1' and opcion != '2'):
            opcion = input("1-Añadir new Arbitro. 2-Añadir new Estadio: ")
        if opcion == '1':
            self.__manejArb.mostrarNombreArb()
            nom_arbitro = input("\nIngrese el nombre de un nuevo arbitro:\n")
            apell_arbitro = input("\nIngrese el apellido de un nuevo arbitro:\n")
            arb = nom_arbitro + ' '+apell_arbitro
            get_arbitro = self.__manejArb.buscarArbitro (arb)
            while get_arbitro != None:
                nom_arbitro = input("\nIngrese de nuevo,el nombre de un nuevo arbitro:\n")
                apell_arbitro = input("\nIngrese de nuevo,el apellido de un nuevo arbitro:\n")
                arb = nom_arbitro + ' '+apell_arbitro
                get_arbitro = self.__manejArb.buscarArbitro (arb)

            self.__manejArb.cargarUnArbitro (nom_arbitro, apell_arbitro)        #Desde aquí podemos añadir a un nuevo arbitro si es necesario

            dicc = self.__manejArb.toJSON()
            self.__objEncArb.guardarArchJSON(dicc,'arbitros.json')

            dicc = self.__objEncArb.leerArchJSON('arbitros.json')
            self.__manejArb = self.__objEncArb.decodificarDicc(dicc)

        else:
            self.__manejEst.nombresEstadios ()
            nom_estadio = input("\nIngrese el nombre de un nuevo estadio: ")
            get_estadio = self.__manejEst.buscarEstadio (nom_estadio)
            while get_estadio != None:
                nom_estadio = input("\nIngrese de nuevo,el nombre de un nuevo estadio: ")
                get_estadio = self.__manejEst.buscarEstadio (nom_estadio)

            ciudad = input("\nIngrese la ciudad del estadio: ")
            capacMax = int(input("\nIngrese la capacidad maxima: "))
            newEstadio = Estadio (nom_estadio, ciudad,capacMax)

            pos = int(input("\nIngrese la posicion a insertar: "))
            self.__manejEst.insertarElemento (pos,newEstadio)

            dicc = self.__manejEst.toJSON()
            self.__jsonEst.guardarArchJSON(dicc,'estadios.json')

            dicc = self.__jsonEst.leerArchJSON('estadios.json')
            self.__manejEst = self.__jsonEst.decodificarDicc(dicc)

        input("\nPRESIONE UNA TECLA para finalizar la opcion 10: ")
        os.system('clear')

    def opcion10 (self):
        print("\nSe ejecuta la opcion 11")
        self.__manejEquip.maximosGoleadores ()
        input("\nPRESIONE UNA TECLA para finalizar la opcion 11: ")
        os.system('clear')
