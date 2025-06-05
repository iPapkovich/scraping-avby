from selenium import webdriver
from selenium_stealth import stealth
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from curl_cffi import requests
import time
from datetime import datetime
import json

car_urls = []
CARIDS = []
CARGENERATIONS = []
CARDATA = []


page = 1
global i

def init_webdriver():
    driver = webdriver.Chrome()
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)
    #driver.minimize_window()
    return driver

def get_mainpage_cards(driver, url):
    driver.get(url)
    allscrolldown(driver)
    
    main_page_html = BeautifulSoup(driver.page_source, "html.parser")

    while True:
        content = main_page_html.find_all("a", {"class": "listing-item__link"})
        
        
        for link in content:
                href = link.get('href')
                if href:
                    # Извлекаем ID из URL (пример: /12345678)
                    CARID = href.split('/')[-1]
                    CARIDS.append(CARID)

                    #CARGENERATION = href.split('/')[-2]
                    #CARGENERATIONS.append(CARGENERATION)

                    CARDATA.append([href.split('/')[-1],CARBRAND,CARMODEL])

                    car_url = urlCar.rsplit('/',1)[0]+'/'+CARID
                    car_urls.append(car_url)
                    
                    print(f"Найдено ID: {CARID}")
                    

        print(f"Страница обработана. Найдено ID: {len(CARIDS)}")
        break



def allscrolldown(driver):
    i=0
    while i < 15:
        driver.execute_script('window.scrollBy(0,600)')
        time.sleep(0.5)
        try:
            # Ожидаем появления ссылки и кликаем
            link = WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.LINK_TEXT, "Показать ещё")))
            link.click()
            
            i=0
            print("Успешный клик!") 
            print(i)
            time.sleep(2)
            
        except :
            print("Не нашел")
        i+=1
        print(i)

urlCar = 'https://cars.av.by/opel/corsa/c-2000-2003' 


#urlCar = 'https://cars.av.by/bmw/3-seriya/e90-e91-e92-e93-2005-2010'
#urlCar = 'https://cars.av.by/bmw/3-seriya/e90-e91-e92e93-2008-2014-restajling'

CARMODEL = urlCar.split('/')[-1].upper()
CARBRAND = urlCar.split('/')[-2].upper()


if __name__ == "__main__":
    driver = init_webdriver()
    get_mainpage_cards(driver, urlCar)
    driver.quit()

print(car_urls)

#print(CARIDS)
#print(CARBRANDS)
#print(CARMODELS)
print(CARDATA)
#print(CARGENERATIONS)

now = datetime.now()

with open(f"JSON_DIR/SOURCE_DIR/{CARBRAND}_{CARMODEL}_DATA_{now.strftime('%Y_%m_%d_AT_%H_%M')}.json", "w") as f:
    json.dump(CARDATA, f)  # Сохраняем в JSON

