import requests
import re
import time
import telegram_send
from bs4 import BeautifulSoup
from selenium import webdriver

while True:
    with open('flats.txt') as f:
        old_flats = f.readlines()
        
    # start web browser
    driver = webdriver.Chrome('chromedriver.exe')

    new_flats = []
    def checkFlat(link, regex):
        with open('flats.txt', 'a') as file:
            if(regex.match(link)):
                if(link+"\n" in old_flats):
                    pass
                else:
                    new_flats.append(link)
                    print("NEW FLAT: ", link)
                    file.write(link+"\n")

    url_immonet = "https://www.immonet.de/immobiliensuche/sel.do?fromarea=75.0&city=130996&parentcat=1&suchart=2&marketingtype=2&toprice=900.0&fromrooms=3.0&district=11417&radius=0&listsize=26&objecttype=1&pageoffset=1&sortby=19"
    url_immowelt = "https://www.immowelt.de/liste/paderborn-kernstadt/wohnungen/mieten?ami=70&d=true&pma=900&rmi=3&sd=DESC&sf=TIMESTAMP&sp=1"
    url_wg_gesucht = "https://www.wg-gesucht.de/wohnungen-in-Paderborn.103.2.1.0.html?offer_filter=1&city_id=103&noDeact=1&dFr=0&categories%5B%5D=2&rent_types%5B%5D=0&sMin=75&rMax=900&ot%5B%5D=2414&rmMin=3&img_only=1"
    url_ebay = "https://www.ebay-kleinanzeigen.de/s-wohnung-mieten/33100/preis::800/wohnung/k0c203l2164+wohnung_mieten.qm_d:70.00%2C+wohnung_mieten.verfuegbarm_i:5%2C+wohnung_mieten.verfuegbary_i:2022%2C+wohnung_mieten.zimmer_d:3.0%2C"


    # check immonet
    print("check immonet")
    r = requests.get(url_immonet)
    soup = BeautifulSoup(r.text.split("Passende </span>Angebote im")[0])
    for flat in soup.find_all('a', href=True):
        link="https://www.immonet.de"+flat["href"]
        regex = re.compile("https://www.immonet.de/angebot/[0-9]+")
        checkFlat(link, regex)

    # check immowelt
    print("check immowelt")
    r = requests.get(url_immowelt)
    soup = BeautifulSoup(r.text)
    for flat in soup.find_all('a', href=True):
        link = flat["href"]
        regex = re.compile("https://www.immowelt.de/expose/.+")
        checkFlat(link, regex)
    # check wg-gesucht
    print("check wg-gesucht")
    r = requests.get(url_wg_gesucht)
    soup = BeautifulSoup(r.text)
    for flat in soup.find_all('a', href=True):
        link = "https://www.wg-gesucht.de/"+flat["href"]
        regex = re.compile("https://www.wg-gesucht.de/wohnungen-in-Paderborn-Kernstadt.[0-9]+.html")
        checkFlat(link, regex)
    
    # check ebay
    print("check ebay-kleinanzeigen")
    driver.get(url_ebay)
    html = driver.page_source.split("Alternative Anzeigen in der Umgebung")[0]
    time.sleep(2)
    soup = BeautifulSoup(html)
    for flat in soup.find_all('a', href=True):
        link = "https://www.ebay-kleinanzeigen.de"+flat["href"]
        regex = re.compile("https://www.ebay-kleinanzeigen.de/s-anzeige/.+")
        checkFlat(link, regex)


    if(new_flats != []):
        print("sending telegram msg")
        telegram_send.send(messages=["Es wurden neue Wohnungen gefunden!"])
        telegram_send.send(messages=new_flats)

    else:
        print("keine neuen Wohnungen")
    driver.close()
    time.sleep(300)