import time
import math
import locale
import html
import json
import pandas as pd
import selenium.common.exceptions
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, \
    StaleElementReferenceException, TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


locale.setlocale(locale.LC_ALL, 'en_US')

URL = 'https://www.njuskalo.hr/'



service = Service("C:/Users/DELL/Desktop/chrome/chromedriver.exe")

options = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("--disable-web-security")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-infobars")
options.add_argument("--disable-popup-blocking")
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")

capabilities = {'pageLoadStrategy': 'none'}
driver = webdriver.Chrome(options=options, desired_capabilities=capabilities)
driver.get(URL)

soup = BeautifulSoup(driver.page_source, 'html.parser')

actions = ActionChains(driver)

time.sleep(5)

def format_item(item):
    formatted_item = item.replace("Č", "c").replace("Ć", "c").replace("Ž", "z").replace("Đ", "d") \
        .replace("Š", "s").replace("č", "c").replace("ć", "c").replace("ž", "z").replace("đ", "d") \
        .replace("š", "s").replace('²','2')
    return(formatted_item)
def accept_cookies():
    accept_cookies =WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH,'//*[@id="didomi-notice-agree-button"]'))
    )
    accept_cookies.click()
def razumijem():
    try:
        razumijem_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="pb-app"]/div[5]/div[1]/div[2]/button'))
        )
        razumijem_btn.click()
    except TimeoutException:
        pass
def get_real_estate_section():
    real_estate = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,'//*[@id="pb-app"]/div[4]/div[2]/div/div/main/div/div/div/nav/ul/li[2]/a'))
    )
    time.sleep(5)
    real_estate.click()
    time.sleep(5)
    time.sleep(5)
    razumijem()
    houses = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.XPATH,
                                    '//*[@id="pb-app"]/div[4]/div[2]/div[3]/div[1]/main/div/div[1]/div/nav/ul/li[1]/div/ul/li[1]/a/div'))
    )

    houses.click()
def get_counties():
    counties = driver.find_elements(By.CLASS_NAME, 'CategoryListing-topCategoryItem')
    counties_dict = {}
    for item in counties:
        if 'EU' in item.text:
            continue
        counties_dict[item.text.split()[0]] = item
    return counties_dict
def get_town_names():
    time.sleep(5)
    town_names_by_county = {}
    #try:
    #    advert = driver.find_element(By.XPATH, '//*[@id="ocm-st"]/ost/ost[1]/div/div')
    #    advert.click()
    #except NoSuchElementException or ElementNotInteractableException:
    #    print("Advert not found")
    try:
        open_menu = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="GeoLocationSelector-geo-wrap"]/div/div/div/div[2]/div/div/div[1]/div'))
        )
        driver.execute_script('arguments[0].scrollIntoView(true)', open_menu)
        time.sleep(5)
        open_menu.click()
    except StaleElementReferenceException:
        print("staleeeee")

        advertisement = EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[2]/button/div[1]'))
        advertisement.click()
        open_menu = driver.find_element(By.XPATH,'//*[@id="GeoLocationSelector-geo-wrap"]/div/div/div/div[2]/div/div/div[1]/div')
        open_menu.click()

    cities = driver.find_elements(By.XPATH,
                                  '//*[@id="GeoLocationSelector-geo-wrap"]/div/div/div/div[2]/div/div/div[2]/ul/ul/li')
    return cities
def get_towns(counties):
    counties_and_towns_dict = {}
    for item in counties:
        url_ending = item.replace('č', 'c').replace('ć', 'c').replace('đ', 'd').replace('š', 's').replace\
                    ('Istarska','istra').replace('ž','z').replace('Ž','ž').replace('Š','S').replace('Medimurska','medimurje').replace('Grad','zagreb')
        if url_ending == 'Grad Zagreb':
            continue
        else:
            current_url = f'https://www.njuskalo.hr/prodaja-kuca/{url_ending}'
            driver.get(current_url)
            towns = get_town_names()
            towns_text = []
            for item in towns:
                towns_text.append(item.text)
            counties_and_towns_dict[towns_text[0]] = towns_text

    return counties_and_towns_dict
