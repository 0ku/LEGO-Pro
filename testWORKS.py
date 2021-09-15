from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import requests
import subprocess
import json

def getBSR(link):
    url = link
    HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    r = requests.get(url,headers=HEADERS)
    soup = BeautifulSoup(r.content,'html5lib')
    for test in soup.findAll('span'):
        if '#' in test.text:
            return test.text

print(getBSR("https://www.amazon.ca/6174038-Creator-Expert-Assembly-Building/dp/B01NBP28HQ/ref=sr_1_1?dchild=1&keywords=lego+10255&qid=1619197649&sr=8-1"))

amazonLinks = []
amazonNames = []
amazonPrices = []
amazonBSRs = []
url = "https://www.amazon.ca/s?k=lego+10255&ref=nb_sb_noss"
amazonLinks.append(url)
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
r = requests.get(url,headers=HEADERS)
tag = 6174038
soup = BeautifulSoup(r.content,'html5lib')
results = soup.findAll('div',href = True, attrs={'class':'a-link-normal a-text-normal'})
print(results)
found = False
for a in range(0,len(results)):
    currentListing = results[a]
    title = currentListing.find('span',attrs={'class':'a-link-normal a-text-normal'})
    if str(tag) in title.text.strip():
        found = True
        amazonNames.append(title.text)
        amazonPrices.append(currentListing.find('span',attrs={'class':'a-offscreen'}))
        link = currentListing.find('a',href = True,attrs={'class':'a-link-normal a-text-normal'})['href']
        amazonBSRs.append(getBSR(f'https://www.amazon.ca{link}'))
        amazonLinks.append(f'https://www.amazon.ca{link}')
        break

if found == False:
    amazonNames.append('N/A')
    amazonPrices.append('N/A')
    amazonBSRs.append('N/A')
    amazonLinks.append('N/A')

print(amazonBSRs)
#df = pd.DataFrame({'Listing Name':names,'Price':prices,'Description':descs,'Link':links,'Amazon Link':amazonLinks})
#df.to_csv('listings.csv',index = False,encoding ='utf-8')