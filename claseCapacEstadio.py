class CapacEstadio (object):
    __cantPolicias = None
    __capacHabitantes = None
    __estadio = None
    __partido = None
    def __init__ (self, estadio, partido):
        self.__cantPolicias = 0
        self.__capacHabitantes = 0
        self.__estadio = estadio
        self.__partido = partido

    def cantidadPolicias (self, cant):
        if cant < self.__estadio.getCapacMax():
            self.__cantPolicias = cant
        else:
            print("\nLa cantidad de policias no puede superar la capac del estadio\n")
            self.__cantPolicias = 15000         #valor por defecto

    def cantidadHabitantes (self, cant):
        if cant < self.__estadio.getCapacMax():
            self.__capacHabitantes = cant
        else:
            print("\nLa cantidad de habitantes no puede superar la capac del estadio\n")
            self.__capacHabitantes = 37592          #valor por defecto

    def mostrarCapacEstadio (self):
        if self.__partido != None and (self.__cantPolicias > 0 and self.__capacHabitantes > 0):
            print("\nCantidad de Policias custodiando: {}\nCantidad de Espectadores: {}".format(self.__cantPolicias, self.__capacHabitantes))
            print("Partido: {} - Instancia: {}\n".format(self.__partido.getNombrePartido(), self.__partido.getInstancia()))
        else:
            print("\nNo hay datos por mostrar con respecto al partido disputado en {}".format(self.__estadio.getNombre())) 



