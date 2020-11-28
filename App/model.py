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
from DISClib.Algorithms.Graphs import dfs
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
from collections import Counter

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

                    "graph": gr.newGraph("ADJ_LIST", True, 1000, compare_stations),
                    "map": m.newMap(comparefunction=compare_ids),
                    "age_range": m.newMap(comparefunction=compare_maps),
                    "list": lt.newList(),
                    "station_names": m.newMap(comparefunction=compare_ids),
                    'names':  m.newMap(numelements=50,
                                     maptype='PROBING',
                                     comparefunction=compareStopsIds),                    
                    'trips':  m.newMap(numelements=500,
                                     maptype='PROBING',
                                     comparefunction=compareStopsIds),
                    'paths':  None,
                    "edges_map_0_10": m.newMap(comparefunction=compare_map_keys),
                    "edges_map_11_20": m.newMap(comparefunction=compare_map_keys), 
                    "edges_map_21_30": m.newMap(comparefunction=compare_map_keys),
                    "edges_map_31_40": m.newMap(comparefunction=compare_map_keys),
                    "edges_map_41_50": m.newMap(comparefunction=compare_map_keys),
                    "edges_map_51_60": m.newMap(comparefunction=compare_map_keys),
                    "edges_map_60_plus": m.newMap(comparefunction=compare_map_keys),
                    'stations': m.newMap(numelements=15000,
                                         maptype='PROBING',
                                         comparefunction=compareStopsIds)



        }
        return citybike
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

def recursivestations(station):
    try:
        station = {
                   'station': station,
                   'weight': None,
                   'adjacents': lt.newList('SINGLE_LINKED')

        }
        return station
    except Exception as exp:
        error.reraise(exp, 'model:recursivestations')

# Funciones para agregar informacion al grafos

def addTrip(citybike, trip):
    user_type = trip["usertype"]
    birth_year = trip["birth year"]
    station_names = citybike["station_names"]
    origin = trip['start station id']
    destination = trip['end station id']
    originstation = trip['start station name']
    laststation = trip['end station name']
    duration = int(trip['tripduration'])  
    if m.contains(station_names, trip["start station name"]) != True:
        m.put(station_names, origin, trip["start station name"])
    if m.contains(station_names, trip["end station name"]) != True:
        m.put(station_names, destination, trip["end station name"])
    addStation(citybike, origin, originstation)
    addStation(citybike, destination, laststation)
    age_range(citybike, origin, destination, duration, birth_year, user_type)    
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
    key = origin + "+" + destination
    edge = gr.getEdge(citybike['graph'], origin, destination)
    if edge is None:
        gr.addEdge(citybike['graph'], origin, destination, duration)
        value = {"sum": duration, "trips_num": 1}
        m.put(citybike["map"], key, value)
    else:
        entry = m.get(citybike["map"], key)
        value = me.getValue(entry)
        value["sum"] += duration
        value["trips_num"] += 1
        avg = value["sum"] / value["trips_num"]
        gr.addEdge(citybike['graph'], origin, destination, avg)
        m.put(citybike["map"], key, value)
    return citybike

