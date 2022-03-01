class Nodo (object):
    __estadio = None
    __siguiente = None
    def __init__ (self, estadio):
        self.__estadio = estadio
        self.__siguiente = None
    def getDato (self):
        return self.__estadio
    def getSiguiente (self):
        return self.__siguiente
    def setSiguiente (self, sigEstadio):
        self.__siguiente = sigEstadio
    