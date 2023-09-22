import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests

LINK_FORM = 'https://docs.google.com/forms/d/e/1FAIpQLSewzrxEvgYsn4Uzpy266PUvcundCtIUPprq1YfjskSAtThh7Q/viewform?usp=sf_link'
DOCUMENT_LINK = 'https://docs.google.com/spreadsheets/d/1YEZvf9j6qRWOGsAOAdrpqivl84CMeWphqtzexygKVu0/edit?resourcekey#gid=622527427'

city_search = input(
    "Where do you want to find an apartment? (digit location)").lower()
x = city_search.split()
city = ''
for y in x:
    if x.index(y) == len(x)-1:
        city += y
    else:
        city += (y + "-")
min_price = input('How much are you willing to pay? (min) ')
max_price = input('How much are you willing to pay? (max) ')
m2 = input('How big at least? m2 ')
link_rental = f'https://www.immobiliare.it/affitto-case/{city}/' \
              f'?criterio=prezzo' \
              f'&ordine=asc' \
              f'&prezzoMinimo={min_price}' \
              f'&prezzoMassimo={max_price}' \
              f'&superficieMinima={m2}'


# INITIALIZATION
chrome_drivers_path = 'C:/Development/chromedriver.exe'
option = webdriver.ChromeOptions()
option.binary_location = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
# option.add_experimental_option("detach", True)  # this is needed for keeping it alive
s = Service(chrome_drivers_path)
driver = webdriver.Chrome(service=s, options=option)


# AUTOMATION
driver.get(link_rental)
html_page = requests.get(link_rental).text
soup = BeautifulSoup(html_page, features='html.parser')
html_house_list = soup.find_all(name='a', class_='in-card__title')
house_link = soup.find_all(name='a', class_='in-card__title', attrs='href')
titles_list = [house.text.split(',')[0] for house in html_house_list]
html_price_list = soup.find_all(
    name='li', class_='in-realEstateListCard__features--main')
price_list = [price.text for price in html_price_list]
link_list = [link.get('href') for link in house_link]
announce_id = soup.find_all(name='li', class_='in-realEstateResults__item')
total_announce = soup.find_all(name='div', class_='in-realEstateListCard')
ids = []
address_for_gmaps = []
for id_ in announce_id:
    if announce_id.index(id_) == len(total_announce):
        break
    else:
        house_id = id_.get('id').split('_')[2]
        ids.append(house_id)
        response = requests.get(
            f'https://www.immobiliare.it/annunci/{house_id}/').text
        soup = BeautifulSoup(response, 'html.parser')
        whole_address = soup.find(name='span', class_='im-location')
        next1 = whole_address.nextSibling.text.replace(
            ' - ', '-').replace(' ', '-').replace('à', 'a').replace("'", '-')
        try:
            next2 = whole_address.nextSibling.nextSibling.text.replace(
                ' - ', '-').replace(' ', '-').replace('à', 'a').replace("'", '-')
            address_for_gmaps.append(f"{whole_address.text}-{next1}-{next2}")
        except AttributeError:
            address_for_gmaps.append(f"{whole_address.text}-{next1}")
gmaps_links = [
    f"https://www.google.com/maps/search/{address}" for address in address_for_gmaps]
map_links = [
    f'https://www.immobiliare.it/annunci/{serial_id}/#mappa' for serial_id in ids]
address_title = [address for address in address_for_gmaps]


for n in range(len(house_link)):
    driver.get(LINK_FORM)
    title_form = driver.find_element(By.XPATH,
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address = driver.find_element(By.XPATH,
                                  '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(By.XPATH,
                                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    announce_direct_link = driver.find_element(By.XPATH,
                                               '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input')
    gmaps = driver.find_element(By.XPATH,
                                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input')
    announce_map = driver.find_element(By.XPATH,
                                       '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[1]/div/div[1]/input')

    time.sleep(1)
    title_form.click()
    title_form.send_keys(titles_list[n])
    time.sleep(1)
    address.click()
    address.send_keys(address_title[n])
    time.sleep(1)
    price.click()
    price.send_keys(price_list[n])
    time.sleep(1)
    announce_direct_link.click()
    announce_direct_link.send_keys(link_list[n])
    time.sleep(1)
    gmaps.click()
    gmaps.send_keys(gmaps_links[n])
    time.sleep(1)
    announce_map.click()
    announce_map.send_keys(map_links[n])
    time.sleep(1)
    driver.find_element(
        By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div').click()
    time.sleep(1)

print(F"Values stored at: {DOCUMENT_LINK}")
