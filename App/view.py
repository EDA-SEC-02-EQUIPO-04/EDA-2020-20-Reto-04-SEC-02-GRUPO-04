"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
"""

import sys
import config
from App import controller
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import stack
import timeit

assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables.
# ___________________________________________________


bikefile = '201801-1-citibike-tripdata.csv'
initialstation = None
RecursionLimit = 20000


# ___________________________________________________
#  Menu principal.
# ___________________________________________________

def printMenu():
    print('\n')
    print('-----------------------------------------------')
    print('1- Inicializar Analizador')
    print('2- Cargar información City Bike')
    print('3- Calcular componentes conectados')
    print('4- Ruta Circular a seguir')  # j.alegria
    print('5- Estaciones críticas')  # af.romerob1
    print('6- Ruta según resistencia')  # ma.vargas73
    print('7- Recomendador de rutas')  # af.romerob1 y ma.vargas73
    print('8- Ruta de interés turístico')  # j.alegria
    print('9- Estaciones para publicidad')  # ma.vargas73
    print('10- Identificador mantenimiento de bicicletas')  # j.alegria
    print('0- Salir')
    print('-----------------------------------------------')


def optiontwo():
    year = int(input('Año actual: '))
    print('\nCargando información rutas City Bike ....')
    controller.loadFile(cont, bikefile, year)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStations(cont)
    print('Número de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El límite de recursión actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(RecursionLimit)
    print('El límite de recursión se ajusta a: ' + str(RecursionLimit))


def optionThree():
    firts_station = input('\nID primera estación: ')
    second_station = input('ID segunda estación: ')
    print('El número de componentes conectados es: ' +
          str(controller.connectedComponents(cont)))
    sc = controller.sameComponent(cont, firts_station, second_station)
    if (sc == True):
        print('Las estaciones ' + firts_station + ' y ' + second_station + ' pertenecen al mismo cluster')
    else:
        print('Las estaciones ' + firts_station + ' y ' + second_station + ' no pertenecen al mismo cluster')


def option_four():
    print('Ingrese el total de tiempo disponible: ')
    print('Ejemplo: Entre 180 y 240 minutos')
    begin_time = input('Rango inferior de minutos: ')
    end_time = input('Rango superior de minutos: ')
    start_station = input('Código de estación de inicio: ')
    circular_quantity_found, report = controller.circular_route(cont, begin_time, end_time, start_station)
    print(f'Se encontraron {circular_quantity_found} recorridos circulares')
    for index, station in enumerate(report):
        print(f'Impresión de estación #{index}')
        print(f'Comienzo en estación {station["start_station"]}')
        print(f'Termina en estación {station["end_station"]}')
        print(f'Duración {station["duration"]}\n')



def option_five():
    top_in_stations = controller.top_stations(cont, "in")
    top_out_stations = controller.top_stations(cont, "out")
    lowest_stations = controller.low_stations(cont)
    print("\nTop 3 estaciones de llegada:")
    print(top_in_stations[0])
    print(top_in_stations[1])
    print(top_in_stations[2])
    print("-------------------------------------------")
    print("Top 3 estaciones de salida:")
    print(top_out_stations[0])
    print(top_out_stations[1])
    print(top_out_stations[2])
    print("-------------------------------------------")
    print("Top 3 estaciones menos utilizadas:")
    print(lowest_stations[0])
    print(lowest_stations[1])
    print(lowest_stations[2])
    print("-------------------------------------------")


def optionSix():
    station = input('Estación de la que parte: ')
    time = int(input('Tiempo de resistencia: '))
    controller.adjacentsvertex(cont, station, time)


def optionSeven():
    print('1. 0 - 10')
    print('2. 11 - 20')
    print('3. 21 - 30')
    print('4. 31 - 40')
    print('5. 41 - 50')
    print('6. 51 - 60')
    print('7. 60+')
    agerange = int(input('Seleccione un rango de edad: '))
    initial, final, name_ini, name_fin = controller.agesroutes(cont, agerange)
    if initial == None and final == None and name_ini == None and name_fin == None:
        print('No se tienen estaciones comunes para ese rango de edad')
    else:
        controller.minimumCostPaths(cont, initial)
        controller.adjacents(cont, initial)
        controller.adjacentsvertex
        haspath = controller.hasPath(cont, final)
        print('Hay camino entre la estación base : ' +
              'y la estación: ' + final + ': ')
        print(haspath)
        path = controller.minimumCostPath(cont, final)
        if path is not None:
            pathlen = stack.size(path)
            print('El camino es de longitud: ' + str(pathlen))
            while (not stack.isEmpty(path)):
                stop = stack.pop(path)
                print(stop)
                print('Parte de la ruta ' + name_ini + ' para llegar a ' + name_fin)
        else:
            print('No hay camino')


def option_eight():
    None


def optionNine():
    age_range = input(
        "Ingrese la letra correspondiente al rango de edad deseado:\na. 0-10\nb. 11-20\nc. 21-30\nd. 31-40\ne. 41-50\nf. 51-60\ng. 60+\n> ")
    if age_range == "a":
        age_range = "0-10"
    elif age_range == "b":
        age_range = "11-20"
    elif age_range == "c":
        age_range = "21-30"
    elif age_range == "d":
        age_range = "31-40"
    elif age_range == "e":
        age_range = "41-50"
    elif age_range == "f":
        age_range = "51-60"
    elif age_range == "g":
        age_range = "60+"
    most_used_stations_by_age_range = controller.most_used_stations_by_age_range(cont, age_range)
    lst = most_used_stations_by_age_range[0]
    value = most_used_stations_by_age_range[1]
    iterator = it.newIterator(lst)
    print("-------------------------------------------")
    print("Estaciones adyacentes que más utilizan las personas entre", age_range, "años:\n")
    while it.hasNext(iterator):
        print(it.next(iterator))
    print("-------------------------------------------")
    print("Total de viajes registrados en el sistema:", value)


def option_ten():
    None


"""
Menu principal
"""
while True:

    printMenu()
    inputs = input('Seleccione una opción para continuar \n')

    if int(inputs[0]) == 1:
        print('\nInicializando...')
        cont = controller.init()
    elif int(inputs[0]) == 2:
        optiontwo()
    elif int(inputs[0]) == 3:
        optionThree()
    elif int(inputs[0]) == 4:
        option_four()
    elif int(inputs[0]) == 5:
        execution_time = timeit.timeit(option_five, number=1)
        print("Tiempo de ejecución: " + str(execution_time))
    elif int(inputs[0]) == 6:
        optionSix()
    elif int(inputs[0]) == 7:
        optionSeven()
    elif int(inputs[0]) == 8:
        print('Ingrese un punto central para consultar accidentes en esa localización.')
        latitude = input('Latitud: ')
        longitude = input('Longitud: ')
        radius = input('Radio de búsqueda en millas: ')
        option_eight()
    elif int(inputs[0]) == 9:
        optionNine()
    elif int(inputs[0]) == 10:
        option_ten()
    else:
        sys.exit(0)
sys.exit(0)
