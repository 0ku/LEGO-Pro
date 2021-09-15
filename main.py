from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import requests

names = []
links = []
prices = []
descs = []
dates = []

url = 'https://www.kijiji.ca/b-ottawa/"lego"-brand-new/k0l1700185?rb=true&dc=true'
for i in range(0,5):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')

    #format later by using .text.strip()
    for listing in soup.findAll('div',attrs={'class':'info'}):
        name = listing.find('a',href = True,attrs={'class':'title'})
        link = f"https://www.kijiji.ca/{name['href']}"
        price = listing.find('div',attrs={'class':'price'})
        desc = listing.find('div',attrs={'class':'description'})
        date = listing.find('span',attrs={'class':'date-posted'})
        names.append(name.text.strip())
        links.append(link)
        prices.append(price.text.strip())
        descs.append(desc.text.strip())
        dates.append(date.text.strip())

    newLink = soup.find('a',href = True,attrs={'title':'Next'})
    url = f"https://www.kijiji.ca{newLink['href']}"

#-------------------------------------------------------------------
def getInfo(link):
    url = link
    information = []
    HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    r = requests.get(url,headers=HEADERS)
    soup = BeautifulSoup(r.content,'html5lib')
    for bsr in soup.findAll('span'):
        if 'Toys & Games' in bsr.text:
            information.append(bsr.text)
    price1 = soup.find('span',attrs={'class':'a-size-base a-color-price'}).text.strip()
    price2 = soup.find('span',attrs={'id':'price_inside_buybox'}).text.strip()
    information.append(f"{price1} / {price2}")
    return information

amazonNames = []
amazonPrices = []
amazonBSRs = []
amazonLinks = []
for currentProduct in names:
    currentProduct.replace('#','')
    integers = [int(s) for s in currentProduct.split() if s.isdigit()]
    if len(integers) == 0:
        amazonLinks.append('N/A')
        continue
    tag = max(integers)
    url = f'https://www.amazon.ca/s?k=lego+{tag}&ref=nb_sb_noss'
    amazonLinks.append(url)
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    r = requests.get(url,headers=headers)
    
    soup = BeautifulSoup(r.content,'html.parser')
    results = soup.findAll('div',href = True,attrs={'class':'a-link-normal a-text-normal'})
    found = False
    print(results)
    for a in range(0,len(results)):
        currentListing = results[a]
        title = currentListing.find('span',attrs={'class':'a-link-normal a-text-normal'})
        if str(tag) in title.text.strip():
            found = True
            amazonNames.append(title.text)
            amazonPrices.append(currentListing.find('span',attrs={'class':'a-offscreen'}))
            link = currentListing.find('a',href = True,attrs={'class':'a-link-normal a-text-normal'})['href']
            info = getInfo(f'https://www.amazon.ca{link}')
            amazonBSRs.append(info[0])
            amazonPrices.append(info[1])
            amazonLinks.append(f'https://www.amazon.ca{link}')
            break
    if found == False:
        amazonNames.append('N/A')
        amazonPrices.append('N/A')
        amazonBSRs.append('N/A')
        amazonLinks.append('N/A')





