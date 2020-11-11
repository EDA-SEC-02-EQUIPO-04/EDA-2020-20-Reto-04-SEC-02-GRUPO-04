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
