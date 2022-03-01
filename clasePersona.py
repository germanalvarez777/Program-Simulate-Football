class Persona(object):
    __apellido = None
    __nombre = None
    __nacionalidad = None
    __edad = None
    def __init__ (self, nom, apell, nac, edad):
        self.__nombre = nom
        self.__apellido = apell
        self.__nacionalidad = nac
        self.__edad = edad
    
    def mostrarPersona (self):
        print("\nNombre: {} - Apellido: {}\nNacionalidad: {} - Edad: {} años\n".format(self.__nombre, self.__apellido, self.__nacionalidad, self.__edad))

    def getNombre (self):
        return self.__nombre
    def getApellido (self):
        return self.__apellido
    def getNacionalidad (self):
        return self.__nacionalidad
    def getEdad (self):
        return self.__edad
