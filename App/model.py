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
import collections
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

def newAnalyzer():

    try:
        citybike = {
                    'stops':  m.newMap(numelements=50,
                                     maptype='PROBING',
                                     comparefunction=compareStopsIds),
                    'graph': gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=50,
                                              comparefunction=compareStopsIds),
                    'paths': None
        }
        return citybike
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


# Funciones para agregar informacion al grafos

def addTrip(citybike, trip):
    origin = trip['start station id']
    destination = trip['end station id']
    duration = int(trip['tripduration'])    
    addStation(citybike, origin)
    addStation(citybike, destination)    
    addConnection(citybike, origin, destination, duration)
    return citybike

def addStation(citybike, stationid):
    """
    Adiciona una estación como vértice al grafo
    """
    try:
        if not gr.containsVertex(citybike['graph'], stationid):
            gr.insertVertex(citybike['graph'], stationid)
        return citybike
    except Exception as exp:
        error.reraise(exp, 'model:addStation')

def addConnection(citybike, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(citybike['graph'], origin, destination)
    if edge is None:
        gr.addEdge(citybike['graph'], origin, destination, duration)
    return citybike

def recursivo(diccionario, station):
    return gr.adjacents(diccionario['graph'],station)

def adjacentscomponents(analyzer, station1):
    """
    Mira cuales son los componentes conectados a la
    estación de inicio

    Args:
        analyzer ([dict]): Datos grafo citybike
        station1 ([str]): Estación de inicio
    """
    values = gr.adjacents(analyzer['graph'], station1)
    for i in range(1,values['size']+1):
        a = lt.getElement(gr.adjacents(analyzer['graph'], station1),i)
   

# ==============================
# Funciones de consulta
# ==============================

def totalStations(citybike):
    return gr.numVertices(citybike['graph'])

def totalConnections(citybike):
    return gr.numEdges(citybike['graph'])

def numSCC(citybike):
    citybike['graph'] = scc.KosarajuSCC(citybike['graph'])
    return scc.connectedComponents(citybike['graph'])

def sameCC(sc, station1, station2):
    return scc.stronglyConnected(sc['graph'], station1, station2)

# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================

def compareStopsIds(stop, keyvaluestop):

    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0 
    elif (stop > stopcode):
        return 1
    else:
        return -1


def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1