def age_range(citybike, origin, destination, duration, birth_year, user_type):
    edges_map_0_10 = citybike["edges_map_0_10"]
    edges_map_11_20 = citybike["edges_map_11_20"]
    edges_map_21_30 = citybike["edges_map_21_30"]
    edges_map_31_40 = citybike["edges_map_31_40"]
    edges_map_41_50 = citybike["edges_map_41_50"]
    edges_map_51_60 = citybike["edges_map_51_60"]
    edges_map_60_plus = citybike["edges_map_60_plus"]
    if user_type == "Customer":
        age = 2020 - int(birth_year)
        age_map = citybike["age_range"]
        key = origin + "+" + destination
        inverse_key = destination + "+" + origin  
        if age < 11:
            age_range = "0-10"
            entry = m.get(age_map, age_range)
            if entry is None:
                m.put(age_map, age_range, edges_map_0_10)
            if m.get(edges_map_0_10, key) is None and m.get(edges_map_0_10, inverse_key) is None:            
                value = 1
                m.put(edges_map_0_10, key, value)
            elif m.get(edges_map_0_10, key) != None or m.get(edges_map_0_10, inverse_key):
                if m.get(edges_map_0_10, key) is None:
                    entry = m.get(edges_map_0_10, inverse_key)
                    value = me.getValue(entry)
                    value += 1
                    m.put(edges_map_0_10, inverse_key, value)
                else:
                    entry = m.get(edges_map_0_10, key)
                    value = me.getValue(entry)
                    value += 1
                    m.put(edges_map_0_10, key, value)
        elif age < 21:
            age_range = "11-20"
            entry = m.get(age_map, age_range)
            if entry is None:
                m.put(age_map, age_range, edges_map_11_20)
            if m.get(edges_map_11_20, key) is None and m.get(edges_map_11_20, inverse_key) is None:            
                value = 1
                m.put(edges_map_11_20, key, value)
            elif m.get(edges_map_11_20, key) != None or m.get(edges_map_11_20, inverse_key):
                if m.get(edges_map_11_20, key) is None:
                    entry = m.get(edges_map_11_20, inverse_key)
                    value = me.getValue(entry)
                    value += 1
                    m.put(edges_map_11_20, inverse_key, value)
                else:
                    entry = m.get(edges_map_11_20, key)
                    value = me.getValue(entry)
                    value += 1
                    m.put(edges_map_11_20, key, value)
        elif age < 31:
            age_range = "21-30"
            entry = m.get(age_map, age_range)
            if entry is None:
                m.put(age_map, age_range, edges_map_21_30)
            if m.get(edges_map_21_30, key) is None and m.get(edges_map_21_30, inverse_key) is None:            
                value = 1
                m.put(edges_map_21_30, key, value)
            elif m.get(edges_map_21_30, key) != None or m.get(edges_map_21_30, inverse_key):
                if m.get(edges_map_21_30, key) is None:
                    entry = m.get(edges_map_21_30, inverse_key)
                    value = me.getValue(entry)
                    value += 1
                    m.put(edges_map_21_30, inverse_key, value)
                else:
                    entry = m.get(edges_map_21_30, key)
                    value = me.getValue(entry)
                    value += 1
                    m.put(edges_map_21_30, key, value)
        elif age < 41:
            age_range = "31-40"
            entry = m.get(age_map, age_range)
            if entry is None:
                m.put(age_map, age_range, edges_map_31_40)
            if m.get(edges_map_31_40, key) is None and m.get(edges_map_31_40, inverse_key) is None:            
                value = 1
                m.put(edges_map_31_40, key, value)
            elif m.get(edges_map_31_40, key) != None or m.get(edges_map_31_40, inverse_key):
                if m.get(edges_map_31_40, key) is None:
                    entry = m.get(edges_map_31_40, inverse_key)
                    value = me.getValue(entry)
                    value += 1
                    m.put(edges_map_31_40, inverse_key, value)
                else:
                    entry = m.get(edges_map_31_40, key)
                    value = me.getValue(entry)
                    value += 1
                    m.put(edges_map_31_40, key, value)
        elif age < 51:
            age_range = "41-50"
            entry = m.get(age_map, age_range)
            if entry is None:
                m.put(age_map, age_range, edges_map_41_50)
            if m.get(edges_map_41_50, key) is None and m.get(edges_map_41_50, inverse_key) is None:            
                value = 1
                m.put(edges_map_41_50, key, value)
            elif m.get(edges_map_41_50, key) != None or m.get(edges_map_41_50, inverse_key):
                if m.get(edges_map_41_50, key) is None:
                    entry = m.get(edges_map_41_50, inverse_key)
                    value = me.getValue(entry)
                    value += 1
                    m.put(edges_map_41_50, inverse_key, value)
                else:
                    entry = m.get(edges_map_41_50, key)
                    value = me.getValue(entry)
                    value += 1
                    m.put(edges_map_41_50, key, value)
        elif age < 61:
            age_range = "51-60"
            entry = m.get(age_map, age_range)
            if entry is None:
                m.put(age_map, age_range, edges_map_51_60)
            if m.get(edges_map_51_60, key) is None and m.get(edges_map_51_60, inverse_key) is None:            
                value = 1
                m.put(edges_map_51_60, key, value)
            elif m.get(edges_map_51_60, key) != None or m.get(edges_map_51_60, inverse_key):
                if m.get(edges_map_51_60, key) is None:
                    entry = m.get(edges_map_51_60, inverse_key)
                    value = me.getValue(entry)
                    value += 1
                    m.put(edges_map_51_60, inverse_key, value)
                else:
                    entry = m.get(edges_map_51_60, key)
                    value = me.getValue(entry)
                    value += 1
                    m.put(edges_map_51_60, key, value)
        elif age > 60:
            age_range = "60+"
            entry = m.get(age_map, age_range)
            if entry is None:
                m.put(age_map, age_range, edges_map_60_plus)
            if m.get(edges_map_60_plus, key) is None and m.get(edges_map_60_plus, inverse_key) is None:            
                value = 1
                m.put(edges_map_60_plus, key, value)
            elif m.get(edges_map_60_plus, key) != None or m.get(edges_map_60_plus, inverse_key):
                if m.get(edges_map_60_plus, key) is None:
                    entry = m.get(edges_map_60_plus, inverse_key)
                    value = me.getValue(entry)
                    value += 1
                    m.put(edges_map_60_plus, inverse_key, value)
                else:
                    entry = m.get(edges_map_60_plus, key)
                    value = me.getValue(entry)
                    value += 1
                    m.put(edges_map_60_plus, key, value)
    return citybike

