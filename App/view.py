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
#  Variables
# ___________________________________________________


bikefile = '201801-1-citibike-tripdata.csv'
initialstation = None
RecursionLimit = 20000


# ___________________________________________________
#  Menu principal
# ___________________________________________________

def print_menu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de bicicletas de Nueva York")
    print("3- Cantidad de clusters de Viajes")
    print("4- Ruta turística Circular")
    print("5- Estaciones críticas")
    print("6- Ruta turística por resistencia")
    print("7- Recomendador de Rutas")
    print("8- Ruta de interés turístico")
    print("9- Identificación de Estaciones para Publicidad")
    print("10- Identificación de Bicicletas para Mantenimiento")
    print("0- Salir")
    print("*******************************************")


def option_two():
    print("\nCargando información de bicicletas de Nueva York ....")
    controller.load_trips(cont)
    print("Archivos cargados\n")


def option_three():
    clusters_number = controller.clusters_number(cont)
    same_cluster = controller.same_cluster(clusters_number[1], station_1, station_2)
    if same_cluster == True:
        same_cluster = "sí"
    else:
        same_cluster = "no"
    print("\nEl total de clusters es:", clusters_number[0])
    print("Las estaciones", same_cluster, "pertenecen al mismo cluster")


"""
Menu principal
"""

while True:
    print_menu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init_analyzer()

    elif int(inputs[0]) == 2:
        execution_time = timeit.timeit(option_two, number=1)
        print("Número de viajes cargados:", controller.total_trips(cont))
        print("Número de vértices en el grafo:", controller.vertex_number(cont))
        print("Número de arcos en el grafo:", controller.edges_number(cont))
        print("Tiempo de ejecución: " + str(execution_time))

    elif int(inputs[0]) == 3:
        print("Ingrese los ids de las estaciones a buscar")
        station_1 = input("Id de la primera estación: ")
        station_2 = input("Id de la segunda estación: ")
        execution_time = timeit.timeit(option_three, number=1)
        print("Tiempo de ejecución: " + str(execution_time))

    elif int(inputs[0]) == 4:
        print("No disponible")

    elif int(inputs[0]) == 5:
        print("No disponible")

    elif int(inputs[0]) == 6:
        print("No disponible")

    elif int(inputs[0]) == 7:
        print("No disponible")

    elif int(inputs[0]) == 8:
        print("No disponible")

    elif int(inputs[0]) == 9:
        print("No disponible")

    elif int(inputs[0]) == 10:
        print("No disponible")

    else:
        sys.exit(0)
sys.exit(0)

# Opción 2


# def printMenu():
#     print('\n')
#     print('-----------------------------------------------')
#     print('1- Inicializar Analizador')
#     print('2- Cargar información City Bike')
#     print('3- Calcular componentes conectados')
#     print('4- Ruta Circular a seguir')
#     print('5- Estaciones críticas')
#     print('6- Ruta según resitencia')
#     print('7- Recomendador de rutas')
#     print('8- Ruta de interés')
#     print('9- Estaciones para publicidad')
#     print('10- Identificador mantenimiento de bicicletas')
#     print('0- Salir')
#     print('-----------------------------------------------')

# def optiontwo():
#     print('\nCargando información rutas City Bike ....')
#     controller.loadFile(cont,bikefile)
#     numedges = controller.totalConnections(cont)
#     numvertex = controller.totalStations(cont)
#     print('Número de vertices: ' + str(numvertex))
#     print('Numero de arcos: ' + str(numedges))
#     print('El límite de recursión actual: ' + str(sys.getrecursionlimit()))
#     sys.setrecursionlimit(RecursionLimit)
#     print('El límite de recursión se ajusta a: ' + str(RecursionLimit))


# def optionThree():
#     firts_station = input('\nID primera estación: ')
#     second_station = input('ID segunda estación: ')
#     print('El número de componentes conectados es: ' +
#           str(controller.connectedComponents(cont)))
#     sc = controller.sameComponent(cont, firts_station, second_station)
#     if (sc == True):
#         print('Las estaciones ' + firts_station +' y ' + second_station + ' pertenecen al mismo cluster')
#     else:
#         print('Las estaciones' + firts_station  +' y ' + second_station + ' no pertenecen al mismo cluster')


# def optionFour():
#     None

# def optionFive():
#     None

# def optionSix():
#     None

# def optionSeven():
#     None

# def optionEight():
#     None

# def optionNine():
#     None

# def optionTen():
#     None


# """
# Menu principal
# """
# while True:
#     printMenu()
#     inputs = input('Seleccione una opción para continuar \n')

#     if int(inputs[0]) == 1:
#         print('\nInicializando...')
#         cont = controller.init()
#     elif int(inputs[0]) == 2:
#         optiontwo()
#     elif int(inputs[0]) == 3:
#         optionThree()

#     elif int(inputs[0]) == 4:
#         optionFour()
#     elif int(inputs[0]) == 5:
#         optionFive()
#     elif int(inputs[0]) == 6:
#         optionSix()
#     elif int(inputs[0]) == 7:
#         optionSeven()
#     elif int(inputs[0]) == 8:
#         optionEight()
#     elif int(inputs[0]) == 9:
#         optionNine()
#     elif int(inputs[0]) == 10:
#         optionTen()
#     else:
#         sys.exit(0)
# sys.exit(0)