def format_towns(towns_dic):
    for key in towns_dic:
        formatted_key = key.replace("Č", "c").replace("Ć", "c").replace("Ž", "z").replace("Đ", "d") \
            .replace("Š", "s").replace("č", "c").replace("ć", "c").replace("ž", "z").replace("đ", "d") \
            .replace("š", "s")
        key = formatted_key
    for item in towns_dic.values():
        for index, string in enumerate(item):
            formatted_item = string.replace("Č", "c").replace("Ć", "c").replace("Ž", "z").replace("Đ", "d") \
                .replace("Š", "s").replace("č", "c").replace("ć", "c").replace("ž", "z").replace("đ", "d") \
                .replace("š", "s")
            item[index] = formatted_item

    file_path = 'all_towns.json'
    with open(file_path, 'w') as json_file:
        json.dump(towns_dic, json_file)
def create_urls_dic():
    with open('all_towns.json', 'r') as file:
        dic = json.load(file)
    new_dict = {}
    for lst in dic.values():
        sub_dict = {}
        for i, item in enumerate(lst[1:]):
            sub_dict[item] = {'url': 'url', 'is_correct': 'is_correct','house_count':'house_count'}
        new_dict[lst[0]] = sub_dict
    return(new_dict)
def get_town_count(urls_dic):
    with open('all_towns_with_url_completion.json', 'r') as file:
        completion = json.load(file)
        for key in completion:
            print(key)
    all_towns_with_url_completion = {}
    for county,towns in urls_dic.items():
        if county in completion:
            continue

        county_complete = False
        key = county
        value = county_complete
        all_towns_with_url_completion[key] = value

        for town in urls_dic[county]:
            original_town = town
            letter = '-'
            if letter in town:
                    town_altered = town.replace(' ', '')
                    current_url = f'https://www.njuskalo.hr/prodaja-kuca/{town_altered}'
            else:
                    town_altered = town.replace(' ','-')
                    current_url = f'https://www.njuskalo.hr/prodaja-kuca/{town_altered}'
            driver.get(current_url)
            try:
                    houses_count = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable(
                            (By.XPATH,'//*[@id="form_browse_detailed_search"]/div/div[1]/div[5]/header/div[1]/strong'))
                    )
                    urls_dic[county][town]['url'] = current_url
                    urls_dic[county][town]['is_correct'] = True
                    urls_dic[county][town]['house_count'] = houses_count.text
            except (StaleElementReferenceException, WebDriverException, TimeoutException,selenium.common.exceptions.TimeoutException):
                    time.sleep(10)
                    houses_count = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//*[@id="form_browse_detailed_search"]/div/div[1]/div[5]/header/div[1]/strong'))
                    )
                    urls_dic[county][town]['url'] = current_url
                    urls_dic[county][town]['is_correct'] = True
                    urls_dic[county][town]['house_count'] = houses_count.text
            except (StaleElementReferenceException, WebDriverException, TimeoutException,selenium.common.exceptions.TimeoutException):
                    time.sleep(10)
                    try:
                        houses_count = WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, '//*[@id="form_browse_detailed_search"]/div/div[1]/div[5]/header/div[1]/strong'))
                        )
                        urls_dic[county][town]['url'] = current_url
                        urls_dic[county][town]['is_correct'] = True
                        urls_dic[county][town]['house_count'] = houses_count.text

                    except (StaleElementReferenceException, WebDriverException, TimeoutException,selenium.common.exceptions.TimeoutException):
                        time.sleep(10)
                        urls_dic[county][town]['url'] = current_url
                        urls_dic[county][town]['is_correct'] = False
                        urls_dic[county][town]['house_count'] = houses_count.text

            except (StaleElementReferenceException, WebDriverException, TimeoutException,selenium.common.exceptions.TimeoutException):
                time.sleep(10)
                urls_dic[county][town]['url'] = current_url
                urls_dic[county][town]['is_correct'] = False
                urls_dic[county][town]['house_count'] = houses_count.text

            time.sleep(3)
        county_complete = True
        all_towns_with_url_completion[key] = county_complete

        file_path = f'all_towns_with_url_{county}.json'
        with open(file_path, 'w') as json_file:
            json.dump(urls_dic, json_file)

        file_path = 'all_towns_with_url_completion.json'
        with open (file_path, 'w') as json_file:
            json.dump(all_towns_with_url_completion,json_file)