def adjacents(analyzer, vertex):
    gr.adjacents(analyzer['graph'],vertex)

#Requerimiento 4

def adyacentes(analyzer, station, time:int):
    """
    Mira cuáles son los componentes conectados a la
    estación de inicio

    Args:
        analyzer (dict]): Datos grafo citybike
        station ([str]): Estación de partida
        time ([int]): Tiempo de duración

    Returns:
        [list]: Lista con las estaciones que cumplen el tiempo 
    """
    if gr.containsVertex(analyzer['graph'], station) == False:
        print('\nEsta parada no existe, pruebe con otra')
    else:
        initial_station = gr.adjacents(analyzer['graph'], station)  #Estacion adyacentes a la estación de inicio
        if initial_station['size'] == 0:
            print('\nLa ruta que selecciono no tiene estaciones adyacentes, pruebe con otra')            
        else:
            iterator = it.newIterator(initial_station)
            while it.hasNext(iterator):
                stations = it.next(iterator)
                time_weight = gr.getEdge(analyzer['graph'], station, stations)['weight'] #Peso de cada arco
                adjacents_st_st = gr.adjacents(analyzer['graph'], stations)
                if stations == station:                                                  #Filtro estación repetida 
                    None
                elif  adjacents_st_st['size'] == 0 and time_weight < time:               #Estaciones que no tienen adyacentes pero cumplen la condición
                    A = gr.getEdge(analyzer['graph'], station, stations)['vertexA']      #ID estación A
                    name_a = list(m.get(analyzer['names'], A).values())[1]               #Nombre estación A
                    B = gr.getEdge(analyzer['graph'], station, stations)['vertexB']      #ID estación B
                    name_b = list(m.get(analyzer['names'], B).values())[1]               #Nombre estación B
                    print('\n- '+'Se tiene un camino entre las siguientes estaciones: '+ str(A) + ' '+ '('+name_a+')'+
                        ' y '+ str(B) + ' ('+ name_b + ')' + ' con un tiempo de '+ str(time_weight)+ ' segundos.')
                elif adjacents_st_st['size'] != 0 and time_weight < time:                #Estaciones que tienen adyacentes que cumplen con el tiempo 
                    estacionrecursiva(analyzer, stations, time_weight, time)
        
    inifinstations(analyzer, station)

                   
