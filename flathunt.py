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
    driver = webdriver.Chrome()

    new_flats = []
    def checkFlat(link, regex):
        with open('flats.txt', 'a') as file:
            if(regex.match(link)):
                if(link+"\n" in old_flats):
                    pass
                else:
                    if(link not in new_flats):   #this prevents double detection from kleinanzeigen
                        new_flats.append(link)
                        print("NEW FLAT: ", link)
                        file.write(link+"\n")

    url_immonet = "https://www.immonet.de/immobiliensuche/beta?objecttype=1&locationIds=452497&fromrooms=3&fromarea=75&parentcat=1&marketingtype=2&page=1&radius=10"
    url_immowelt = "https://www.immowelt.de/suche/iserlohn-letmathe/wohnungen/mieten?ami=75&d=true&r=10&rmi=3&sd=DESC&sf=TIMESTAMP&sp=1"
    url_ebay = "https://www.kleinanzeigen.de/s-wohnung-mieten/58642/wohnung-mieten/k0c203l1740r10+wohnung_mieten.qm_d:75.00%2C+wohnung_mieten.zimmer_d:3.0%2C"

    # check immonet
    print("check immonet")
    r = requests.get(url_immonet)
    soup = BeautifulSoup(r.text.split("Passende </span>Angebote im")[0], features="html.parser")
    for flat in soup.find_all('a', href=True):
        link="https://www.immonet.de"+flat["href"]
        regex = re.compile("https://www.immonet.de/angebot/[0-9]+")
        checkFlat(link, regex)

    # check immowelt
    print("check immowelt")
    r = requests.get(url_immowelt)
    soup = BeautifulSoup(r.text, features="html.parser")
    for flat in soup.find_all('a', href=True):
        link = flat["href"]
        regex = re.compile("https://www.immowelt.de/expose/.+")
        checkFlat(link, regex)
    # check wg-gesucht
    # print("check wg-gesucht")
    # r = requests.get(url_wg_gesucht)
    # soup = BeautifulSoup(r.text)
    # for flat in soup.find_all('a', href=True):
    #     link = "https://www.wg-gesucht.de/"+flat["href"]
    #     regex = re.compile("https://www.wg-gesucht.de/wohnungen-in-Paderborn-Kernstadt.[0-9]+.html")
    #     checkFlat(link, regex)
    
    # check ebay
    print("check ebay-kleinanzeigen")
    driver.get(url_ebay)
    html = driver.page_source.split("Alternative Anzeigen in der Umgebung")[0]
    time.sleep(2)
    soup = BeautifulSoup(html, features="html.parser")
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