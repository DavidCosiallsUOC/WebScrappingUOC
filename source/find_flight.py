import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


def search_flights(search:str):
    # Primer paso es abrir el navegador con las opciones qu necesitemos, en este caso, incognito y sin extensiones
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument('--incognito')

    driver = webdriver.Chrome(executable_path=r"./source/chromedrive_win32/chromedriver.exe",options=options)
    # Una vez abierto el navegador, vamos a la página de google
    driver.get("https://www.google.com/search?q="+search)
    wait = WebDriverWait(driver, 10)
    # Necesitamos saber en que idioma está la página para poder aceptar las cookies
    lang = driver.find_element(by=By.XPATH, value='//html')
    lang = lang.get_attribute('lang')
    if lang == 'es':
        accept_cookies_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(),"Aceptar todo")]/ancestor::button')))
    elif lang=='en-ES' or lang=='en':
        accept_cookies_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(),"Accept all")]/ancestor::button')))
    elif lang=='ca':
        accept_cookies_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(),"Accepta-ho tot")]/ancestor::button')))
    else:
        raise Exception("Language not supported")
    # Una vez encontramos el botón para aceptar las cookies, lo pulsamos
    accept_cookies_button.click()
    # El siguiente paso es acceder a la pagina del comparador de vuelos de google
    flight_btn = driver.find_element(by=By.XPATH, value='//g-more-link')
    flight_btn.click()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "XsapA")))
    # Por defecto google nos muestra los vuelos más baratos, pero si queremos ver los vuelos más rápidos, tenemos que pulsar el botón de "Más opciones"
    more_btn = driver.find_element(by=By.CLASS_NAME, value="XsapA")
    more_btn.click()
    # Una vez pulsado el botón, tenemos que esperar a que se cargue la página y que se muestren las opciones. Luego ya podemos recuperar la lista de vuelos
    wait.until(EC.presence_of_element_located((By.XPATH, '//li')))
    time.sleep(10)
    flight_table = driver.find_elements(by=By.XPATH, value='//li')
    # Creamos un dataframe para almacenar los datos de los vuelos
    dataset = pd.DataFrame(columns=['airline', 'price', 'duration', 'stops', 'departure', 'arrival','returns','datetime','from','to'])
    # Guardamos la fecha y hora de la búsqueda
    date = datetime.datetime.now().isoformat()
    from_city = search.split(' ')[1]  
    to_city =  ' '.join(search.split(' ')[2:])
    # Recorremos la lista de vuelos y extraemos los datos que nos interesan
    for flight in flight_table: 
        # Quitamos las recomendaciones de tren
        if 'Renfe' not in flight.text:
            aux = flight.text.split('\n')
            # Descartamos los casos en los que no haya datos disponibles
            if len(aux)>1:
                try:
                    departure = aux[0]
                    arrival = aux[2]
                    airline = aux[3]
                    duration = aux[4]
                    stops = aux[6]
                    # En algunos casos, el precio no está disponible, por lo que tenemos que tratarlo de forma diferente
                    if aux[-1]=="Precio no disponible":
                        price = aux[-1]
                        returns = "No disponible"
                    else:    
                        price = aux[-2]
                        returns = aux[-1]
                    # Añadimos los datos a nuestro dataframe
                    dataset = dataset.append({'airline': airline, 'price': price, 'duration': duration, 'stops': stops, 'departure': departure, 'arrival': arrival,'returns':returns,'datetime':date,'from':from_city,'to':to_city},ignore_index=True)
                except Exception as e:
                    print(str(e))
                    print(aux)
    # Cerramos el navegador
    driver.quit()
    return dataset
