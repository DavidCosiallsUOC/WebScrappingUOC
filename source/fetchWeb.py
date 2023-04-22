import requests
import json
from bs4 import BeautifulSoup

class Airlines: 
    def __init__(self, airline, destinations):
        self.airline = airline
        self.destinations = destinations
    
    def getAirline(self,):
        return self.airline
    
    def getDestinations(self,):
        return self.destinations

def fetch_airlines():

    url = "https://www.aena.es/es/adolfo-suarez-madrid-barajas/aerolineas-y-destinos/aerolineas.html"
    response = requests.get(url)


    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all article elements with role attribute set to "table"
    articles = soup.find_all('article', attrs={'role': 'table'})

    # Create a list to store all the airlines
    airlines = []

    # Define a list of words to remove from airline names and destinations
    unwanted_words = ['Compañía Aérea', 'Terminal', 'destinos', 'DETALLES', 'T1', 'T2', 'T3', 'T4', "CompañíaAerea:","-",":","  ","+"]

    # Iterate over each article
    for article in articles:
        # Find all the <li> elements within the article
        lis = article.find_all('li')

        # Extract the airline name from the first <li> element
        airline_name = lis[0].text.strip().replace('\t', '').replace('\r', '').replace('\n', '')

        # Remove unwanted words from the airline name
        for word in unwanted_words:
            airline_name = airline_name.replace(word, '').strip()

        # Extract the destinations from the remaining <li> elements
        destinations = [li.text.strip().replace('\t', '').replace('\r', '').replace('\n', '') for li in lis[1:]]

        # Remove unwanted words from the destinations
        for i, destination in enumerate(destinations):
            for word in unwanted_words:
                destinations[i] = destinations[i].replace(word, '').strip()

        # Add the airline and its destinations to the list of airlines
        airlines.append({
            'airline': airline_name,
            'destinations': destinations
        })

    # Format the response
    formatted_response = ""
    response = []
    inDestinos = False
    airlineTMP = ""
    destinosTMP = []
    airlinesVector = []
    for airline in airlines:
        for destination in airline['destinations']:
            if destination != '' and destination != "Destinos":
                dest = destination.split("Destinos")
                if len(dest) > 1:
                    inDestinos = True
                else:
                    inDestinos = False
                    if airlineTMP != "" and len(destinosTMP) > 0:
                        airlinesVector.append(Airlines(airlineTMP, destinosTMP))
                        destinosTMP = []
                        airlineTMP = ""
                    airlineTMP = destination

                if inDestinos:
                    dest_parentesis = dest[1].split("(")
                    for split in dest_parentesis:
                        if len(split.split(")")) > 1:
                            destinosTMP.append(split.split(")")[0])
        
        formatted_response += "\n".join([f"{destination}" for destination in airline['destinations']]) #ANALIZAR CADA LÍNEA

    result = []
    for airline in airlinesVector:
        aux = set(result)
        diff = set(airline.destinations) - aux
        result = result + list(diff)
    return result



