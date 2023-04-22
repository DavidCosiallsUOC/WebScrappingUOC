import pandas as pd
from find_flight import search_flights
from fetchWeb import fetch_airlines
from json import load

if __name__=="__main__":
    destinos = fetch_airlines()
    with open('./source/destinos_es.json',encoding='utf-8') as f:
        aeropuertos = load(f)
    dataset = pd.DataFrame(columns=['airline', 'price', 'duration', 'stops', 'departure', 'arrival','returns','datetime'])
    for dest in destinos:
        if dest in aeropuertos:
            busqueda = 'vuelos madrid '+aeropuertos[dest].replace('Airport','')
            dataset = dataset.append(search_flights(busqueda),ignore_index=True)
    dataset.to_csv('./dataset/flights.csv',index=False)