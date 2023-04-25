import requests
import json
from bs4 import BeautifulSoup

# CLASE PARA RELACIONAR LA AEROLINEA CON EL DESTINO
class Airlines: 
    def __init__(self, airline, destinations):
        self.airline = airline
        self.destinations = destinations
    
    def getAirline(self,):
        return self.airline
    
    def getDestinations(self,):
        return self.destinations

# BUSCAMOS LA AEROLÍNEAS QUE OPERAN EN EL AEROPUERTO DE MADRID-BARAJAS
def fetch_airlines():

    url = "https://www.aena.es/es/adolfo-suarez-madrid-barajas/aerolineas-y-destinos/aerolineas.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # BUSCAMOS EL ELEMENTO "ARTICLE" YA QUE LA TABLA DESEADA ES EN REALIDAD ESTE ELEMENTO
    articles = soup.find_all('article', attrs={'role': 'table'})

    airlines = []
    #DEFINIMOS AQUELLAS PALABRAS QUE NO QUEREMOS QUE SALGAN EN NUESTRA BASE DE DATOS
    unwanted_words = ['Compañía Aérea', 'Terminal', 'destinos', 'DETALLES', 'T1', 'T2', 'T3', 'T4', "CompañíaAerea:","-",":","  ","+"]

    for article in articles:
        # BUSCAMOS TODAS LAS FILAS DEL ARTICULO.
        lis = article.find_all('li')
        #ELIMINAMOS TODOS LOS SEPARADORES, COMO TABULACIONES E INTROS PARA LAS AEROLÍNEAS. 
        airline_name = lis[0].text.strip().replace('\t', '').replace('\r', '').replace('\n', '')
        # ELIMINAMOS TODAS LAS PALABRAS INDESEADAS PARA LAS AEROLÍNEAS
        for word in unwanted_words:
            airline_name = airline_name.replace(word, '').strip()

        # ELIMINAR LOS SEPRADORES, COMO TABULACIONES E INTROS PARA LOS DESTINOS. 
        destinations = [li.text.strip().replace('\t', '').replace('\r', '').replace('\n', '') for li in lis[1:]]
        # ELIMINAMOS TODAS LAS PALABRAS INDESEADAS PARA LOS DESTINOS
        for i, destination in enumerate(destinations):
            for word in unwanted_words:
                destinations[i] = destinations[i].replace(word, '').strip()

        #AÑADIMOS LOS DATOS QUE NOS INTERSAN DENTRO DEL VECTOR
        airlines.append({
            'airline': airline_name,
            'destinations': destinations
        })

    # FORMATEAMOS LA RESPUESTA QUE NOS LLEGA
    formatted_response = ""
    response = []
    inDestinos = False
    airlineTMP = ""
    destinosTMP = []
    airlinesVector = []

    # BUSCAMOS POR AEROLINEA
    for airline in airlines:
        for destination in airline['destinations']:
            if destination != '' and destination != "Destinos":
                dest = destination.split("Destinos")
                if len(dest) > 1:
                    inDestinos = True
                else:
                    inDestinos = False
                    if airlineTMP != "" and len(destinosTMP) > 0:
                        # GUARDAMOS LOS ELEMENTOS QUE HEMOS ENCONTRADO EN UN VECTOR
                        airlinesVector.append(Airlines(airlineTMP, destinosTMP))
                        destinosTMP = []
                        airlineTMP = ""
                    airlineTMP = destination

                if inDestinos:
                    dest_parentesis = dest[1].split("(")
                    for split in dest_parentesis:
                        if len(split.split(")")) > 1:
                            destinosTMP.append(split.split(")")[0])
        
        # CUANDO FINALIZAMOS EL RECORRIDO JUNTAMOS TODA LA RESPUESTA
        formatted_response += "\n".join([f"{destination}" for destination in airline['destinations']])


    # DEVOLVEMOS UN VECTOR CON LAS AEROLÍNEAS Y DESTINOS PARA SER USADO EN OTRA PARTE DEL PROGRAMA
    result = []
    for airline in airlinesVector:
        aux = set(result)
        diff = set(airline.destinations) - aux
        result = result + list(diff)
    return result



