import db

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date

#Para que se realize el mapeo entre clase-tabla
#se crean subclases de Base, con los metodos necesarios para definir las columnas y/o claves foraneas.
#además se define una columna x clase como clave primaria, que es manejada automaticamente por la base de datos

class Arbitros (db.Base):
    __tablename__ = 'Arbitros'
    nom = Column(String(20), primary_key= True)
    apell = Column(String(30), unique = False, nullable = False)
    nac = Column(String(80), unique = False, nullable = False)
    edad = Column(Integer,unique = False, nullable=False)
    anio = Column(String(5), unique = False, nullable=False)
    reemplazo = Column(String(15), unique=False, nullable=True)
    resultPartido = relationship ('ResultPartido', backref='Arbitros',lazy='dynamic')

class Partidos (db.Base):
    __tablename__ = 'Partidos'
    nom = Column (String(120),primary_key=True)
    inst = Column (String(80),unique = False,nullable=False)
    resultPartido = relationship ('ResultPartido', backref='Partidos',lazy='dynamic')

class ResultPartido (db.Base):
    __tablename__ = 'ResultPartido'
    idResultado = Column (Integer, primary_key = True)
    arbitro = Column(String, ForeignKey(Arbitros.nom))
    partido = Column (String, ForeignKey(Partidos.nom))
    cantGolesEqA = Column(Integer, unique = False, nullable=False)
    cantGolesEqB = Column(Integer, unique = False, nullable=False)
