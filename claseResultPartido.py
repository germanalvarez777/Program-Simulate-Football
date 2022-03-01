class ResultPartido (object):
    __cantGolesEqA = 0
    __cantGolesEqB = 0
    __arbitro = None
    __partido = None
    def __init__ (self,arbitro, partido,cantGolesEqA=0,cantGolesEqB=0):
        self.__cantGolesEqA = cantGolesEqA
        self.__cantGolesEqB = cantGolesEqB
        self.__arbitro = arbitro
        self.__partido = partido

    def EqAcontarGol (self):
        self.__cantGolesEqA += 1

    def EqBcontarGol (self):
        self.__cantGolesEqB += 1
    
    def getPartido_Result (self):
        return self.__partido
    
    def mostrarResultPartido (self, nombre_arb):
        eq1 = self.__partido.getEquipo1 ()
        eq2 = self.__partido.getEquipo2 ()
        print(''.center(30,'*'))
        nombre = self.__arbitro.getNombre()+' '+ self.__arbitro.getApellido()

        if nombre_arb == nombre:        #comparamos que el nombre del arbitro que dirigio este partido coincida
            print("\nGoles del Equipo %s: %d - Goles del Equipo %s: %d"%(eq1.getNombreEq(),self.__cantGolesEqA, eq2.getNombreEq(),self.__cantGolesEqB))
            if self.__cantGolesEqA > self.__cantGolesEqB:
                print("\nVictoria del Equipo %s!"%(eq1.getNombreEq()))
            elif self.__cantGolesEqB > self.__cantGolesEqA:
                print("\nVictoria del Equipo %s!"%(eq2.getNombreEq()))
            else:
                print("\nEmpate entre ambos Equipos!")
    
    def getCantGolesEqA (self):
        return self.__cantGolesEqA
    def getCantGolesEqB (self):
        return self.__cantGolesEqB
