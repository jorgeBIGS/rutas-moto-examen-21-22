from rutas import *


def test_ciudades_top_tiempo_dificultad(datos):
    print(ciudades_top_tiempo_dificultad(datos, 3))
def test_top_rutas_lejanas(datos):
    print(top_rutas_lejanas(datos, 2,  Coordenada(35.15, -8.76)))

def test_diferencias_kms_meses_anyo(datos):
    diccionario = diferencias_kms_meses_anyo(datos)
    print(diccionario[2021])   

def test_acumula_kms_por_meses(datos):
    print(acumula_kms_por_meses(datos))

def test_lee_rutas(datos):
    print(list(d.zona_descanso for d in datos))
    print(len(datos))

if __name__ == '__main__':
    RUTAS = lee_rutas('data/rutas_motos.csv')
    #test_lee_rutas(RUTAS)
    #test_acumula_kms_por_meses(RUTAS)
    #test_diferencias_kms_meses_anyo(RUTAS)
    #test_top_rutas_lejanas(RUTAS)
    test_ciudades_top_tiempo_dificultad(RUTAS)