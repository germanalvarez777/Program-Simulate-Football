from claseJugador import Jugador
from claseCuerpoTec import CuerpoTecnico
class Equipo (object):
    __nombre= None
    __sede = None           #nombre de la cuidad y pais proveniente
    __jugadores = None
    __cuerpoTec = None
    __partidos = []
    def __init__ (self, nom, sede):
        self.__nombre = nom
        self.__sede = sede
        self.__jugadores = []
        self.__cuerpoTec = []           #composicion

        self.__partidos = []          #asociacion               #NO DEBO GUARDAR LOS PARTIDOS EN JSON -> los guardo en base de datos

        self.__puntos = 0
    def partidoJugado (self, unPartido):
        self.__partidos.append(unPartido)           #no es necesario especificar que: len(partidos) < 7, ya que no hacemos mundial

    def getPartidosEquipo (self):
        return self.__partidos

    def __del__ (self):
        print("\nBorramos los jugadores y cuerpo tecnico")
        del self.__jugadores, self.__cuerpoTec

    #def addJugador (self,nom, apell, nac, edad, nroCam, posic, apodo):
    def addJugador (self,unJugador):    
        if len(self.__jugadores) < 5:
            #if unJugador not in self.__jugadores:           #para que no se repita el jugador
            self.__jugadores.append(unJugador)
        else:
            print("\nYa hay 5 jugadores en el equipo!\n")

    def addCuerpoTec (self, cuerpoT):
        #cuerpoT = CuerpoTecnico (nom, apell, nac, edad, funcion)
        #if cuerpoT not in self.__cuerpoTec:                 #para que no se repita la persona
        self.__cuerpoTec.append(cuerpoT)

    def cargarUnJugador (self, nom, apell):
        
        nac = input("\nIngrese la nacionalidad: ")
        edad = input("\nIngrese la edad del jugador: ")
        nroCam = input("\nIngrese el numero de la camiseta: ") 
        posicion = input("\nIngrese la posicion del jugador: ")
        apodo = input("\nIngrese el apodo del jugador: ")
        unJug = Jugador (nom,apell,nac,edad,nroCam,posicion, apodo)
        self.addJugador(unJug)



    def getJugadores (self):
        return self.__jugadores
    def getCuerpoTecnico (self):
        return self.__cuerpoTec

    def getNombreEq (self):
        return self.__nombre

    def getSede (self):
        return self.__sede

    def buscarJugador (self, jugador):
        i = 0
        band = False
        while (i < len(self.__jugadores) and band == False):
            #if self.__jugadores[i].getNroCamiseta() == jugador.getNroCamiseta() and self.__jugadores[i].getApodo() == jugador.getApodo():
            if self.__jugadores[i] == jugador:
                band = True
            else:
                i += 1
        return band

    def mostrarEquipo (self):
        print("\nDatos del equipo: ")
        print("Nombre: {} - Sede: {}".format(self.__nombre, self.__sede))
        print("Datos de los Jugadores: ")        
        for jug in self.__jugadores:
            print(''.center(54,'='))
            jug.mostrarPersona()
            
        print("\nDatos del Cuerpo Tecnico: ")
        
        for ct in self.__cuerpoTec:
            #print(''.center(18,'-'))
            ct.mostrarPersona()

    
    def acPuntos (self, cant):
        self.__puntos += cant
    
    def getPuntos (self):
        return self.__puntos
    
    def __lt__ (self, otroEquip):                   #sobrecarga de operadores - de menor a mayor (Para fase de grupos)
        return self.__puntos < otroEquip.getPuntos()
    