from zope.interface import Interface
from zope.interface import implementer

class IElemento (Interface):
    #insertar elem en posicion determinada
    def insertarElemento (posicion, unElem):
        pass

    #agregar un elemento al final de la coleccion
    def agregarElemento (unElem):
        pass

    #mostrar los datos del elemento en una pos almacenada
    def mostrarElemento (posicion):
        pass