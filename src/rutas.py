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


def diferencias_kms_meses_anyo(rutas):
    '''
        3. **diferencias_kms_meses_anyo**: recibe una lista de tuplas de tipo Ruta, y devuelve un 
        diccionario que asocia cada año con una lista con las diferencias en kilómetros recorrido
        s de cada mes de ese año con respecto al mes anterior. 
        Las diferencias deben estar ordenadas cronológicamente, es decir, el primer valor es la diferencia 
        entre febrero y enero, el segundo la diferencia entre marzo y febrero,
        y así sucesivamente. Tiene que usar de forma obligatoria la función del apartado anterior. (2 ptos)

        Por ejemplo, con los datos del fichero, el valor devuelto debe ser:
        ```
        {2021: [88.2, 546.26, -197.41, -355.27, 164.58, 289.87, -188.18, 24.29, 120.18, -507.89, -40.04], 2022: [1244.8, -1849.68, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
        ```
        indicando que, en el año 2021, la diferencia de kilómetros totales recorridos entre febrero y enero fue 88.2.
    '''
    kms_anyo = acumula_kms_por_meses(rutas)
    for a in kms_anyo:
        kms_anyo[a] = [t[0] - t[1] for t in list(zip(kms_anyo[a][1:],  kms_anyo[a][:-1]))]
    return kms_anyo


def distancia_manhattan(c1, c2):
    return abs(c1.latitud- c2.latitud) + abs(c1.longitud - c2.longitud)

def top_rutas_lejanas(rutas, n, c, km_min=None):
    '''
    4. **top_rutas_lejanas**: Dada una lista de tuplas de tipo Ruta, un valor entero n, un valor c de tipo 
    Coordenada, y un entero km_min, obtener una lista con las n rutas cuya ciudad de inicio está más lejana 
    a las coordenadas que se pasan como parámetro de entrada y cuyo número de kilómetros sea mayor al valor km_min. 
    La variable km_min tomará como valor por defecto None, en cuyo caso se tendrán en cuenta todas las rutas.

    Para calcular la distancia entre las distintas ciudades, deberá usar la distancia Manhattan. 
    Dadas dos coordenadas c1, y c2, la distancia Manhattan se calcula como d = |lat1-lat2| + |long1-long2|. 
    Donde lat1 y long1 son la latitud y longitud de c1, y lat2 y long2 son la latitud y longitud de c2. 
    Use el método abs para obtener el valor absoluto. (1,5 ptos)
    Por ejemplo, si n tiene el valor 2, c el valor (35.15, -8.76) y km_min = None, el valor devuelto debe ser:
    ```
    [Ruta(ciudad_inicio='Badolatosa', coordenada=Coordenada(latitud=37.31, longitud=-4.674225), fecha_ruta=datetime.date(2021, 10, 20), km=148.07, gasolineras=2, dificultad='baja', zona_descanso=False, vel_max=127, vel_min=87),
    Ruta(ciudad_inicio='Casariche', coordenada=Coordenada(latitud=37.29, longitud=-4.759777), fecha_ruta=datetime.date(2021, 2, 26), km=93.53, gasolineras=10, dificultad='baja', zona_descanso=False, vel_max=118, vel_min=78)]
    ```
    indicando que Badolatosa y Casariche son las ciudades más lejanas a las coordenadas 35.15 y -8.76. 
    Para hacerse una idea de si está haciendo bien o no el ejercicio, puede usar las coordenadas 
    específicas de Sevilla, que son lat = 37.3826 y long = -5.99629.
    '''
    if km_min==None:
        km_min = 0

    rutas_filtradas = [r for r in rutas if km_min<r.km]

    return sorted(rutas_filtradas, key = lambda r: distancia_manhattan(c, r.coordenada), reverse=True)[:n]


def transforma_a_ciudad_inicio(rutas):
    return [r.ciudad_inicio for r in rutas]

def ciudades_top_tiempo_dificultad(rutas, n=3):
    '''5. **ciudades_top_tiempo_dificultad**: Dada una lista
     de tuplas de tipo Ruta y un valor entero n, obtener un diccionario que relacione cada dificultad 
     con las ciudades de inicio de las n rutas con zona de descanso que han tardado más tiempo en hacerse,
      ordenadas de mayor a menor tiempo. Si suponemos que la velocidad de las rutas ha sido siempre constante 
      y con valor vel_min, podemos calcular el tiempo usando la fórmula t = km/vel_min. 
      El parámetro n tendrá un valor por defecto igual a 3. (2,5 ptos)
        Por ejemplo, si el valor de n es 3, el valor devuelto debe ser:
        ```
        {alta: ['Montellano', 'Aguadulce', 'Guadalcanal'], media: ['Pedroso (El)', 'Pilas', 'Gines'], baja: ['Rinconada (La)', 'Tocina', 'Algámitas']}
        ```
        indicando que, para la dificultad alta, las 3 rutas que más tiempo han tardado en hacerse han sido las que
        empezaron en Montellano, Aguadulce y Guadalcanal.
    '''
    result = defaultdict(list)
    rutas_filtradas = [r for r in rutas if r.zona_descanso]
    for r in rutas_filtradas:
        listado = result[r.dificultad]
        listado.append(r)
        result[r.dificultad] = sorted(listado, key = lambda r: r.km/r.vel_min)[:n]

    return {clave: transforma_a_ciudad_inicio(result[clave]) for clave in result}