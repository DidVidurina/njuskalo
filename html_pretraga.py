import time
import html
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

<<<<<<< Updated upstream
print("tes1t")
=======
print("test3")
>>>>>>> Stashed changes
print("test3")



service = Service("C:/Users/DELL/Desktop/chrome/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get(URL)

soup = BeautifulSoup(driver.page_source, 'html.parser')
print("we up")

URL = 'https://www.njuskalo.hr/prodaja-kuca/bjelovar'

current_url = driver.current_url

soup = BeautifulSoup(driver.page_source, 'html.parser')


print(soup.html)


