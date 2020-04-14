from bs4 import BeautifulSoup
import re
import requests
import time
import pandas as pd
import numpy as np
from app import db
from app.models import ScrapedData

sort_options = {
    'relevance':'relevance',
    'popularity':'popularity',
    'price low to high':'price_asc',
    'price high to low':'price_desc',
    'discount':'relevance',
    'new arrivals':'recency_desc'
}


def flipkartparser(url):
    time.sleep(2)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    response = requests.get(url, headers=headers)
    output = {}

    htmltext = response.text
    soup = BeautifulSoup(htmltext,'html.parser')
    brand = soup.find('span',{'class':"_2J4LW6"})
    name = soup.find('span',{'class':"_35KyD6"})
    price = soup.find('div',{'class':"_1vC4OE _3qQ9m1"})
    rating = soup.find('div',{'class':"hGSR34"})
    try:
        photo = soup.findAll('div',{'class':"_2_AcLJ"})[0].get('style')[21:-1]
    except:
        photo = None
    reviews_n_ratings = soup.find('span',{'class':'_38sUEc'}).text
    link = url
    if name:
        output['name'] = name.text
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
   
    if reviews_n_ratings:
        if '&' in reviews_n_ratings:
            output['total_reviews'] = reviews_n_ratings.split('&')[1]
    else:
        output["total_reviews"] = np.nan

    if reviews_n_ratings :
        if '&' in reviews_n_ratings:
            output['total_rating']=reviews_n_ratings.split('&')[0]
        else:
            output['total_rating'] = reviews_n_ratings
    else:
        output['total_rating']= np.nan

    output['link'] = link
    output['website'] = 'flipcart'
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

def NextPage(keyword = 'mobile',delay=1, page=1,sort = sort_options.get('relevance')):
    pattern = re.compile(r"/[/ 0-9 a-z -]+/p/[0-9a-z]{16,16}") #flipkart product id
    url = f"https://www.flipkart.com/search?"
    params = {
        'q' : keyword,
        'sort' : sort,
        'page':page,
        }

    htmltext = requests.get(url,params=params).text
    time.sleep(delay)
    List = re.findall(pattern,htmltext)
    pagelinks = list(set(List))
    page +=1
    return pagelinks, page
    



def getPageLinks(links,query,delay=1):
    with open('scraper.log','a') as f:
        f.write(f"-->{len(links)} links are to be scraped from flipcart\n")
    for i in links[:5]:
        url =  "https://www.flipkart.com"+i
        print ("Processing: "+url)
        try:
            dd = flipkartparser(url) # data dictionary variable
            # print(dd)
            scraped_data = ScrapedData(
                name = dd['name'],
                price = dd['price'],
                rating = dd['rating'],
                photo = dd['photo'],
                total_reviews = dd.get('total_reviews',np.nan),
                total_rating = dd.get('total_rating',np.nan),
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
            print("---"*20)

        with open('scraper.log','a') as f:
            f.write(f"query: {query} | flipcart, scraped: {i}\n")
    time.sleep(delay)
    return "saved info to scraper.log file"
        
def collect_n_store(query = 'laptops',item_pos = 1,count=50,delay=1,sorting=sort_options.get('relevance') ):
    # print("running flipcart scraper")
    # print('>query',query)
    # print('>item_pos',item_pos)
    # print('>limit ',count)
    # print('>delay',delay)
    # print('>sort option',sorting)
    productlinks = []
    while True:
        try:
            links,pos = NextPage(keyword=query,delay=delay,page=item_pos,sort=sorting)
            productlinks.extend(links)
            item_pos = pos
            if (item_pos>=count):
                print("links:", len(links),"\npos:",pos)
                break
            else:
                print('loading pages',item_pos)
        except Exception as e:
            print(e)
    message = getPageLinks(productlinks,query,delay)
    return message
 
if __name__ == "__main__":
    item_pos = 0
    query = 'laptops'
    message  = collect_n_store(query=query,item_pos=item_pos,count=1,delay=1)