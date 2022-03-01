import json
from claseManejaEquipos import ManejaEquipos
from claseEquipo import Equipo
from claseJugador import Jugador
from claseCuerpoTec import CuerpoTecnico

class ObjectEncoderE:                #clase sin atributos
    def guardarArchJSON (self, dicc, archivo):
        with open(archivo, 'w', encoding = "UTF-8") as destino:
            json.dump (dicc, destino, indent = 4)
            destino.close()
    
    def leerArchJSON (self, archivo):
        with open (archivo, encoding = "UTF-8") as fuente:
            dicc = json.load(fuente)
            fuente.close()
            return dicc
        
    def decodificarDicc (self, dicc):
        if "__class__" not in dicc:
            return dicc
        else:
            class_name = dicc["__class__"]
            class_= eval(class_name)
            if class_name == "ManejaEquipos":
                equipos = dicc["equipos"]
                manejador = class_()
                for i in range(len(equipos)):
                    dequip = equipos[i]
                    class_name = dequip.pop("__class__")
                    class_= eval(class_name)
                    atributos = dequip["__atributos__"]
                    unEquipo = class_(**atributos)

                    manejador.agregarEquipo (unEquipo)
                    #print("Atributos: ", atributos['jug'])
                    jugadores = atributos['jug']
                    cuerpoTec = atributos['cuerpoTec']
                    
                    for j in range(len(jugadores)):
                        dJug = jugadores[j]
                        class_name = dJug.pop("__class__")
                        class_= eval(class_name)
                        #atributos = dJug["__atributos__"]
                        atributos2 = dJug.pop("__atributos__")
                        
                        unJugador = class_(**atributos2)
                        #unJugador = Jugador(**atributos2)
                        #input("\nJugador en ObjectEncoder: ")
                        
                        #print("\nSe creo jugador: ", unJugador.getNombre())
                        if type(unJugador) == Jugador:
                            #unEquipo.addJugador(unJugador)
                            manejador.agregarJugador(unJugador)

                    
                    for k in range(len(cuerpoTec)):
                        dcT = cuerpoTec[k]
                        class_name = dcT.pop("__class__")
                        class_= eval(class_name)
                        atributos = dcT.pop("__atributos__")
                        unCT = class_(**atributos)
                        if type(unCT) == CuerpoTecnico:
                            unEquipo.addCuerpoTec (unCT)

                    #manejador.agregarEquipo (unEquipo)             
                    #manejador.mostrarEquipos()

            return manejador