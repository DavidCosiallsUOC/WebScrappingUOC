import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unicodedata import normalize
import json

from bs4 import BeautifulSoup

url = "https://www.aena.es/es/adolfo-suarez-madrid-barajas/aerolineas-y-destinos/aerolineas.html"
response = requests.get(url)

with open("listaDeVuelos.html", "w") as file:
    file.write(response.text)

with open('listaDeVuelos.html') as file:
    html = file.read()

soup = BeautifulSoup(html, 'html.parser')
class_to_find = ['tabla','cuatro-col','h6','tag-result']

for article in soup.find_all('article'):
    article_class = article.get('class')
    article_role = article.get('role')
    article_content = article.get_text()
    #if article_role == "table":
        #print(f'Article class: {article_class}\nRole: {article_role}\n')
    #if article_class == class_to_find:  
        #print(f'Article id: {article_class}\nRole: {article_role}\n')



url = 'https://www.aena.es/es/adolfo-suarez-madrid-barajas/aerolineas-y-destinos/aerolineas.html'

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


class Airlines: 
    def __init__(self, airline, destinations):
        self.airline = airline
        self.destinations = destinations
    
    def getAirline():
        return self.airline
    
    def getDestinations():
        return self.destinations


inDestinos = False
airlineTMP = ""
destinosTMP = []
airlinesVector = []
for airline in airlines:
   
    for destination in airline['destinations']:
        #print(destination)
        if destination != '' and destination != "Destinos":
            dest = destination.split("Destinos")
            #print(dest)
            if len(dest) > 1:
                inDestinos = True
            else:
                #print(airlineTMP)
                inDestinos = False
                if airlineTMP != "" and len(destinosTMP) > 0:
                    airlinesVector.append(Airlines(airlineTMP, destinosTMP))
                    destinosTMP = []
                    airlineTMP = ""
                airlineTMP = destination

            if inDestinos:
                dest_parentesis = dest[1].split("(")
                #print(dest_parentesis)
                for split in dest_parentesis:
                    if len(split.split(")")) > 1:
                         destinosTMP.append(split.split(")")[0])
                         #print(destinosTMP)
    
    formatted_response += "\n".join([f"{destination}" for destination in airline['destinations']]) #ANALIZAR CADA LÍNEA
    
# Print the formatted response
#print(formatted_response)

JSONvector = []

for airline in airlinesVector:
    data = {
        "airline": airline.airline,
        "destinos": airline.destinations
    }
    JSONvector.append(data)
    #print("airline: ", airline.airline)
    #print("destinos: ", airline.destinations)
    #print("\n")
#print(airlinesVector)

with open("airlines.json", "w") as f:
    json.dump(JSONvector, f)


