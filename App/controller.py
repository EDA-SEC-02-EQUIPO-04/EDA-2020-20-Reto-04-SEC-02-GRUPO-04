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
import os
import config as cf
from App import model
import csv
import os

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def init():
    analyzer = model.newAnalyzer()
    return analyzer

# # ___________________________________________________
# #  Funciones para la carga de datos y almacenamiento
# #  de datos en los modelos
# # ___________________________________________________

def loadFile(citybike, tripfile, year):
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding= 'utf-8'), delimiter = ',')
    for trip in input_file:
        model.addTrip(citybike,trip)
        years_i =trip['birth year'].split(',')
        initialroute_name = trip['start station name'].split(',')
        finalroute_name = trip['end station name'].split(',')
        for years in years_i:
            model.addyear(citybike, year - int(years.lower()), trip,initialroute_name, finalroute_name)
    return citybike

def loadTrips(citybike):
    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadFile(citybike, filename)
    return citybike
# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def totalStations(citybike):
    return model.totalStations(citybike)

def totalConnections(citybike):
    return model.totalConnections(citybike)

def connectedComponents(citybike):
    """
    Número de componentes fuertemente conectados
    """
    return model.numSCC(citybike)

def sameComponent(citybike, s1, s2):
    """
    Informa si las estaciones están en el mismo componente
    """
    return model.sameCC(citybike, s1, s2)

def adjacents(analyzer, vertex):
    model.adjacents(analyzer, vertex)

def adjacentsvertex(citybike, station, time):
    return model.adjacentscomponents(citybike,station, time)

def agesroutes(analyzer, agerange):
    return model.agesroutes(analyzer, agerange)

def minimumCostPaths(analyzer, initialStation):
    """
    Calcula todos los caminos de costo minimo de initialStation a todas
    las otras estaciones del sistema
    """
    return model.minimumCostPaths(analyzer, initialStation)


def hasPath(analyzer, destStation):
    """
    Informa si existe un camino entre initialStation y destStation
    """
    return model.hasPath(analyzer, destStation)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo desde initialStation a destStation
    """
    return model.minimumCostPath(analyzer, destStation)