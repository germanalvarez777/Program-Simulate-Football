import csv
from datetime import date
import re
from claseEquipo import Equipo
from claseJugador import Jugador
from claseCuerpoTec import CuerpoTecnico
#from claseObjectEncoderE import ObjectEncoderE

class ManejaEquipos(object):
    __listaEquipos = []
    def __init__ (self):
        self.__listaEquipos = []
    def agregarEquipo (self, unEquipo):
        self.__listaEquipos.append(unEquipo)

    def agregarJugador (self, unJugador):
        long = len(self.__listaEquipos)
        self.__listaEquipos[long-1].addJugador(unJugador)

    def testListaEquipos (self):
        archivo = open ('equipos.csv','r')
        Reader = csv.reader (archivo, delimiter=';')
        
        for fila in Reader:
            #nombreEquipo, Sede
            #if re.match('[(a-z0-9\_\-\.)]+,[(a-z)]{5,80}$', fila[1]):
            if len(fila) == 2:
                nomEq = fila[0]
                sede = fila[1]
                unEquipo = Equipo (nomEq,sede)
                self.agregarEquipo (unEquipo)
            elif len(fila) == 7:
                nom = fila[0]
                apell = fila[1]
                nac = fila[2]
                edad = int(fila[3])
                nroC = int(fila[4])
                posicion = fila[5]
                apodo = fila[6]
                unJug = Jugador (nom,apell,nac,edad,nroC,posicion, apodo)
                unEquipo.addJugador(unJug)  
            elif len(fila) == 5:
                nom = fila[0]
                apell = fila[1]
                nac = fila[2]
                edad = int(fila[3])                
                funcion = fila[4]
                unCT = CuerpoTecnico (nom,apell,nac,edad,funcion)
                
                unEquipo.addCuerpoTec(unCT)
                   
        archivo.close()


    def mostrarEquipos (self):
        input("\nMostramos todos los equipos guardados: ")
        for equip in self.__listaEquipos:
            print(''.center(40,'|'))
            equip.mostrarEquipo()

    def mostrarNomEquipos (self):
        print("Mostramos el nombre de todos los equipos\n")
        for equip in self.__listaEquipos:
            print("---->[%s]"%(equip.getNombreEq()))

    def buscarEquipo (self, nomEquipo):
        equipo = None
        i = 0
        band = False
        while (i < len(self.__listaEquipos) and band == False):
            if self.__listaEquipos[i].getNombreEq().lower() == nomEquipo.lower():
                band = True
                equipo = self.__listaEquipos[i]
            else:
                i += 1
        
        return equipo       #si lo encontro retorna el equipo, sino retorna None



    def cargarUnEquipo (self):                              #Funciona bien
        nom = input("\nIngrese el nombre del nuevo equipo: ")
        sede = input("\nIngrese la ciudad y pais proveniente del equipo:\n")
        unEquipo = Equipo (nom,sede)

        cantJug = int(input("\nIngrese la cantidad de jugadores: "))
        cantCT = int(input("\nIngrese la cantidad de personas del cuerpo tecnico: "))
        while (cantJug <= 0 and cantCT <= 0):
            cantJug = int(input("\nIngrese nuevamente, la cantidad de jugadores: "))
            cantCT = int(input("\nIngrese nuevamente,la cantidad de personas del cuerpo tecnico: "))

        cantJug += 1
        for i in range(1,cantJug):      #sino colocar cantjug + 1
            nom = input("\nIngrese el nombre del jugador {}: ".format(i))
            apell = input("\nIngrese el apellido del jugador {}: ".format(i))
            nac = input("\nIngrese la nacionalidad: ")
            edad = input("\nIngrese la edad del jugador {}: ".format(i))
            nroCam = input("\nIngrese el numero de la camiseta: ") 
            posicion = input("\nIngrese la posicion del jugador {}: ".format(i))
            apodo = input("\nIngrese el apodo del jugador: ")
            unJug = Jugador (nom,apell,nac,edad,nroCam,posicion, apodo)
            unEquipo.addJugador(unJug)

        cantCT += 1         #+1 para el for
        for j in range(1, cantCT):
            nom = input("\nIngrese el nombre del cuerpo tecnico {}: \n".format(j))
            apell = input("\nIngrese el apellido del cuerpo tecnico {}: \n".format(j))
            nac = input("\Ingrese la nacionalidad: ")
            edad = input("\nIngrese la edad {}: ".format(j))
            func = input("\nIngrese la funcion que ocupa: ")
            unCT = CuerpoTecnico (nom, apell, nac, edad,func)
            unEquipo.addCuerpoTec(unCT)

        self.agregarEquipo(unEquipo)

    def verificarJug (self, nom, apell):
        i = 0
        band = False
        nomAbuscar = nom + ' '+ apell
        while (i < len(self.__listaEquipos) and band == False):
            jugadores = self.__listaEquipos[i].getJugadores()
            j = 0
            while (j < len(jugadores) and band == False):
                nomyApp = jugadores[j].getNombre() + ' '+jugadores[j].getApellido()
                if nomyApp.lower() == nomAbuscar.lower():
                    band = True
                else:
                    j += 1
            
            i += 1
        
        return band

    def getListaEquipos(self):
        return self.__listaEquipos
    
    def cargaDeUnEquipoCSV (self):      #cargamos en CSV, los nuevos equipos creados            -->Funciona bien
        self.cargarUnEquipo()
        archivo = open ('equipos.csv','w')
        Writer = csv.writer (archivo, delimiter=';')

        for equip in self.__listaEquipos:
            Writer.writerow([equip.getNombreEq(), equip.getSede()])
            for jug in equip.getJugadores():
                Writer.writerow([jug.getNombre(), jug.getApellido(), jug.getNacionalidad(),str(jug.getEdad()), str(jug.getNroCamiseta()), jug.getPosicionCampo(), jug.getApodo()])

            for ct in equip.getCuerpoTecnico():
                Writer.writerow([ct.getNombre(),ct.getApellido(), ct.getNacionalidad(), str(ct.getEdad()), ct.getFuncion()])

    def maximosGoleadores (self):
        lista = []
        fecha = str(date.today())
        i = fecha.find('-')          #!= -1 encontro el char
        j = fecha.rfind ('-')        #rfind hace la busqueda desde el final hacia adelante
        anio = fecha[:i]
        mes = fecha[i+1:j]
        dia = fecha[j+1:]
        fecha= str(dia+'-'+mes+'-'+anio)
        input("\nMostramos los goleadores del día %s\n"%(fecha))
        
        for equip in self.__listaEquipos:
            jugadores = equip.getJugadores()
            for jug in jugadores:
                if jug.getCantGolesJug() > 0:       #añado a la lista solo aquellos jugadores que marcaron al menos un gol
                    lista.append(jug)           #lista donde tengo todos los jugadores por equipo
        
        if len(lista) == 0:
            print("----No se registraron goles en el dia %s----"%(fecha))
        else:
            lista.sort(reverse=True)        #ordenamos por sobrecarga de operadores, el jugador con mayor cantidad de goles
            for i in range(len(lista)):
                print(''.center(38,'*'))
                nom = lista[i].getNombre() + ' '+ lista[i].getApellido()
                print("Jugador: {} - Goles: {}".format(nom,lista[i].getCantGolesJug()))

    def obtenerEquipo (self, nroEquipo):
        i = 1
        band = False
        equipo = None
        while (i <= len(self.__listaEquipos) and band == False):
            if i == nroEquipo:
                band = True
                equipo = self.__listaEquipos[i-1]
            else:
                i += 1
        return equipo
