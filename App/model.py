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
from DISClib.Algorithms.Graphs import dfo
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
                    'names':  m.newMap(numelements=50,
                                     maptype='PROBING',
                                     comparefunction=compareStopsIds),
                    'graph': gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=50,
                                              comparefunction=compareStopsIds),
                    'routes': gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=50,
                                              comparefunction=compareStopsIds),
                    'trips':  m.newMap(numelements=50,
                                     maptype='PROBING',
                                     comparefunction=compareStopsIds)
        }
        return citybike
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al grafos

def addTrip(citybike, trip):
    origin = trip['start station id']
    destination = trip['end station id']
    originstation = trip['start station name']
    laststation = trip['end station name']
    duration = int(trip['tripduration'])    
    year = int(trip['birth year'])
    addStation(citybike, origin, originstation)
    addStation(citybike, destination, laststation)    
    addConnection(citybike, origin, destination, duration)
    return citybike

def addStation(citybike, stationid, name):
    """
    Adiciona una estación como vértice al grafo
    """
    try:
        if not gr.containsVertex(citybike['graph'], stationid):
            gr.insertVertex(citybike['graph'], stationid)            
        if not m.contains(citybike['names'], name):
            m.put(citybike['names'],stationid, name)
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


def addTrip_routes(citybike, station, station2, time):
    origin = station
    destination = station2
    originstation = list(m.get(citybike['names'],station).values())[1]
    laststation = list(m.get(citybike['names'],station2).values())[1]
    duration = time  
    addStation_routes(citybike, origin, originstation)
    addStation_routes(citybike, destination, laststation)    
    addConnection_routes(citybike, origin, destination, duration)
    return citybike

def addStation_routes(citybike, stationid, name):
    """
    Adiciona una estación como vértice al grafo
    """
    try:
        if not gr.containsVertex(citybike['routes'], stationid):
            gr.insertVertex(citybike['routes'], stationid)        
        if not m.contains(citybike['names'], name):
            m.put(citybike['names'],stationid, name)
        return citybike
    except Exception as exp:
        error.reraise(exp, 'model:addStation')


def addConnection_routes(citybike, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(citybike['routes'], origin, destination)
    if edge is None:
        gr.addEdge(citybike['routes'], origin, destination, duration)
    return citybike

#Requerimiento 4

def adjacentscomponents(analyzer, station1, time):
    """
    Mira cuáles son los componentes conectados a la
    estación de inicio

    Args:
        analyzer ([dict]): Datos grafo citybike
        station1 ([str]): Estación de inicio
    """
    values = gr.adjacents(analyzer['graph'], station1)  #Lista estaciones adyacentes
    
    connections = lt.newList('SINGLE_LINKED')
    if values['size'] == 0:
        print('\nLa para que selecciono no tiene estaciones adyacentes, pruebe con otra ruta')
    else:
        for i in range(1,values['size']+1):
            station = lt.getElement(gr.adjacents(analyzer['graph'], station1),i)   #Número estación adyacente
            time_weight = gr.getEdge(analyzer['graph'],station1,station)['weight'] #Peso del arco 
            adjacent_station = gr.adjacents(analyzer['graph'],station) 
            if adjacent_station['size'] == 0 and time_weight<= time:           
                save = (station, time_weight, list(m.get(analyzer['names'],station).values())[1])
                lt.addLast(connections, save)            
                addTrip_routes(analyzer,station1, station, time_weight)  
            elif adjacent_station['size'] != 0:  
                for j in range(1,values['size']+1):
                    stationc = lt.getElement(gr.adjacents(analyzer['graph'], station1),j)
                    if stationc == station:
                        None
                    else:
                        stationsrecursive(analyzer, station, stationc, time)
    return connections
    
def stationsrecursive(analyzer, station, stationc, time):
    adjacent_station = gr.adjacents(analyzer['graph'], stationc)
    time_u = time 
    if adjacent_station['size'] == 0:    
        print(str(stationc)+'s') 
        print(type(station))
        print(type(stationc))
        x = gr.getEdge(analyzer['graph'],station,stationc)['weight']        
        print(x)
        time_u += x
        print(time_u)
        if time_u <= time:
            addTrip_routes(analyzer,station, stationc, x)
            time_u = time
        else:
            time_u = time
            None
    else:
        for j in range(1,adjacent_station['size']+1):
                stationc = lt.getElement(gr.adjacents(analyzer['graph'], station),j)
                adjacent_station = gr.adjacents(analyzer['graph'],station) 
                
                print(stationc)
                print(adjacent_station)
                x = gr.getEdge(analyzer['graph'],station,stationc)['weight']
                stationsrecursive(analyzer, station, stationc, time)

#Requerimiento 5 

def newage(year):
    """
    Crea una estructura para modelar los id de las rutas según la 
    edad

    Args:
        year(str): Rango de años en que nació la persona 
    return:
        Diccionario del año correspondiente con sus estaciones de
        entrada y salida 
    """

    p_year = {'year': year,
              'initialroute_id': lt.newList('SINGLE_LINKED', compareStopsIds),
              'finalroute_id': lt.newList('SINGLE_LINKED', compareStopsIds)
              }
    return p_year

def addyear(analyzer, year, route_id, initialroute_name, finalroute_name):
    years = analyzer['trips']
    existyear = m.contains(years, year)
    
    if existyear:
        entry = m.get(years, year)
        yearr = me.getValue(entry)
    else:
        yearr = newage(year)
        m.put(years, year, yearr)
    lt.addLast(yearr['initialroute_id'], (route_id['start station id'],initialroute_name))
    lt.addLast(yearr['finalroute_id'], (route_id['end station id'],finalroute_name))

def getagetrips(tripfile, agerange):

    if agerange == 1:    
        
    elif agerange == 2:
    elif agerange == 3:
    elif agerange == 4:
    elif agerange == 5:
    elif agerange == 6:
    elif agerange == 7:




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


def comparevertex(vertex1, vertex2):
    """
    Compara dos vertices
    """
    if (vertex1 == vertex2):
        return 0
    elif (vertex1 > vertex2):
        return 1
    else:
        return -1