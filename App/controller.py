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


def init_analyzer():
    return model.new_analyzer()


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def load_trips(analyzer):
    for filename in os.listdir(cf.data_dir):
        if filename.endswith(".csv"):
            print("Cargando archivo: " + filename)
            load_file(analyzer, filename)
    return analyzer


def load_file(analyzer, file):
    file = cf.data_dir + file
    input_file = csv.DictReader(open(file, encoding="utf-8"), delimiter=",")
    for trip in input_file:
        model.add_trip(analyzer, trip)
    return analyzer


# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def total_trips(analyzer):
    return model.total_trips(analyzer)


def vertex_number(analyzer):
    return model.vertex_number(analyzer)


def edges_number(analyzer):
    return model.edges_number(analyzer)


def clusters_number(analyzer):
    return model.clusters_number(analyzer)


def same_cluster(sc, station_1, station_2):
    return model.same_cluster(sc, station_1, station_2)

# Opcion 2

# def init():
#     analyzer = model.newAnalyzer()
#     return analyzer

# def loadFile(citibike, tripfile):
#     tripfile = cf.data_dir + tripfile
#     input_file = csv.DictReader(open(tripfile, encoding= 'utf-8'), delimiter = ',')
#     for trip in input_file:
#         model.addTrip(citibike,trip)
#     return citibike


# def loadTrips(citibike):
#     for filename in os.listdir(cf.data_dir):
#         if filename.endswith('.csv'):
#             print('Cargando archivo: ' + filename)
#             loadFile(citibike, filename)
#     return citibike
# # ___________________________________________________
# #  Funciones para consultas
# # ___________________________________________________

# def totalStations(citibike):
#     return model.totalStations(citibike)

# def totalConnections(citibike):
#     return model.totalConnections(citibike)

# def connectedComponents(citibike):
#     """
#     Número de componentes fuertemente conectados
#     """
#     return model.numSCC(citibike)

# def sameComponent(citibike, s1, s2):
#     """
#     Informa si las estaciones están en el mismo componente
#     """
#     return model.sameCC(citibike, s1, s2)
