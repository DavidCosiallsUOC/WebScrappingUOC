import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unicodedata import normalize
import json
import time
from googlesearch import search

from bs4 import BeautifulSoup

#plt.use('Agg')

class Airports: 
    def __init__(self, location, IATA):
        self.location = location
        self.IATA = IATA
    
    def getIATA():
        return self.IATA
    
    def getLocation():
        return self.location

url = "https://es.wikipedia.org/wiki/Anexo:Aeropuertos_de_España"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the second table on the page (index 1)
table_index = 1
table = soup.find_all('table')[table_index]

# Extract the thead and tbody elements from the table
trow = table.find_all('tr')

col = []
rowIndex = 0
header_elements = []
AirportsVector = []
IATAindex = 0
LocationIndex = 0
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
                # FIND FOR IATA INDEX
                if titleText.strip() == "IATA":
                    IATAindex = count
                # FIND FOR LOCATION INDEX
                if titleText.strip() == "Localización":
                    LocationIndex = count
                count += 1
    else:
        tds = row.find_all('td')
        IATA_element = ""
        Location_element = ""
        if len(tds) > IATAindex + 1:
            #IATA_elements.append(tds[IATAindex].getText().strip()) 
            IATA_element = tds[IATAindex].getText().strip()
        if len(tds) > LocationIndex + 1:
            #Location_elements.append(tds[LocationIndex].getText().strip()) 
            Location_element = tds[LocationIndex].getText().strip()
        if IATA_element != "" and Location_element != "":
            AirportsVector.append(Airports(location=Location_element, IATA=IATA_element))
    rowIndex += 1
# Print the thead and tbody as HTML strings

JSONvector = []

for aiport in AirportsVector:
    data = {
        "location": aiport.location,
        "IATA": aiport.IATA
    }
    JSONvector.append(data)


with open("spainTable.json", "w") as f:
    json.dump(JSONvector, f)

# Define the search query

# for airport in AirportsVector:
#     #query = airport.IATA + " coordinates"
#     query = airport.IATA+ " airport coordinates"
#     url = f"https://www.google.es/search?q={query}"

#     # Set the user agent to simulate a real user
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
#         "Cookie": "CONSENT=YES+ES.es+V16+BX"
#     }

#     # Send the GET request to the URL and get the HTML response
#     response = requests.get(url, headers=headers, cookies={})
#     soup = BeautifulSoup(response.content, "html.parser")
#     file = open("google.html", "w")
#     file.write(str(soup))
#     # Find the knowledge graph section and extract the coordinates
#     divs = soup.find_all("div")
#     coordinates_div = soup.find("div", {"class": "Z0LcW"})
#     if coordinates_div:
#         coordinates = coordinates_div.text
#         print(f"The coordinates of MAD airport are {coordinates}")
#     else:
#         print("Coordinates not found in knowledge graph")
    

#     time.sleep(15)

origin = "BCN"
destination = "MAD"

originYear = "2023"
originMonth = "04"
originDay = "23"
originDate = originYear+"-"+originMonth+"-"+originDay

destinationYear = "2023"
destinationMonth = "05"
destinationDay = "27"
destinationDate = destinationYear+"-"+destinationMonth+"-"+destinationDay

flightClass = "economy"
numberAdults = "1"

url = "https://vuelos-baratos.rastreator.com/?utm_source=rastreator&utm_medium=affiliate&utm_term=rev&utm_campaign=whitelabel&utm_content=CMSVuelos/#/flights/ABC-MAD/2023-04-23/2023-05-27/economy/1adults"

rastreatorUrl = "https://vuelos-baratos.rastreator.com/?utm_source=rastreator&utm_medium=affiliate&utm_term=rev&utm_campaign=whitelabel&utm_content=CMSVuelos/#/flights/{origin}-{destination}/{originDate}/{destinationDate}/{flightClass}/{numberAdults}adults"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

rastreatorFile = open("rastreator.html", "w")
rastreatorFile.write(str(soup))
