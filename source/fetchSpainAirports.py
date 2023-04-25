import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unicodedata import normalize
import json
import time
from googlesearch import search

from bs4 import BeautifulSoup

# Clase para tener relacionado el código IATA y el nombre del aeropuerto
class Airports: 
    def __init__(self, nombre, IATA):
        self.nombre = nombre
        self.IATA = IATA
    
    def getIATA(self,):
        return self.IATA
    
    def getNombre(self,):
        return self.nombre

# RECUPERAR LA TABLA CON LOS AREROPUERTOS DE ESPAÑA DE LA WIKIPEDIA
def get_airports():
    url = "https://es.wikipedia.org/wiki/Anexo:Aeropuertos_de_España"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # BUSCAMOS LA SEGUNDA TABLA DEL DOCUMENTO HTML, QUE ES DONDE SE ENCUENTRA LA TABLA DESEADA
    table_index = 1
    table = soup.find_all('table')[table_index]

    # BUSCAMOS TODAS LAS ETIQUETAS "TR", YA QUE NOS DAN LAS FILAS DE LA TABLA
    trow = table.find_all('tr')

    rowIndex = 0 
    header_elements = []
    AirportsVector = []
    IATAindex = 0 
    AeropuertoIndex = 0
    for row in trow:
        # HEADER
        if rowIndex == 0:
            title_row = row.find_all('th')
            count = 0
            for title in title_row:
                titleText = title.get_text()
                if titleText != "\n":
                    print(titleText.strip())
                    header_elements.append(titleText.strip())
                    # ENCONTRAR EL INDICE DONDE SE ENCUENTRA IATA EN LA CABECERA
                    if titleText.strip() == "IATA":
                        IATAindex = count
                    # ENCONTRAR EL INDICE DONDE SE ENCUENTRA EL NOMBRE DEL AEROPUERTO EN LA CABECERA
                    if titleText.strip() == "Aeropuertos públicos":
                        AeropuertoIndex = count
                    count += 1
        # TODAS LAS OTRAS FILAS
        else:
            # BUSCAMOS LOS ELEMENTOS CON LA ETIQUETA TD
            tds = row.find_all('td')
            IATA_element = ""
            aeropuerto_element = ""

            # ENCONTRAMOS EL CÓDIGO IATA EN CADA FILA
            if len(tds) > IATAindex + 1:
                IATA_element = tds[IATAindex].getText().strip()

            # ENCONTRAMOS EL NOMBRE DEL AEROPUERTO EN CADA FILA
            if len(tds) > AeropuertoIndex + 1:
                aeropuerto_element = tds[AeropuertoIndex].getText().strip()
            if IATA_element != "" and aeropuerto_element != "":
                AirportsVector.append(Airports(nombre=aeropuerto_element, IATA=IATA_element))
        rowIndex += 1

    # GUARDAMOS TODOS LOS DATOS EN FORMATO JSON
    data = {airport.IATA: airport.nombre for airport in AirportsVector}

    #ESCRIBIMOS LOS DATOS DENTRO DE UN FICHERO JSON PARA QUE PUEDA SER UTILIZADO EN OTRAS PARTES DEL PROGRAMA
    with open("./source/spainTable.json", "wb") as f:
        f.write(json.dumps(data,ensure_ascii=False).encode('utf-8'))
    return data