def get_houses(url,town):
    time.sleep(1)
    driver.get(url)
    try:
        houses_count = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'entities-count')))
        range = str(houses_count.text)
    except (StaleElementReferenceException, WebDriverException, TimeoutException):
        time.sleep(1)
        houses_count = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'entities-count')))
        range = str(houses_count.text)
    try:
        houses_container = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, 'EntityList-items')))
    except (StaleElementReferenceException, WebDriverException, TimeoutException):
        time.sleep(5)
        houses_container = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, 'EntityList-items')))
    try:
        houses = houses_container.find_elements(By.CSS_SELECTOR, 'li')
    except (StaleElementReferenceException, WebDriverException, TimeoutException):
        time.sleep(5)
        houses_container = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, 'EntityList-items')))
        houses = houses_container.find_elements(By.CSS_SELECTOR, 'li')

    houses_list_neat = []
    for item in houses:
        try:
            if len(item.text.split('\n')) > 3:
                try:
                    title = item.find_element(By.CLASS_NAME, 'entity-title')
                    title = format_item(title.text)
                    size_sqm_container = item.find_element(By.CLASS_NAME, 'entity-description-main')
                    size_sqm_split = size_sqm_container.text.splitlines()
                    size_sqm = float(size_sqm_split[1].split(':')[1].split(' ')[1])
                    price_elem = item.find_element(By.CLASS_NAME, 'entity-prices')
                    value_without_dot = price_elem.text.split(' ')[0].replace('.', '')
                    price = locale.atoi(value_without_dot)
                    price_per_sqm = price / size_sqm
                    house = {'title': title, 'size_sqm': size_sqm, 'price': price, 'price_per_sqm': price_per_sqm}
                    houses_list_neat.append(house)
                except(StaleElementReferenceException, WebDriverException, TimeoutException, NoSuchElementException):
                    time.sleep(1)
                    houses_container = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.CLASS_NAME, 'EntityList-items')))
                    houses = houses_container.find_elements(By.CSS_SELECTOR, 'li')
                    for item in houses:
                        if len(item.text.split('\n')) > 3:
                            title = item.find_element(By.CLASS_NAME, 'entity-title')
                            title = format_item(title.text)
                            size_sqm_container = item.find_element(By.CLASS_NAME, 'entity-description-main')
                            size_sqm_split = size_sqm_container.text.splitlines()
                            size_sqm = float(size_sqm_split[1].split(':')[1].split(' ')[1])
                            price_elem = item.find_element(By.CLASS_NAME, 'entity-prices')
                            value_without_dot = price_elem.text.split(' ')[0].replace('.', '')
                            price = locale.atoi(value_without_dot)
                            price_per_sqm = price / size_sqm
                            house = {'title': title, 'size_sqm': size_sqm, 'price': price, 'price_per_sqm': price_per_sqm}
                            houses_list_neat.append(house)
        except(StaleElementReferenceException, WebDriverException, TimeoutException):
            time.sleep(1)
            houses_container = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, 'EntityList-items')))
            houses = houses_container.find_elements(By.CSS_SELECTOR, 'li')
            for item in houses:
                if len(item.text.split('\n')) > 3:
                    try:
                        title = item.find_element(By.CLASS_NAME, 'entity-title')
                        title = format_item(title.text)
                        size_sqm_container = item.find_element(By.CLASS_NAME, 'entity-description-main')
                        size_sqm_split = size_sqm_container.text.splitlines()
                        size_sqm = float(size_sqm_split[1].split(':')[1].split(' ')[1])
                        price_elem = item.find_element(By.CLASS_NAME, 'entity-prices')
                        value_without_dot = price_elem.text.split(' ')[0].replace('.', '')
                        price = locale.atoi(value_without_dot)
                        price_per_sqm = price / size_sqm
                        house = {'title': title, 'size_sqm': size_sqm, 'price': price, 'price_per_sqm': price_per_sqm}
                        houses_list_neat.append(house)
                    except(StaleElementReferenceException, WebDriverException, TimeoutException):
                        time.sleep(10)
                        houses_container = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable(
                                (By.CLASS_NAME, 'EntityList-items')))
                        houses = houses_container.find_elements(By.CSS_SELECTOR, 'li')
                        for item in houses:
                            if len(item.text.split('\n')) > 3:
                                title = item.find_element(By.CLASS_NAME, 'entity-title')
                                title = format_item(title.text)
                                size_sqm_container = item.find_element(By.CLASS_NAME, 'entity-description-main')
                                size_sqm_split = size_sqm_container.text.splitlines()
                                size_sqm = float(size_sqm_split[1].split(':')[1].split(' ')[1])
                                price_elem = item.find_element(By.CLASS_NAME, 'entity-prices')
                                value_without_dot = price_elem.text.split(' ')[0].replace('.', '')
                                price = locale.atoi(value_without_dot)
                                price_per_sqm = price / size_sqm
                                house = {'title': title, 'size_sqm': size_sqm, 'price': price, 'price_per_sqm': price_per_sqm}
                                houses_list_neat.append(house)
    houses_list_dic = {'town': town, 'house_count': range, 'house_list': houses_list_neat}
    if str(len(houses_list_dic['house_list'])) == str(houses_count.text):
        print("bang onnnnn")
    else:
        print('this is the len houses dic',len(houses_list_dic['house_list']))
        print('this is the houses count var str',str(houses_count.text))
        #print(houses_container.text)
    return (houses_list_dic)
