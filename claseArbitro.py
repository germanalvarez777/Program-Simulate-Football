from clasePersona import Persona
from claseResultPartido import ResultPartido

class Arbitro (Persona):
    __anioInicio = None
    __reemplazo = None
    __resultPartido = []        #clase asociacion, contiene partido

    def __init__ (self,nom, apell, nac, edad, anio='', reemplazo = None, resultPartido=[]):
        super().__init__(nom, apell, nac, edad)
        self.__anioInicio = anio
        self.__reemplazo = reemplazo            #arbitro de reemplazo en caso de lesion u otro problema
        self.__resultPartido = resultPartido
    
    def mostrarPersona(self):
        super().mostrarPersona()
        nom = str(self.getNombre() +' ' + self.getApellido())
        print("----Datos del Arbitro----")
        if self.__reemplazo == None:
            print("Año de Inicio: {}\n".format(self.__anioInicio))
        else:
            nom = str(self.__reemplazo.getNombre() +' ' + self.__reemplazo.getApellido())
            print("Año de Inicio: {} - Reemplazo: {}\n".format(self.__anioInicio, nom))
        if len(self.__resultPartido) == 0:
            nom = str(self.getNombre() +' ' + self.getApellido())
            print("\n{} no ha dirigido algún partido el dia de hoy!\n".format(nom))
        else:
            for result in self.__resultPartido:
                result.mostrarResultPartido (nom)

    def getAnioInicio (self):
        return self.__anioInicio
    def getReemplazo (self):
        return self.__reemplazo

    def guardarResultado (self,unPartido, cantGolesA, cantGolesB):        #recibimos la instancia de partido y los param cantGolesA, cantGolesB
        #creamos la instancia dentro del metodo y lo añadimos ala lista
        unaPlanilla = ResultPartido (self,unPartido)
        for i in range(cantGolesA):
            unaPlanilla.EqAcontarGol ()
        for j in range (cantGolesB):
            unaPlanilla.EqBcontarGol ()
        
        #if unaPlanilla not in self.__resultPartido:         #para no guardar la plantilla cada vez que se haga un gol
        self.__resultPartido.append(unaPlanilla)
    
    def mostrarResultado (self, partido):
        i = 0
        band = False
        while (i< len(self.__resultPartido) and band == False):
            if partido.getNombrePartido() == self.__resultPartido[i].getPartido_Result().getNombrePartido():
                band = True
                arbitro = partido.getArbitroPartido()
                nombre = arbitro.getNombre()+' '+arbitro.getApellido()
                self.__resultPartido[i].mostrarResultPartido(nombre)
            else:
                i += 1

    def getResultPartido (self):
        return self.__resultPartido

    def toJSON (self):
        dicc = dict(
            __class__ = self.__class__.__name__,
            __atributos__ = dict(
                nom = super().getNombre(),
                apell = super().getApellido(),
                nac = super().getNacionalidad(),
                edad = super().getEdad(),
                anio = self.__anioInicio,
                reemplazo = self.__reemplazo            #lista de result partido no lo guardamos, pues no hemos guardado partidos
            )
        )
        return dicc