def estacionrecursiva(analyzer, station, timestation, time):
    time_u = timestation
    initial_station = gr.adjacents(analyzer['graph'], station)
    iterator = it.newIterator(initial_station)
    while it.hasNext(iterator):
        stations = it.next(iterator)
        if stations == station:
            None
        elif time_u <= time:                           #Comprobación tiempo
            time_weight = gr.getEdge(analyzer['graph'], station, stations)['weight']            
            time_u += time_weight
            if time_u <=time:
                time_station = 0
                adjacents = gr.adjacents(analyzer['graph'], stations)['size']
                if adjacents == 0:
                    savestation = analyzer['stations']
                    existstation = m.contains(savestation, station)
                    if existstation:
                        entry = m.get(savestation, station)
                        stationss = me.getValue(entry)
                        time_station = time_u
                    else:
                        stationss = recursivestations(station)
                        m.put(savestation, station, stationss)
                        time_station = time_u
                    lt.addLast(stationss['adjacents'],(stations,time_station))
                    stationss['weight'] = time_u
                else: 
                    estacionrecursiva(analyzer, stations, time_u, time)
                    
            else:
                time_u = timestation


def inifinstations(analyzer,initial_station):
    """Obtiene las últimas estaciones de las estaciones 
    adyacentes que cumplen con los requerimientos

    Args:
        stations (dict): Diccionario con las estaciones adyacentes 
        initial_station (int): Estación de partida

    Returns:
        str,str: Retorna la estación inicial y final del recorrido
    """
    iterator = it.newIterator(m.valueSet(analyzer['stations']))
    while it.hasNext(iterator):
        stationss = it.next(iterator)['adjacents']
        iterator_2 = it.newIterator(stationss)
        while it.hasNext(iterator_2):
            stations_2 =it.next(iterator_2)    
            name_a = list(m.get(analyzer['names'], initial_station).values())[1] 
            name_b = list(m.get(analyzer['names'], stations_2[0]).values())[1] 
            print('\n- '+'Se tiene un camino entre las siguientes estaciones: '+ str(initial_station) + ' '+ '('+name_a+')'+
                    ' y '+ str(stations_2[0]) + ' ('+ name_b + ')' + ' con un tiempo de '+ str(stations_2[1])+ ' segundos.')
        
def namestation(analyzer, station):
    name = list(m.get(analyzer['names'], station).values())[1] 
    return name


#Requerimiento 5 

