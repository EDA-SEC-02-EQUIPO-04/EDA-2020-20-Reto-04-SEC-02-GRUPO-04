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
 """

import config as cf
from App import model
import csv

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
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def loadServices(analyzer, servicesfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    servicesfile = cf.data_dir + servicesfile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    lastservice = None
    for service in input_file:
        if lastservice is not None:
            sameservice = lastservice['ServiceNo'] == service['ServiceNo']
            samedirection = lastservice['Direction'] == service['Direction']
            if sameservice and samedirection:
                model.addStopConnection(analyzer, lastservice, service)
        lastservice = service
    model.addRouteConnections(analyzer)
    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def totalStops(analyzer):
    """
    """
    return model.totalStops(analyzer)


def totalConnections(analyzer):
    """
    """
    return model.totalConnections(analyzer)


def connectedComponents(analyzer):
    """
    """
    return model.connectedComponents(analyzer)


def minimumCostPaths(analyzer, initialStation):
    """
    """
    return model.minimumCostPaths(analyzer, initialStation)


def hasPath(analyzer, destStation):
    """
    """
    return model.hasPath(analyzer, destStation)


def minimumCostPath(analyzer, destStation):
    """
    """
    return model.minimumCostPath(analyzer, destStation)
