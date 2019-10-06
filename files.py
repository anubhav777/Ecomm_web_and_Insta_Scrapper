from app import app
from bs4 import BeautifulSoup
import requests,lxml
from selenium import webdriver
import time
import json
from functools import wraps
from flask import request
import jwt
from models import *
secret=app.config['SECRET_KEY']

def decorator(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        token =None
        
        if 'x-access-token' in request.headers:
            new_token=request.headers['x-access-token']
            token_decode=jwt.decode(new_token,secret)
            currentuser=Signup.query.filter_by(id=token_decode['userid']).first()
            if not currentuser:
                return ({'status':'You are not a valid user please register first'})
            userid=token_decode['userid']
                   
            return func(userid,*args,**kwargs)
        else:
            return({'status':'token not valid'})
            
    return wrapper



def ebay(name):
    url=f"https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={name}&_sacat=0"
    source=requests.get(url).text

    soup=BeautifulSoup(source,'lxml')
    art=soup.find(id='mainContent')
    child_art=art.find('div',id='srp-river-main')
    ul_par=child_art.find('div',id='srp-river-results')
    ul=ul_par.find('ul',class_='srp-results')
    li=ul.find_all('li',class_='s-item')
    newarr=[]
    for new_li in li:
        try:
            txtli=new_li.text
            img_class=new_li.find('img', class_='s-item__image-img')['src']
            a_tag=new_li.find('a',class_='s-item__link').h3.text
            price_span=new_li.find('span',class_='s-item__price').text
            new_obj={'img_src':img_class,'discription':a_tag,'price_span':price_span}
            newarr.append(new_obj)
            
        except Exception as e:
            print(e)
    return newarr
# print(ebay('hp'))

# source=requests.get('https://www.flipkart.com/search?q=hp&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off').text

# soup=BeautifulSoup(source,'lxml')
# art=soup.find_all('div',class_='_3liAhj')
# for parent in art:
#     img_src=parent.find('img',class_='_1Nyybr')['src']
    
#     disc=parent.find('a',class_='_2cLu-l').text
#     print(img_src)

def amazon(name):
    newarr=[]
    headers = {'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'}
    search_attr=None
    if " " in name:
        search_attr=name.replace(" ","+")
    else:
        search_attr=name
    url=f"https://www.amazon.com/s?k={search_attr}&ref=nb_sb_noss_1"
    source=requests.get(url,headers=headers).text
    
    soup=BeautifulSoup(source,'lxml')
    art=soup.find_all('div',class_='s-result-item')
    for parent in art:
        try:
            first_par=parent.find('div',class_='s-include-content-margin')
            img_src=first_par.find('div',class_='s-image-fixed-height').img['src']
            disc=first_par.find('span',class_='a-size-medium').text
            price=first_par.find('span',class_='a-offscreen').text
            if price:
                new_obj={'img_src':img_src,'discription':disc,'price':price}
                newarr.append(new_obj)
            
        except Exception as e:
            pass

    return newarr



# print(amazon('hp laptop'))


def daraz(name):
    newarr=[]
    search_attr=None
    if " " in name:
        search_attr=name.replace(" ","+")
    else:
        search_attr=name
    url=f"https://www.daraz.com.np/catalog/?q={name}&_keyori=ss&from=input&spm=a2a0e.11779170.search.go.36c42d2b2Nkfy8"
    source=requests.get(url).text
    soup=BeautifulSoup(source,'lxml')
    art=soup.find_all('script')
    art_child=None
    for par in art:
        try:
            fg=str(par)
            if 'window.pageData' in fg:
                art_child=fg
            
        except Exception as e:
            pass
    fistsplit=art_child.split("=",1)[1]
    sec_split=fistsplit.replace("</script>","")

    new_json=json.loads(sec_split)
    first_child=new_json['mods']
    main_child=first_child['listItems']


    # notes for finding key of a large object
    # for k,v in first_child.items():
    
    #        print(k)
    for parent in main_child:
        try:
            discription=parent['name']
            image=parent['image']
            price=parent['priceShow']
            newobj={'discription':discription,'image':image,'price':price}
            newarr.append(newobj)

        except Exception as e:
            pass
    return newarr

def walmart(name):
    newarr=[]
    search_attr=None
    if " " in name:
        search_attr=name.replace(" ","%20")
    else:
        search_attr=name
    url=f"https://www.walmart.com/search/?query={search_attr}"
    source=requests.get(url).text
    soup=BeautifulSoup(source,'lxml')
    art=soup.find_all('div',class_='search-result-gridview-item')
    for parent in art:
        try:
            img_src=parent.find('div',class_='orientation-square').img['src']
            discription=parent.find('a',class_='product-title-link').span.text
            price=parent.find('span',class_='price-main-block').span.find('span').text
            newobj={'discription':discription,'img':img_src,'price':price}
            newarr.append(newobj)
        except Exception as e:
            pass
        
    return newarr

def sastodeal(name):
    newarr=[]
    search_attr=None
    if " " in name:
        search_attr=name.replace(" ","+")
    else:
        search_attr=name
    url=f"https://www.sastodeal.com/catalogsearch/result/?q={search_attr}"
    source=requests.get(url).text
    soup=BeautifulSoup(source,'lxml')
    art=soup.find('ol',class_='product-items').find_all('li')
    for parent in art:
        # try:
            img=parent.find('span',class_='product-image-wrapper').img['src']
            discription=parent.find('a',class_='product-item-link').text
            discription=discription.strip()
            price=parent.find_all('span',class_='price-final_price')[-1].text
            newobj={'discription':discription,'img':img,'price':'price'}
            newarr.append(newobj)
        # except Exception as e:
        #     pass

   
    return newarr

def tudoholic():
    newarr=[]
    headers={
       
        'Referer': 'https://tudoholic.com/search?type=product&q=shoes',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'ss=29be291bot; tawkUUID=D898KeZOSb3TnV6h1HiTTMpAde2sj4VU0gqqcQFKOUuFqhnPsdYX2U9sQJbRRIyf%7C%7C2',
        'origin': 'https://tudoholic.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
        'accessToken':'07e05537bb67d15b19460a6539dfe3b4'
    }
    source=requests.get('https://tudoholic.com/search?type=product&q=shoes',headers=headers).text
    soup=BeautifulSoup(source,'lxml')
    art=soup.find('div',class_='grid-uniform').text
    newarr.append(art)
    return newarr