def newage(year):
    """
    Crea una estructura para modelar los id de las rutas según la 
    edad

    Args:
        year(str): Rango de años en que nació la persona 
    return:x
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
    lt.addLast(yearr['initialroute_id'], route_id['start station id'])
    lt.addLast(yearr['finalroute_id'], route_id['end station id'])
    
def iterartion(data):
    iterator= it.newIterator(data) 
    while it.hasNext(iterator):
        station = it.next(iterator)
        return station

def agesroutes(analyzer, agerange):
    ages = analyzer['trips']
    ages_k = m.keySet(analyzer['trips'])
    iterator= it.newIterator(ages_k) 
    L = []
    M = []
    if agerange == 1:
        while it.hasNext(iterator):
            age_k = it.next(iterator)
            if 0<= age_k <= 10:
                b = iterartion(m.get(ages, age_k)['value']['initialroute_id'])       
                c = iterartion(m.get(ages, age_k)['value']['finalroute_id'])
                L.append(b)
                M.append(c)
            else: 
                None
    elif agerange == 2:
        while it.hasNext(iterator):
            age_k = it.next(iterator)
            if 11<= age_k <= 20:
                b = iterartion(m.get(ages, age_k)['value']['initialroute_id'])       
                c = iterartion(m.get(ages, age_k)['value']['finalroute_id'])
                L.append(b)
                M.append(c)
            else: 
                None
    elif agerange == 3:
        while it.hasNext(iterator):
            age_k = it.next(iterator)
            if 21<= age_k <= 30:
                b = iterartion(m.get(ages, age_k)['value']['initialroute_id'])       
                c = iterartion(m.get(ages, age_k)['value']['finalroute_id'])
                L.append(b)
                M.append(c)
            else: 
                None
    elif agerange == 4:
        while it.hasNext(iterator):
            age_k = it.next(iterator)
            if 31<= age_k <= 40:   
                b = iterartion(m.get(ages, age_k)['value']['initialroute_id'])       
                c = iterartion(m.get(ages, age_k)['value']['finalroute_id'])
                L.append(b)
                M.append(c)
            else: 
                None        
    elif agerange == 5:
        while it.hasNext(iterator):
            age_k = it.next(iterator)
            if 41<= age_k <= 50:
                b = iterartion(m.get(ages, age_k)['value']['initialroute_id'])       
                c = iterartion(m.get(ages, age_k)['value']['finalroute_id'])
                L.append(b)
                M.append(c)
            else: 
                None
    elif agerange == 6:
        while it.hasNext(iterator):
            age_k = it.next(iterator)
            if 51<= age_k <= 60:
                b = iterartion(m.get(ages, age_k)['value']['initialroute_id'])       
                c = iterartion(m.get(ages, age_k)['value']['finalroute_id'])
                L.append(b)
                M.append(c)
            else: 
                None
    elif agerange == 7:
        while it.hasNext(iterator):
            age_k = it.next(iterator)
            if age_k>60:
                b = iterartion(m.get(ages, age_k)['value']['initialroute_id'])       
                c = iterartion(m.get(ages, age_k)['value']['finalroute_id'])
                L.append(b)
                M.append(c)
            else: 
                None
    else:
        None
    if L != []:
        inistation = Counter(L).most_common()[0][0]    #Estación de salida
        name_ini = list(m.get(analyzer['names'],inistation).values())[1]
    else:
        inistation = None
        name_ini = None
    if M != []:
        finalstation = Counter(M).most_common()[0][0]  #Estación de llegada 
        name_fin = list(m.get(analyzer['names'], finalstation).values())[1]
    else:
        finalstation = None
        name_fin = None          
    
    return inistation,finalstation, name_ini, name_fin
    
# ==============================
# Funciones de consulta.
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

def minimumCostPaths(analyzer,initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer['graph'], initialStation)
    return analyzer

def hasPath(analyzer,destStation):
    """
    Indica si existe un camino desde la estacion inicial a la estación destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    return djk.hasPathTo(analyzer['paths'], destStation)

def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path

def top_stations(analyzer, selector):
    graph = analyzer["graph"]
    top = lt.newList("SINGLE_LINKED", top_cmpfunction)
    lst = gr.vertices(graph)
    lst["cmpfunction"] = lst_cmpfunction
    greatest = 0
    greatest_degree = 0
    counter = 0
    while counter < 3:
        iterator = it.newIterator(lst)
        while it.hasNext(iterator):
            vertex = it.next(iterator)
            if selector == "in":
                degree = gr.indegree(graph, vertex)
            elif selector == "out":
                degree = gr.outdegree(graph, vertex)
            if degree > greatest_degree:
                greatest = int(vertex)
                greatest_degree = degree 
        lt.addLast(top, greatest)
        pos = lt.isPresent(lst, str(greatest))
        lt.deleteElement(lst, pos)
        greatest_degree = 0
        counter += 1 
    first_entry = m.get(analyzer["station_names"], str(lt.removeFirst(top)))
    first = me.getValue(first_entry)
    second_entry = m.get(analyzer["station_names"], str(lt.removeFirst(top)))
    second = me.getValue(second_entry)
    third_entry = m.get(analyzer["station_names"], str(lt.removeFirst(top)))
    third = me.getValue(third_entry)
    return first, second, third

