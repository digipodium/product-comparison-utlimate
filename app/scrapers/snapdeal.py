from bs4 import BeautifulSoup
import re
import requests
import time
import pandas as pd
import numpy as np
from app import db
from app.models import ScrapedData

sort_options = {
    'relevance':'rlvncy',
    'popularity':'plrty',
    'price low to high':'plth',
    'price high to low':'phtl',
    'discount':'dhtl',
    'new arrivals':'rec'
}


def snapdealparser(url):
    time.sleep(2)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    response = requests.get(url, headers=headers)
    output = {}

    htmltext = response.text
    soup = BeautifulSoup(htmltext,'html.parser')
    name = soup.findAll('img',{'class':"cloudzoom"})[0].get('title')
    price = soup.find('span',{'class':"payBlkBig"})
    rating = soup.find('span',{'class':"avrg-rating"})
    photo = soup.findAll('img',{'class':"cloudzoom"})[0].get('src')
    total_rating = soup.find('span',{'class':'total-rating'})
    total_reviews = soup.find('span',{'class':'numbr-review'})
    link = url
    if name:
        output['name'] = name
    else :
        output['name'] = None
            
    if price:
        output['price'] = price.text
    else :
        output['price'] = np.nan 
        
    if rating:
        output['rating'] = rating.text  
    else :
        output['rating'] = np.nan

    if photo:
        output['photo'] = photo
    else:
        output["photo"] = None
   
    if total_reviews:
        output['total_reviews'] = total_reviews.text
    else:
        output["total_reviews"] = np.nan

    if total_rating:
        output['total_rating']=total_rating.text
    else:
        output['total_rating']= np.nan

    output['link'] = link
    output['website'] = 'snapdeal'
    return output


# def init(query='mobile',baseurl="https://www.snapdeal.com/search?keyword=",delay=2):
#     url =  baseurl + query.lower()
#     pattern = re.compile(r"/product/.*/\d{12,20}")  #Snapdeal product id
#     print("Searching your product at...",url )
#     htmltext = requests.get(url).text
#     time.sleep(delay)
#     List = re.findall(pattern,htmltext)
#     pagelinks = list(set(List))
#     return pagelinks

def NextPage(keyword = 'mobile',delay=2, item_pos=0, pincode = '226001',sort = sort_options.get('relevance'),searchState = 'k3=true|k5=0|k6=0|k8=0', webpageName = 'searchResult', clickSrc = 'unknown',isMC = False, showAds = False, page = 'srp'):
    item_pos +=20
    pattern = re.compile(r"/product/.*/\d{12,20}")
    url = f"https://www.snapdeal.com/acors/json/product/get/search/0/{item_pos}/20?"
    params = {
        'keyword' : keyword, 'pincode':pincode, 'sort' : sort,
        'searchState':searchState, 'webpageName' : webpageName, 'clickSrc' : clickSrc,
        'isMC':isMC , 'showAds' : showAds, 'page' : page}

    htmltext = requests.get(url,params=params).text
    time.sleep(delay)
    List = re.findall(pattern,htmltext)
    pagelinks = list(set(List))
    return pagelinks, item_pos
    



def getPageLinks(links,query,delay=1):
    with open('scraper.log','a') as f:
        f.write(f"-->{len(links)} links are to be scraped from snapdeal\n")
    for i in links:
        url = "https://www.snapdeal.com"+i
        print ("Processing: "+url)
        try:
            dd = snapdealparser(url) # data dictionary variable
            scraped_data = ScrapedData(
                name = dd['name'],
                price = dd['price'],
                rating = dd['rating'],
                photo = dd['photo'],
                total_reviews = dd['total_reviews'],
                total_rating = dd['total_rating'],
                link = dd['link'],
                website = dd['website'].lower(),
                keyword= query.lower(),
            )
            db.session.add(scraped_data)
            db.session.commit()
        except Exception as e:
            print("---"*20)
            print(e)
            print("------------------------------"*10)
        with open('scraper.log','a') as f:
            f.write(f"query: {query} | snapdeal, scraped: {i}\n")
    
    time.sleep(delay)
    return "saved info to scraper.log file"
        
def collect_n_store(query = 'laptops',item_pos = 0,count=500,delay=2,sorting=sort_options.get('relevance') ):
    count *= 30*2
    # print("running snapdeal scraper")
    # print('>query',query)
    # print('>item_pos',item_pos)
    # print('>limit ',count)
    # print('>delay',delay)
    # print('>sort option',sorting)
    productlinks = []
    while True:
        # try:
        links,pos = NextPage(keyword=query,item_pos=item_pos,delay=delay,sort=sorting)
        productlinks.extend(links)
        item_pos = pos
        print('loading pages',item_pos)
        if (item_pos>=count):
            print("links:", len(links),"\npos:",pos)
            break
        else:
            print('loading pages',item_pos)
        # except Exception as e:
        #     print(e)
    message = getPageLinks(productlinks,query,delay)
    return message
 
if __name__ == "__main__":
    item_pos = 0
    query = 'laptops'
    message  = collect_n_store(query=query,item_pos=int(item_pos),count=25,delay=1)