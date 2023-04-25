import pandas as pd
from find_flight import search_flights
from fetchWeb import fetch_airlines
from fetchSpainAirports import get_airports
from json import load
import os

if __name__=="__main__":
    destinos = fetch_airlines()
    aeropuertos = get_airports()
    dataset = pd.DataFrame(columns=['airline', 'price', 'duration', 'stops', 'departure', 'arrival','returns','datetime','from','to'])
    for dest in destinos:
        if dest in aeropuertos:
            busqueda = 'vuelos madrid '+aeropuertos[dest].replace('Airport','')
            dataset = dataset.append(search_flights(busqueda),ignore_index=True)
    if not os.path.isfile('./dataset/flights.csv'):
        dataset.to_csv('./dataset/flights.csv',index=False)
    else: 
        dataset.to_csv('./dataset/flights.csv',mode='a',header=False,index=False)