import json
from claseManejaArbitros import ManejaArbitros
from claseArbitro import Arbitro

class ObjectEncoderArb:                #clase sin atributos
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
            if class_name == "ManejaArbitros":
                arbitros = dicc["arbitros"]
                manejador = class_()
                for i in range(len(arbitros)):
                    dArb = arbitros[i]
                    class_name = dArb.pop("__class__")
                    class_= eval(class_name)
                    atributos = dArb["__atributos__"]
                    unArbitro = class_(**atributos)

                    manejador.agregarArbitro (unArbitro)
                
                return manejador