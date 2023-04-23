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
    def __init__(self, sobrenombre, IATA):
        self.sobrenombre = sobrenombre
        self.IATA = IATA
    
    def getIATA():
        return self.IATA
    
    def getSobrenombre():
        return self.sobrenombre

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
SobrenombreIndex = 0
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
                # FIND FOR SOBRENOMBRE INDEX
                if titleText.strip() == "Sobrenombre":
                    SobrenombreIndex = count
                count += 1
    else:
        tds = row.find_all('td')
        IATA_element = ""
        sobrenombre_element = ""
        if len(tds) > IATAindex + 1:
            IATA_element = tds[IATAindex].getText().strip()
        if len(tds) > SobrenombreIndex + 1:
            sobrenombre_element = tds[SobrenombreIndex].getText().strip()
        if IATA_element != "" and sobrenombre_element != "":
            AirportsVector.append(Airports(sobrenombre=sobrenombre_element, IATA=IATA_element))
    rowIndex += 1
# Print the thead and tbody as HTML strings



lengthVector = len(AirportsVector)

string = ""

data = {airport.IATA: airport.sobrenombre + " airport" for airport in AirportsVector}

print (data)

with open("./source/spainTable.json", "w", encoding ='utf-8') as f:
    json.dump(data, f, ensure_ascii= True )


