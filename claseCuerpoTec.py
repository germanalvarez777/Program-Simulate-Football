import re
from clasePersona import Persona
class CuerpoTecnico (Persona):
    __funcion = None
    def __init__ (self, nom, apell, nac, edad, func=''):
        super().__init__(nom, apell, nac, edad)
        self.__funcion = func
    def mostrarPersona(self):
        super().mostrarPersona()
        print("-------------------------------------------")
        print("\nFuncion que Ocupa: %s" %(self.__funcion))

    def getFuncion (self):
        return self.__funcion
    

