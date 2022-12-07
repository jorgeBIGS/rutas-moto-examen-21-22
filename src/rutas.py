from parseadores import *
from collections import defaultdict
import csv

DELIMITER = ';'

Ruta = namedtuple('Ruta', 'ciudad_inicio, coordenada, fecha_ruta, km, gasolineras, dificultad, zona_descanso, vel_max, vel_min')



def lee_rutas(fichero):
    '''1. **lee_rutas**: lee un fichero de entrada en formato CSV codificado en UTF-8, 
    y devuelve una lista de tuplas de tipo Ruta conteniendo todos los datos almacenados 
    en el fichero. 
    Utilice la función datetime.strptime(cadena, formato).date() 
    con el formato '%m/%d/%Y' para convertir la fecha. 
    Tenga en cuenta que hay valores en el csv para la fecha que están vacíos 
    (su valor es igual a “”), 
    en este caso deberá asignarle el valor del día actual (datetime.today().date()). 
    Use el método de cadenas split para separar la latitud de la longitud a la hora de hacer 
    la lectura de la coordenada. Por último, tenga en cuenta que el atributo 
    ciudad_inicio puede venir con un espacio adicional al final que hay que eliminar; 
    use la función strip para ello. (1 pto)'''
    result = []
    with open(fichero, encoding='UTF-8') as f:
        lector = csv.reader(f, delimiter=DELIMITER)
        #Aguadulce;37.25/-4.991359;8/8/2021;32.21;9;alta;True;106;66
        next(lector)
        for ciudad_inicio, coordenada, fecha_ruta, km, gasolineras, dificultad, zona_descanso, vel_max, vel_min in lector:
            ciudad_inicio = ciudad_inicio.strip()
            coordenada = parsea_coordenada(coordenada.strip())
            fecha_ruta = parsea_fecha(fecha_ruta.strip())
            km = float(km.strip())
            gasolineras = int(gasolineras.strip())
            dificultad = dificultad.strip()
            zona_descanso = parsea_boolean(zona_descanso.strip())
            vel_max = int(vel_max.strip())
            vel_min = int(vel_min.strip()) 
            result.append(Ruta(ciudad_inicio, coordenada, fecha_ruta, km, gasolineras, dificultad, zona_descanso, vel_max, vel_min ))
    return result


def acumula_kms_por_meses(rutas):
    '''2. **acumular_kms_por_meses**: recibe una lista de tuplas 
    de tipo Ruta, y devuelve un diccionario que asocia a cada año 
    una lista con el total de kilómetros que se han recorrido en 
    cada mes. Si en alguno de los meses no se ha realizado ninguna 
    ruta, debe aparecer el valor 0.0. 
    Los valores en la lista deben estar ordenados cronológicamente, 
    es decir, el primer valor se corresponde con enero, el segundo con 
    febrero, y así sucesivamente. (3 ptos)
    Por ejemplo, con los datos del fichero, 
    el valor devuelto debe ser:
    {2021: [426.04, 514.24, 1060.5, 863.1, 507.82, 672.4, 
    962.27, 774.1, 798.38, 918.56, 410.67, 370.63], 
    2022: [604.88, 1849.68, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    indicando que, en enero del 2022, el total de kilómetros recorridos por 
    el motorista fueron 604.88.'''
    result = dict()
    for r in rutas:
        clave = r.fecha_ruta.year
        if not clave in result:
            result[clave] = [0.,0., 0.,0., 0.,0., 0.,0.,0.,0.,0.,0.]
            result[clave][r.fecha_ruta.month-1] = r.km
        else:
            result[clave][r.fecha_ruta.month-1] += r.km
    return result

def acumula_kms_por_meses_f(rutas):
    '''2. **acumular_kms_por_meses**: recibe una lista de tuplas 
    de tipo Ruta, y devuelve un diccionario que asocia a cada año 
    una lista con el total de kilómetros que se han recorrido en 
    cada mes. Si en alguno de los meses no se ha realizado ninguna 
    ruta, debe aparecer el valor 0.0. 
    Los valores en la lista deben estar ordenados cronológicamente, 
    es decir, el primer valor se corresponde con enero, el segundo con 
    febrero, y así sucesivamente. (3 ptos)
    Por ejemplo, con los datos del fichero, 
    el valor devuelto debe ser:
    {2021: [426.04, 514.24, 1060.5, 863.1, 507.82, 672.4, 
    962.27, 774.1, 798.38, 918.56, 410.67, 370.63], 
    2022: [604.88, 1849.68, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    indicando que, en enero del 2022, el total de kilómetros recorridos por 
    el motorista fueron 604.88.'''
    result = defaultdict(lambda :[0.]*12)
    for r in rutas:
        result[r.fecha_ruta.year][r.fecha_ruta.month-1] += r.km
    return result