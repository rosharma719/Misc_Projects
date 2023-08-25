import selenium
import requests
from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
stock = "AAPL"

options = webdriver.ChromeOptions()

options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options, executable_path='C:\\Users\\kragg\\Projects\\ChromeDriver\\chromedriver.exe')
driver.get(f"https://finance.yahoo.com/quote/{stock}/")
 
def pricefind():
    driver.refresh()
    time.sleep(1)
    content = driver.page_source
    soup = bs(content, features="lxml")
    div = soup.find('div', {'id': "quote-header-info"})
    div2 = div.find('div', {'class' : "D(ib) Va(m) Maw(65%) Ov(h)"})
    div3 = div2.find('div', {'class': 'D(ib) Mend(20px)'}) 
    fin_streamer = div3.find(['fin-streamer'], attrs={'class': "Fw(b) Fz(36px) Mb(-4px) D(ib)"})
    price = fin_streamer.get_text()
    return(price)

data = {
    'Time': [],
    'Price': []
}

try: 
    x = 0
    while x < 5:

        price = pricefind()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        data['Time'].append(current_time)
        data['Price'].append(price)
        print("Price at " + current_time + " is " + price)

        x +=1
        time.sleep(1)
    driver.close()
except selenium.common.exceptions.WebDriverException: 
    print("Webdriver error")
    driver.close()

pandata = pd.DataFrame.from_dict(data)
print(pandata)

pandata.to_csv('CSVExport\\pandata.csv')
