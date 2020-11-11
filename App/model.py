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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error

assert config
from DISClib.Algorithms.Graphs import scc

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""


# -----------------------------------------------------
#                       API
# -----------------------------------------------------


def new_analyzer():
    analyzer = {
        "graph": gr.newGraph("ADJ_LIST", True, 1000, compare_stations),
        "map": m.newMap(comparefunction=compare_ids),
        "list": lt.newList()
    }
    return analyzer


# Funciones para agregar informacion al grafo

def add_trip(analyzer, trip):
    graph = analyzer["graph"]
    lst = analyzer["list"]
    start_station = trip["start station id"]
    end_station = trip["end station id"]
    duration = int(trip["tripduration"])
    lt.addLast(lst, trip)
    add_station(graph, start_station)
    add_station(graph, end_station)
    if start_station != end_station:
        add_link(analyzer, graph, start_station, end_station, duration)
    return analyzer


def add_station(graph, station_id):
    if gr.containsVertex(graph, station_id) == False:
        gr.insertVertex(graph, station_id)
    return graph


def add_link(analyzer, graph, start_station_id, end_station_id, duration):
    key = start_station_id + "+" + end_station_id
    if gr.getEdge(graph, start_station_id, end_station_id) is None:
        gr.addEdge(graph, start_station_id, end_station_id, duration)
        value = {"sum": duration, "trips_num": 1}
        m.put(analyzer["map"], key, value)
    else:
        entry = m.get(analyzer["map"], key)
        value = me.getValue(entry)
        value["sum"] += duration
        value["trips_num"] += 1
        avg = value["sum"] / value["trips_num"]
        gr.addEdge(graph, start_station_id, end_station_id, avg)
        m.put(analyzer["map"], key, value)
    return graph


# ==============================
# Funciones de consulta
# ==============================

def total_trips(analyzer):
    lst = analyzer["list"]
    return lt.size(lst)


def vertex_number(analyzer):
    graph = analyzer["graph"]
    return gr.numVertices(graph)


def edges_number(analyzer):
    graph = analyzer["graph"]
    return gr.numEdges(graph)


def clusters_number(analyzer):
    sc = scc.KosarajuSCC(analyzer["graph"])
    return scc.connectedComponents(sc), sc


def same_cluster(sc, station_1, station_2):
    return scc.stronglyConnected(sc, station_1, station_2)


# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================

def compare_stations(station_1, station_2):
    station_1 = int(station_1)
    station_2 = int(station_2["key"])
    if station_1 == station_2:
        return 0
    elif station_1 > station_2:
        return 1
    else:
        return -1


def compare_ids(id1, id2):
    id2 = id2["key"]
    if id1 == id2:
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

# Opcion 2
# def newAnalyzer():

#     try:
#         citibike = {
#                     'stops':  m.newMap(numelements=14000,
#                                      maptype='PROBING',
#                                      comparefunction=compareStopsIds),
#                     'graph': gr.newGraph(datastructure='ADJ_LIST',
#                                               directed=True,
#                                               size=1000,
#                                               comparefunction=compareStopsIds),
#                     'paths': None
#         }
#         return citibike
#     except Exception as exp:
#         error.reraise(exp, 'model:newAnalyzer')


# # Funciones para agregar informacion al grafos

# def addTrip(citibike, trip):
#     origin = trip['start station id']
#     destination = trip['end station id']
#     duration = int(trip['tripduration'])    
#     addStation(citibike, origin)
#     addStation(citibike, destination)    
#     addConnection(citibike, origin, destination, duration)
#     return citibike

# def addStation(citibike, stationid):
#     """
#     Adiciona una estación como vértice al grafo
#     """
#     try:
#         if not gr.containsVertex(citibike['graph'], stationid):
#             gr.insertVertex(citibike['graph'], stationid)
#         return citibike
#     except Exception as exp:
#         error.reraise(exp, 'model:addStation')


# def addConnection(citibike, origin, destination, duration):
#     """
#     Adiciona un arco entre dos estaciones
#     """
#     edge = gr.getEdge(citibike['graph'], origin, destination)
#     if edge is None:
#         gr.addEdge(citibike['graph'], origin, destination, duration)
#     return citibike


# # ==============================
# # Funciones de consulta
# # ==============================

# def totalStations(citibike):
#     return gr.numVertices(citibike['graph'])

# def totalConnections(citibike):
#     return gr.numEdges(citibike['graph'])

# def numSCC(citibike):
#     citibike['graph'] = scc.KosarajuSCC(citibike['graph'])
#     return scc.connectedComponents(citibike['graph'])

# def sameCC(sc, station1, station2):
#     return scc.stronglyConnected(sc['graph'], station1, station2)

# # ==============================
# # Funciones Helper
# # ==============================

# # ==============================
# # Funciones de Comparacion
# # ==============================

# def compareStopsIds(stop, keyvaluestop):

#     stopcode = keyvaluestop['key']
#     if (stop == stopcode):
#         return 0 
#     elif (stop > stopcode):
#         return 1
#     else:
#         return -1
