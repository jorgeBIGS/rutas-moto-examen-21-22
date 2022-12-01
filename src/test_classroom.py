import pytest
from rutas import *
from datetime import datetime, date

'''
Este fichero es de configuración para Github Classroom
NO DEBE MODIFICARSE bajo ningún concepto.
La modificación de este fichero supondrá una penalización.
'''


def test_lee_rutas():
    rutas = lee_rutas("data/rutas_motos.csv")
    assert len(rutas) == 105, 'Número de registros léidos incorrecto'
    assert rutas[0].ciudad_inicio == 'Aguadulce', 'Lectura incorrecta'
    assert rutas[-1].ciudad_inicio == 'Viso del Alcor (El)', 'Lectura incorrecta'    
    assert isinstance(rutas[0].coordenada, Coordenada), 'Error en el parseo del atributo coordenada'
    assert isinstance(rutas[0].fecha_ruta, date), 'Error en el parseo del atributo fecha_ruta'
    assert isinstance(rutas[0].km, float), 'Error en el parseo del atributo km'
    assert isinstance(rutas[0].zona_descanso, bool), 'Error en el parseo del atributo coordenada'

def test_acumular_kms_por_meses():
    rutas = lee_rutas("data/rutas_motos.csv")
    resultado = acumular_kms_por_meses(rutas)
    assert isinstance(resultado, dict), 'Error en el tipo de dato devuelto'
    assert resultado[2021][1] == 514.24, 'Resultado incorrecto'

def test_diferencias_kms_meses_anyo():
    rutas = lee_rutas("data/rutas_motos.csv")
    resultado = diferencias_kms_meses_anyo(rutas)
    assert isinstance(resultado, dict), 'Error en el tipo de dato devuelto'
    assert resultado[2021][1] == 546.26, 'Resultado incorrecto'

def test_top_rutas_lejanas():
    rutas = lee_rutas("data/rutas_motos.csv")
    resultado = top_rutas_lejanas(rutas, 3, Coordenada(37.3826, -5.99629), km_min=None)
    assert isinstance(resultado, list), 'Error en el tipo de dato devuelto'
    assert resultado[0].coordenada.latitud == 37.2, 'Resultado incorrecto'
    assert resultado[-1].coordenada.latitud == 37.29, 'Resultado incorrecto'

def test_ciudades_top_tiempo_dificultad():
    rutas = lee_rutas("data/rutas_motos.csv")
    resultado = ciudades_top_tiempo_dificultad(rutas)
    assert isinstance(resultado, dict), 'Error en el tipo de dato devuelto'
    assert resultado['alta'] == ['Montellano', 'Aguadulce', 'Guadalcanal'], 'Resultado incorrecto'
    assert resultado['media'] == ['Pedroso (El)', 'Pilas', 'Gines'], 'Resultado incorrecto'