def get_region_all(region,items):
        whole_region = {'region': region, 'towns': []}
        for town in items.values():
            url = town['url']
            try:
                town_processed = get_houses(url,town['url'].split('/')[-1])
            except(StaleElementReferenceException, WebDriverException, TimeoutException):
                time.sleep(1)
                town_processed = get_houses(url,town['url'].split('/')[-1])
            if int(town_processed['house_count']) > 25:
                rounded_result = math.ceil(int(town_processed['house_count'])/25)
                counter = 2
                for page in range(rounded_result-1):
                    url = url + '?page=' + str(counter)
                    url_fixed = url.split('?')[0]+'?'+url.split('?')[-1]
                    counter += 1
                    town_processed_extra = get_houses(url_fixed,town['url'].split('/')[-1])
                    for item in town_processed_extra['house_list']:
                        town_processed['house_list'].append(item)

            whole_region['towns'].append(town_processed)
            #print(whole_region)
        return whole_region
def check_region(region):
    adds_up = 'adds_up'
    for town in region['towns']:
        #print(f"{town['town']} has {town['house_count']} houses on the count, and {len(town['house_list'])} in the list.")
        if int(town['house_count']) != len(town['house_list']):
            adds_up = f"Balls! {town} has {town['house_count']} houses on the count, and {len(town['house_list'])} in the list."
    return adds_up







#accept_cookies()
#time.sleep(5)
#razumijem()
#time.sleep(5)
#get_real_estate_section()
#time.sleep(5)
#razumijem()
#time.sleep(5)
#counties_dict = get_counties()
#time.sleep(5)
#counties_and_towns_dict = get_towns(counties_dict)
#time.sleep(5)
#format_towns(counties_and_towns_dict)
#time.sleep(60)

urls_dic = create_urls_dic()
time.sleep(5)
accept_cookies()
time.sleep(5)
razumijem()
time.sleep(5)
get_town_count(urls_dic)
time.sleep(5)




#with open('all_towns_with_url.json', 'r') as file:
#    dic = json.load(file)
#towns_with_urls = dic

#for region, items in towns_with_urls.items():
#    whole_region = get_region_all(region,items)
#    file_path = f'whole_region-{region}.json'
#    check_result = check_region(whole_region)
    #print(check_result)
#    with open(file_path, 'w') as json_file:
#       json.dump(whole_region, json_file)

driver.close()


print("local change")
