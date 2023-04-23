import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


def search_flights(search:str):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument('--incognito')

    driver = webdriver.Chrome(executable_path=r"./source/chromedrive_win32/chromedriver.exe",options=options)
    driver.get("https://www.google.com/search?q="+search)
    wait = WebDriverWait(driver, 10)

    lang = driver.find_element(by=By.XPATH, value='//html')
    lang = lang.get_attribute('lang')
    if lang == 'es':
        accept_cookies_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(),"Aceptar todo")]/ancestor::button')))
    elif lang=='en':
        accept_cookies_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(),"Accept all")]/ancestor::button')))
    elif lang=='ca':
        accept_cookies_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(),"Accepta-ho tot")]/ancestor::button')))
    else:
        raise Exception("Language not supported")

    accept_cookies_button.click()

    flight_btn = driver.find_element(by=By.XPATH, value='//g-more-link')
    flight_btn.click()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "XsapA")))
    more_btn = driver.find_element(by=By.CLASS_NAME, value="XsapA")
    more_btn.click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//li')))
    time.sleep(10)
    flight_table = driver.find_elements(by=By.XPATH, value='//li')
    dataset = pd.DataFrame(columns=['airline', 'price', 'duration', 'stops', 'departure', 'arrival','returns','datetime'])
    date = datetime.datetime.now().isoformat()
    for flight in flight_table: 
        if 'Renfe' not in flight.text:
            aux = flight.text.split('\n')
            if len(aux)>1:
                try:
                    departure = aux[0]
                    arrival = aux[2]
                    airline = aux[3]
                    duration = aux[4]
                    stops = aux[6]
                    if aux[-1]=="Precio no disponible":
                        price = aux[-1]
                        returns = "No disponible"
                    else:    
                        price = aux[-2]
                        returns = aux[-1]
                    dataset = dataset.append({'airline': airline, 'price': price, 'duration': duration, 'stops': stops, 'departure': departure, 'arrival': arrival,'returns':returns,'datetime':date},ignore_index=True)
                except Exception as e:
                    print(str(e))
                    print(aux)
    # Cerrar el navegador
    driver.quit()
    return dataset
