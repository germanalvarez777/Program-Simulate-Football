class Gol(object):
    __minuto = None
    __tiempo = None         #primer o segundo tiempo
    __partido = None
    __jugador = None
    def __init__(self, min,tiempo, part, jug):
        self.__minuto = min
        self.__tiempo = tiempo
        self.__partido = part
        self.__jugador = jug
    
        self.__partido.anotarGol (self)
        self.__jugador.addGolJug (self)

    def getMinGol (self):
        return self.__minuto
    def getTiempoGol (self):
        return self.__tiempo
    
    def mostrarGol (self):
        nomyapp = str(self.__jugador.getNombre() + ' '+ self.__jugador.getApellido())
        print("\nMinuto del Gol: {} - Tiempo: {}\nPartido: {}\nJugador que lo anotó: {}".format(self.__minuto, self.__tiempo, self.__partido.getNombrePartido(), nomyapp))
