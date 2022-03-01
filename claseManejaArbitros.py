import json
import numpy as np
from claseArbitro import Arbitro

from models import db
from models import Arbitros

class ManejaArbitros(object):
    __cantidad = None
    __dimension = None
    __incremento = None
    def __init__ (self, dim=3,inc=3):
        self.__cantidad = 0
        self.__incremento = inc
        self.__dimension = dim
        self.__arbitros = np.empty (dim, dtype=Arbitro)
    
    def agregarArbitro (self, unArb):
        if self.__cantidad == self.__dimension:
            self.__dimension += self.__incremento
            self.__arbitros.resize(self.__dimension)
        self.__arbitros[self.__cantidad] = unArb
        self.__cantidad += 1
    
    def mostrarArbitros (self):
        print("\nMostramos el listado de arbitros: ")
        for i in range(self.__cantidad):
            print(''.center(22,':'))
            self.__arbitros[i].mostrarPersona()

    def getListaArb (self):
        return self.__cantidad

    def getArbitros (self):
        arbitros = []
        for i in range (self.__cantidad):
            arbitros.append(self.__arbitros[i])
        
        return arbitros

    def guardarArbitrosBD (self):
        for i in range(self.__cantidad):
            if self.__arbitros[i].getReemplazo() != None:
                nuevo_arbitro = Arbitros (
                        nom = self.__arbitros[i].getNombre(),
                        apell = self.__arbitros[i].getApellido(),
                        nac = self.__arbitros[i].getNacionalidad(),
                        edad = self.__arbitros[i].getEdad(),
                        anio = self.__arbitros[i].getAnioInicio(),
                        reemplazo = self.__arbitros[i].getReemplazo().getNombre()
                        #resultadPartido = None
                )
            else:
                nuevo_arbitro = Arbitros (
                            nom = self.__arbitros[i].getNombre(),
                            apell = self.__arbitros[i].getApellido(),
                            nac = self.__arbitros[i].getNacionalidad(),
                            edad = self.__arbitros[i].getEdad(),
                            anio = self.__arbitros[i].getAnioInicio(),
                            reemplazo = None
                            #resultadPartido = None
                    )
                    
            db.session.add(nuevo_arbitro)
            db.session.commit()

    """  
    def testListaArbitros (self):
        archivo = open ('arbitros.csv', 'r')
        Reader = csv.reader (archivo, delimiter=';')
        band = True
        for fila in Reader:
            if band:
                #Nombre;Apellido;Nacionalidad;Edad;Año de Inicio (reemplazo queda en None)
                band = not band     #salteamos cabecera
            else:
                if re.search ('fin', fila[0]):
                    print("\nDatos del arbitro invalidos")
                else:
                    nom = fila[0]
                    apell = fila[1]
                    nac = fila[2]
                    edad = int(fila[3])
                    anioIni = int(fila[4])
                    unArbitro = Arbitro (nom,apell,nac,edad,anioIni)
                    self.agregarArbitro(unArbitro)
    
        archivo.close()
    """
    def toJSON (self):
        dicc = dict (
            __class__ = self.__class__.__name__,
            arbitros = [self.__arbitros[i].toJSON() for i in range(self.__cantidad)]
        )
        return dicc  
        
    def mostrarNombreArb (self):
        print("\nNombre de los arbitros: ")
        for i in range(self.__cantidad):
            nom = self.__arbitros[i].getNombre() + ' '+ self.__arbitros[i].getApellido()
            print('---> [%s]'%(nom))

    def buscarArbitro (self, nombreArb):
        i = 0
        band = False
        arbitro = None
        while (i < self.__cantidad and band == False):
            nom = self.__arbitros[i].getNombre() + ' '+ self.__arbitros[i].getApellido()
            if nom.lower() == nombreArb.lower():
                band = True
                arbitro = self.__arbitros[i]
            else:
                i += 1

        return arbitro      #si encontro el arbitro, lo retorna, sino retorna None

    def cargarUnArbitro (self, nombre, apellido):
        nacionalidad = input("\nIngrese la nacionalidad del mismo: ")
        edaD = int(input("\nIngrese su edad: "))
        anioIni = int(input("\nIngrese el año de inicio de actividad: "))

        unArbitro = Arbitro (nombre,apellido,nacionalidad,edaD,anioIni)
        self.agregarArbitro(unArbitro)
        #ahora lo agregamos en la base de datos
        newArb = Arbitros (
            nom = nombre,
            apell = apellido,
            nac = nacionalidad,
            edad = edaD,
            anio = anioIni,
            reemplazo = None
        )
        db.session.add(newArb)
        db.session.commit()



    def obtenerUnArbitro (self, posicion):
        i = 1
        band = False
        unArb = None
        while (i <= self.__cantidad and band == False):
            if i == posicion:
                band = True
                unArb = self.__arbitros[i-1]
            else:
                i += 1

        return unArb

"""if __name__ == '__main__':       #Funciona bien
    ma = ManejaArbitros(3,2)
    ma.testListaArbitros()  
    ma.mostrarNombreArb()   """