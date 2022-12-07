from datetime import datetime
from collections import namedtuple

Coordenada = namedtuple('Coordenada', 'latitud, longitud')

def parsea_fecha(cadena):
    result = datetime.today().date()
    if cadena != "":
        result = datetime.strptime(cadena, '%m/%d/%Y').date()
    return result

def parsea_coordenada(cadena):
    lista = cadena.split('/')
    return Coordenada(float(lista[0].strip()), float(lista[1].strip()))

def parsea_boolean(cadena):
    mayusculas = cadena.upper()
    return mayusculas == 'TRUE'