def low_stations(analyzer):
    graph = analyzer["graph"]
    low_top = lt.newList("SINGLE_LINKED", top_cmpfunction)
    lst = gr.vertices(graph)
    lst["cmpfunction"] = lst_cmpfunction
    lowest = 0
    lowest_degree = gr.numEdges(graph)
    counter = 0
    while counter < 3:
        iterator = it.newIterator(lst)
        while it.hasNext(iterator):
            vertex = it.next(iterator)
            in_degree = gr.indegree(graph, vertex)
            out_degree = gr.outdegree(graph, vertex)
            degree = in_degree + out_degree
            if degree < lowest_degree:
                lowest = int(vertex)
                lowest_degree = degree 
        lt.addLast(low_top, lowest)
        pos = lt.isPresent(lst, str(lowest))
        lt.deleteElement(lst, pos)
        lowest_degree = gr.numEdges(graph)
        counter += 1 
    first_entry = m.get(analyzer["station_names"], str(lt.removeFirst(low_top)))
    first = me.getValue(first_entry)
    second_entry = m.get(analyzer["station_names"], str(lt.removeFirst(low_top)))
    second = me.getValue(second_entry)
    third_entry = m.get(analyzer["station_names"], str(lt.removeFirst(low_top)))
    third = me.getValue(third_entry)
    return first, second, third
    
def most_used_stations_by_age_range(citybike, age_range):
    age_map = citybike["age_range"]
    lst = lt.newList()
    selected_entry = m.get(age_map, age_range)
    selected_map = me.getValue(selected_entry)
    selected_map_keys = m.keySet(selected_map)
    iterator = it.newIterator(selected_map_keys)
    greatest = 0
    second = 0
    while it.hasNext(iterator):
        stations_id = it.next(iterator)
        entry = m.get(selected_map, stations_id)
        if me.getValue(entry) > greatest:
            greatest_key = me.getKey(entry)
            greatest = me.getValue(entry)
        if me.getValue(entry) > second and me.getValue(entry) <= greatest:
            second_key = me.getKey(entry)
            second = me.getValue(entry)
    value = greatest
    greatest_pos = lt.isPresent(selected_map_keys, greatest_key)
    second_pos = lt.isPresent(selected_map_keys, second_key)
    lt.deleteElement(selected_map_keys, greatest_pos)
    lt.deleteElement(selected_map_keys, second_pos)
    station_names = citybike["station_names"]
    ids_0 = greatest_key.split("+")
    ids_1 = second_key.split("+")
    key_0 = m.get(station_names, ids_0[0])["value"]
    key_1 = m.get(station_names, ids_0[1])["value"]
    key_2 = m.get(station_names, ids_1[0])["value"]
    key_3 = m.get(station_names, ids_1[1])["value"]
    pareja_1 = key_0 + " y " + key_1
    pareja_2 = key_2 + " y " + key_3
    lt.addFirst(lst, pareja_1)
    if greatest != second:
        lt.addFirst(lst, pareja_2)
    if greatest == second:
        iterator = it.newIterator(selected_map_keys) 
        while it.hasNext(iterator):
            entry = m.get(selected_map, it.next(iterator))
            if me.getValue(entry) == greatest:
                key_4 = m.get(citybike["station_names"], it.next(iterator).split("+")[0])["value"]
                key_5 = m.get(citybike["station_names"], it.next(iterator).split("+")[1])["value"]
                pareja_3 = key_4 + " y " + key_5
                lt.addFirst(lst, pareja_3)
    return lst, value
# ==============================
# Funciones Helper.
# ==============================

# ==============================
# Funciones de Comparación.
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
def compareStopsIds(stop, keyvaluestop):
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0 
    elif (stop > stopcode):
        return 1
    else:
        return -1

def lst_cmpfunction(station_1, station_2):
    station_1 = int(station_1)
    station_2 = int(station_2)
    if station_1 == station_2:
        return 0
    elif station_1 > station_2:
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

def top_cmpfunction(station_1, station_2):
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

def compare_maps(map1, map2):
    if map1 == map2["key"]:
        return 0
    elif map1 > map2["key"]:
        return 1
    else:
        return -1

def compare_keys(key1, key2):
    if key1 == key2:
        return 0
    elif key1 > key2:
        return 1
    else:
        return -1

def compare_map_keys(key1, key2):
    if type(key2) is not str:
        if key1 == key2["key"]:
            return 0
        elif key1 > key2["key"]:
            return 1
        else:
            return -1
    else:
        if key1 == key2:
            return 0
        elif key1 > key2:
            return 1
        else:
            return -1