from sqlalchemy import create_engine            #punto de entrada a la BaseDatos (permite a SQLAlchemy comunicarse con la Base de datos)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///datos.db')            #se especifica la cadena de conexion hacia la base de datos
Session = sessionmaker(bind=engine)
session = Session()                         #Session es una transaccion que permite ejecutar varias operaciones sobre objetos creados y plasmar sus datos en DB
Base = declarative_base()

#Se crea una clase llamada Base con el método declarative_base(). 
#Esta clase será de la que hereden todos los modelos y tiene la capacidad 
# de realizar el mapeo correspondiente a partir de la metainformación (atributos de clase, nombre de la clase, etc.)