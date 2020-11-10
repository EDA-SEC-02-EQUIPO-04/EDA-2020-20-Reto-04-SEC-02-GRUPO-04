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

bikefile = ''
initialstation = None
RecursionLimit = 20000

# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print('\n')
    print('-----------------------------------------------')
    print('1- Inicializar Analizador')
    print('2- Cargar información City Bike')
    print('3- Calcular componentes conectados')
    print('4- Ruta Circular a seguir')
    print('5- Estaciones críticas')
    print('6- Ruta según resitencia')
    print('7- Recomendador de rutas')
    print('8- Ruta de interés')
    print('9- Estaciones para publicidad')
    print('10- Identificador mantenimiento de bicicletas')
    print('0- Salir')
    print('-----------------------------------------------')

def optiontwo():
    print('\nCargando información rutas City Bike ....')
    controller.loadServices(cont,servicefile)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Número de vertices: ' + str(numvertex))
    print('Numero de arcos; ' + str(numedges))
    print('El límire de recursión actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(RecursionLimit)
    print('El límite de recursión se ajusta a: ' + str(RecursionLimit))


def optionThree():
    print('El número de componentes conectados es: ' +
          str(controller.connectedComponents(cont)))

def optionFour():
    None

def optionFive():
    None

def optionSix():
    None

def optionSeven():
    None

def optionEight():
    None

def optionNine():
    None
 
def optionTen():
    None


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar \n')

    if int(inputs[0]) == 1:
        print('\nInicializando...')
        cont = controller.int()
    elif int(inputs[0]) == 2:
        optiontwo()
    elif int(inputs[0]) == 3:
        optionThree()
    elif int(inputs[0]) == 4:
        optionFour()
    elif int(inputs[0]) == 5:
        optionFive()
    elif int(inputs[0]) == 6:
        optionSix()
    elif int(inputs[0]) == 7:
        optionSeven()
    elif int(inputs[0]) == 8:
        optionEight()
    elif int(inputs[0]) == 9:
        optionNine()
    elif int(inputs[0]) == 10:
        optionTen()
    else:
        sys.exit(0)
sys.exit(0)



        