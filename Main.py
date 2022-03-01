import os
from claseEquipo import Equipo
from claseJugador import Jugador
from claseCuerpoTec import CuerpoTecnico
from claseObjectEncoderE import ObjectEncoderE
from claseManejaEquipos import ManejaEquipos

from claseArbitro import Arbitro
from claseManejaArbitros import ManejaArbitros
from claseEstadio import Estadio
from claseListaEstadios import ListaEstadios
from ObjectEncoderArb import ObjectEncoderArb
from ObjectEncoderEst import ObjectEncoderEst

from claseMenu import Menu

import db
from models import Partidos,Arbitros,ResultPartido

if __name__ == '__main__':

    db.Base.metadata.drop_all(db.engine)        #eliminar todos los registros de la base de datos
    db.Base.metadata.create_all(db.engine)      #crea las tablas de todos los modelos que se encuentren  importados con anterioridad
    
    menu = Menu ()
    salir = True
    while salir:
        print("""
        ===================================================================
        1 - Jugar un Amistoso.
        2 - Jugar Campeonato con 16 Equipos.
        3 - Añadir a un Equipo.
        4 - Ingresar un nuevo jugador en un equipo existente.
        5 - Ingresar el nombre de un EQUIPO y mostrar sus datos.
        6 - Mostrar los partidos del día.
        7 - Ingresar el nombre de un ESTADIO y mostrar sus datos.
        8 - Ingresar el nombre de un ARBITRO y mostrar sus datos.
        9 - Añadir un NUEVO arbitro o estadio.
        10 - Mostrar los goleadores del día.
        11 - Salir del Programa.
        ===================================================================
        """)
        op = input("Selecciona una opcion --->> ")
        os.system('clear')
        if (op != '1' and op != '2' and op != '3' and op != '4' and op != '5' and op != '6' and op != '7' and op != '8' and op != '9' and op != '10' and op != '11'):
            salir = False
            print("\nFinalizacion del programa, pues selecciono una opcion incorrecta!")
        else:
            if op == '11':
                menu.salir()
                salir = False
            else:
                menu.opcion (op)

        