from selenium import webdriver
from bs4 import BeautifulSoup
import re
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import requests
from pymongo import MongoClient

driver = webdriver.Chrome('./chromedriver 3')  # 드라이버를 실행합니다.
client = MongoClient('mongodb+srv://test:sparta@cluster0.mja2a.mongodb.net/?retryWrites=true&w=majority')
db = client.kimchivergleich

#Kshop
url = "https://k-shop.eu/ko/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url, headers=headers)

driver.get(url)
sleep(1)  # 페이지가 로딩되는 동안 1초 간 기다립니다.
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(7)

req = driver.page_source  # html 정보를 가져옵니다.
driver.quit()  # 정보를 가져왔으므로 드라이버는 꺼줍니다.

# soup = BeautifulSoup(data.text, 'html.parser')
soup = BeautifulSoup(req, 'html.parser')  # 가져온 정보를 beautifulsoup으로 파싱해줍니다.

# products = soup.select("#frm > div > table > tbody > tr")
# products = soup.find_all(text=re.compile('진로 참이슬 프레쉬 16.9도 350ml'))
products = soup.select("#wrapper > div.displayPosition.displayPosition1 > div > div > div")
products = soup.select(
    "#wrapper > div.displayPosition.displayPosition1 > div > div > div:nth-child(3) > div > div.prod-filter.labContent > div.product_list > div > div > div > div > div")

for product in products:
    products_name = product.select_one("div > div > article > div > div.laber-product-description > h2").text
    price = product.select_one(
        "div > div > article > div > div.laber-product-description > div.laber-product-price-and-shipping > span.price").text

    doc = {
        "site_name" : 'Kshop',
        "products_name": products_name,
        "price": price
    }

    db.kimchivergleich.insert_one(doc)

#Kmall
driver.get("https://kmall.de/cat/index/sCategory/1046")
sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

req2 = driver.page_source
driver.quit()

soup2 = BeautifulSoup(req2, 'html.parser')
products2 = soup2.select('body > div.page-wrap > section > div > div.content--wrapper > div > div.listing--wrapper.visible--xl.visible--xl.visible--l.visible--m.visible--s.visible--xs > div.listing--container > div.listing>div')

for product2 in products2:
    product_name2 = product2.select_one('div > div.product--info > a.product--title').text.replace('*','').strip()
    price2 = product2.select_one('div > div.product--info > div.product--price-info > div.product--price-outer > div > span').text.strip(' * ')
    # print(product_name2 , price2)

    doc = {
        "site_name" : 'Kmall',
        "products_name": product_name2,
        "price": price2
    }
    db.kimchivergleich.insert_one(doc)

#Handokmall
driver.get("http://shop7.handokonline.cafe24.com/category/%EB%B2%A0%EC%8A%A4%ED%8A%B8%EC%83%81%ED%92%88/278/")
sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

req3 = driver.page_source
driver.quit()

soup3 = BeautifulSoup(req3, 'html.parser')
products3 = soup3.select('#contents > div.xans-element-.xans-product.xans-product-normalpackage > div.xans-element-.xans-product.xans-product-listnormal.ec-base-product > ul > li')

for product3 in products3:
    product_name3 = product3.select_one('div.description > p.name > a > span:nth-child(2)').text
    price3 = product3.select_one('div.description > ul > li:nth-child(1) > span:nth-child(2)').text
    # print(product_name3,price3)

    doc = {
        "site_name" : 'Handok',
        "products_name": product_name3,
        "price": price3
    }
    db.kimchivergleich.insert_one(doc)