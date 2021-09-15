from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import requests
import subprocess

names = []
links = []
prices = []
descs = []
dates = []

amazonNames = []
amazonPrices = []
amazonBSRs = []
amazonLinks = []

url = 'https://www.kijiji.ca/b-ottawa/"lego"-brand-new/k0l1700185?rb=true&dc=true'
for i in range(0,7):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    #format later by using .text.strip()
    for listing in soup.findAll('div',attrs={'class':'info'}):
        name = listing.find('a',href = True,attrs={'class':'title'})
        link = f"https://www.kijiji.ca{name['href']}"
        price = listing.find('div',attrs={'class':'price'})
        desc = listing.find('div',attrs={'class':'description'})
        date = listing.find('span',attrs={'class':'date-posted'})
        names.append(name.text.strip())
        links.append(link)
        if date:
            dates.append(date.text.strip())
        else:
            dates.append("N/A")
        if price != None:
            prices.append(price.text.strip())
        else:
            prices.append("N/A")
        descs.append(desc.text.strip())

    newLink = soup.find('a',href = True,attrs={'title':'Next'})
    url = f"https://www.kijiji.ca{newLink['href']}"

def getInfo(link):
    url = link
    HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    r = requests.get(url,headers=HEADERS)
    soup = BeautifulSoup(r.content,'html5lib')
    found = False
    for bsr in soup.findAll('span'):
        if 'in Toys & Games' in bsr.text:
            amazonBSRs.append(bsr.text.strip())
            found = True
            break
    if found == False:
        amazonBSRs.append("N/A")

    price1 = soup.find('span',attrs={'class':'a-size-base a-color-price'})
    price2 = soup.find('span',attrs={'id':'price_inside_buybox'})
    if price2:
        amazonPrices.append(price2.text.strip())
    elif price1:
        amazonPrices.append(price1.text.strip())
    else:
        amazonPrices.append("N/A")

for currentProduct in names:
    currentProduct.replace('#','')
    integers = [int(s) for s in currentProduct.split() if s.isdigit()]
    if len(integers) == 0:
        amazonLinks.append("N/A")
        amazonPrices.append("N/A")
        amazonBSRs.append("N/A")
        continue
    tag = max(integers)
    foundLink = False
    url = f'https://www.amazon.ca/s?k=lego+{tag}&ref=nb_sb_noss'
    #url = "https://www.amazon.ca/s?k=lego+10255&ref=nb_sb_noss"

    HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    r = requests.get(url,headers=HEADERS)

    soup = BeautifulSoup(r.content,'html5lib')
    results = soup.findAll('a',href = True,attrs={'class':'a-link-normal a-text-normal'})
    print(len(results))
    for listing in soup.findAll('a',href = True,attrs={'class':'a-link-normal a-text-normal'}):
        title = listing.find('span',attrs={'class':'a-size-base-plus a-color-base a-text-normal'})
        if str(tag) in title.text:
            print(title.text)
            foundLink = True
            amazonLinks.append(f"https://www.amazon.ca/{listing['href']}")
            getInfo(f"https://www.amazon.ca/{listing['href']}")
            break
    if foundLink == False:
        amazonLinks.append("N/A")
        amazonPrices.append("N/A")
        amazonBSRs.append("N/A")


print(len(amazonLinks),len(amazonPrices),len(amazonBSRs),len(names))

df = pd.DataFrame({'Listing Name':names,'Price':prices,'Description':descs,'Link':links, 'Dates':dates, 'Amazon Link':amazonLinks,'Amazon Price':amazonPrices,'Amazon BSR':amazonBSRs})
df.to_csv('listings.csv',index = False,encoding ='utf-8')




