import pandas as pd
from find_flight import search_flights
from fetchWeb import fetch_airlines
from fetchSpainAirports import get_airports
#from json import load
import os

if __name__=="__main__":
    #Recupera todos los destinos que se pueden volar desde Madrid
    destinos = fetch_airlines()
    #Recupera todos los aeropuertos de España con su codigo IATA
    aeropuertos = get_airports()
    #Crea un dataset con todos los vuelos desde Madrid a los destinos
    dataset = pd.DataFrame(columns=['airline', 'price', 'duration', 'stops', 'departure', 'arrival','returns','datetime','from','to'])
    for dest in destinos:
        if dest in aeropuertos:
            #Genera la busqueda en google flights
            busqueda = 'vuelos madrid '+aeropuertos[dest].replace('Airport','')
            dataset = dataset.append(search_flights(busqueda),ignore_index=True)
    #Si no esta creado el archivo lo crea, si no lo añade al final
    if not os.path.isfile('./dataset/flights.csv'):
        dataset.to_csv('./dataset/flights.csv',index=False)
    else: 
        dataset.to_csv('./dataset/flights.csv',mode='a',header=False,index=False)