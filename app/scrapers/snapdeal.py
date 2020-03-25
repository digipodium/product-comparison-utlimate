from bs4 import BeautifulSoup
import re
import requests
import time

sort_options = {
    'relevnace':'rlvncy',
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
        output['name'] = 'N/A' 
            
    if price:
        output['price'] = price.text
    else :
        output['price'] = 'N/A' 
        
    if rating:
        output['rating'] = rating.text  
    else :
        output['rating'] = 'N/A'

    if photo:
        output['photo'] = photo
    else:
        output["photo"] = 'N/A'
   
    if total_reviews:
        output['total_reviews'] = total_reviews.text
    else:
        output["total_reviews"] = 'N/A'

    if total_rating:
        output['total_rating']=total_rating.text
    else:
        output['total_rating']='N/A'

    output['link'] = link
    return output


def init(query='mobile',baseurl="https://www.snapdeal.com/search?keyword=",delay=2):
    url =  baseurl + query.lower()
    pattern = re.compile(r"/product/.*/\d{12,20}")  #Snapdeal product id
    print("Searching your product at...",url )
    htmltext = requests.get(url).text
    time.sleep(delay)
    List = re.findall(pattern,htmltext)
    pagelinks = list(set(List))
    return pagelinks

def NextPage(keyword = 'mobile',delay=2, item_pos=0, pincode = '226001',sort = sort_options.get('relevnace'),searchState = 'k3=true|k5=0|k6=0|k8=0', webpageName = 'searchResult', clickSrc = 'unknown',isMC = False, showAds = False, page = 'srp'):
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
    



def getPageLinks():
    
    links,pos = NextPage()
    print(links)
    extracted_data = []
    for i in links:
        url = "https://www.snapdeal.com"+i
        print ("Processing: "+url)
        extracted_data.append(snapdealparser(url))
        time.sleep(1)
    for i in extracted_data:
        print(i)
        print()
        
        
 
if __name__ == "__main__":
    getPageLinks()