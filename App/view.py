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


# bikefile = '201801-1-citibike-tripdata.csv'
# initialstation = None
# RecursionLimit = 20000

# ___________________________________________________
#  Menu principal
# ___________________________________________________


        
=======
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
    print("Las estaciones",same_cluster,"pertenecen al mismo cluster")

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
        print("Número de viajes cargados:",controller.total_trips(cont))
        print("Número de vértices en el grafo:",controller.vertex_number(cont))
        print("Número de arcos en el grafo:",controller.edges_number(cont))
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

