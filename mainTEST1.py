from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import requests
import subprocess
import jsonlines
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
        names.append(name.text.strip())
        links.append(link)
        prices.append(price.text.strip())
        descs.append(desc.text.strip())

    newLink = soup.find('a',href = True,attrs={'title':'Next'})
    url = f"https://www.kijiji.ca{newLink['href']}"

#-------------------------------------------------------------------
def getBSR(link):
    url = link
    HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    r = requests.get(url,headers=HEADERS)
    soup = BeautifulSoup(r.content,'html5lib').prettify
    for test in soup.findAll('span',attrs={'class':None}):
        if '#' in test.text:
            return test.text

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
    foundLink = False
    #url = f'https://www.amazon.ca/s?k=lego+{tag}&ref=nb_sb_noss'
    url = "https://www.amazon.ca/s?k=lego+10255&ref=nb_sb_noss"
    urlFile = open("c:/Users/evanj.DESKTOP-VSHI6R0.000/Documents/GitHub/legoprofit/kijiji-scraper/search_results_urls.txt","r+")
    urlFile.truncate(0)
    urlFile.write(url)
    subprocess.call(["python", "c:/Users/evanj.DESKTOP-VSHI6R0.000/Documents/GitHub/legoprofit/kijiji-scraper/searchresults.py"])
    with jsonlines.open('c:/Users/evanj.DESKTOP-VSHI6R0.000/Documents/GitHub/legoprofit/kijiji-scraper/search_results_output.jsonl') as f:
        a = 0
        for listing in f.iter():
            if a == 5:
                break
            print(listing["title"])
            if str(tag) in listing["title"]:
                foundLink = True
                amazonLinks.append(listing["search_url"])
            a+=1
    if foundLink == False:
        amazonLinks.append("N/A")

#     print(url)
#     amazonLinks.append(url)
#     headers = {'User-Agent': 'Mozilla/5.0'}
#     r = requests.get(url,headers=headers)
    
#     soup = BeautifulSoup(r.content,'html.parser')
#     results = soup.findAll('div',href = True,attrs={'class':'a-link-normal a-text-normal'})
#     found = False
#     for a in range(0,len(results)):
#         currentListing = results[a]
#         title = currentListing.find('span',attrs={'class':'a-link-normal a-text-normal'})
#         if str(tag) in title.text.strip():
#             found = True
#             amazonNames.append(title.text)
#             amazonPrices.append(currentListing.find('span',attrs={'class':'a-offscreen'}))
#             link = currentListing.find('a',href = True,attrs={'class':'a-link-normal a-text-normal'})['href']
#             amazonBSRs.append(getBSR(f'https://www.amazon.ca{link}'))
#             amazonLinks.append(f'https://www.amazon.ca{link}')
#             break
#     if found == False:
#         amazonNames.append('N/A')
#         amazonPrices.append('N/A')
#         amazonBSRs.append('N/A')
#         amazonLinks.append('N/A')

df = pd.DataFrame({'Listing Name':names,'Price':prices,'Description':descs,'Link':links,'Amazon Link':amazonLinks})
df.to_csv('listings.csv',index = False,encoding ='utf-8')




