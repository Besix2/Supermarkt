import requests
import json
from bs4 import BeautifulSoup
import pymongo
import json
import unicodedata
from task import mongo_add

# url = "https://api.foursquare.com/v3/places/search?ll=52.32%2C13.05&radius=5000&categories=17069&chains=fbac2d50-d890-0132-61d6-7a163eb2a6fc%2Ceaea0f66-7e6d-4c9c-acb2-2653f0c3ff5d%2C16cbce60-992b-0132-fd75-7a163eb2a6fc%2C2fcc4bf0-9c63-0132-6632-3c15c2dde6c8%2Cb0b33b60-d890-0132-61d2-7a163eb2a6fc%2Cabab48f8-0cc2-43e0-a175-05e18078ad1f%2Cfbaac220-d890-0132-61d6-7a163eb2a6fc%2Cfbabe960-d890-0132-61d6-7a163eb2a6fc"
# api_key = "fsq3YmOpN5OSe3VVDGxhghb1fROqrD1U0ztU50aajR0DlQU="

# headers = {
#     "accept": "application/json",
#     "Authorization": api_key
# }
# # location = "52.327999, 13.051232"
# # response = requests.get(url, headers=headers)
# # real_response = json.loads(response.text)
# # for i in real_response["results"]:
# #     print(i["name"] + " " + i["location"]["formatted_address"])

# # page = requests.get("https://www.supermarktcheck.de/rewe/sortiment/9000")
# # soup = BeautifulSoup(page.content, "html.parser")
# # print(soup)
def database():
    client = pymongo.MongoClient("mongodb+srv://max916328:Mongodb_2020@cluster0.v24mw5y.mongodb.net/")
    return client['Sortiment']


def get_max_product_number(Supermarkt_link):
    url = f"https://www.supermarktcheck.de{Supermarkt_link}sortiment/?page=1"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    page_element = soup.find("span", style='line-height:39px;font-weight:bold;')
    page_element_list = page_element.text.strip().split()
    return int(page_element_list[3])
        
        

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")   


    
def sortiment(Supermarkt_link, Supermarkt_name):
    print(Supermarkt_link)
    print(Supermarkt_name)
    with open("progress.txt", "r") as t: 
        paused_loop_start = int(t.read())
    for e in range(paused_loop_start, get_max_product_number(Supermarkt_link)):
        json_list = []
        print(e)
        page = requests.get(f"https://www.supermarktcheck.de{Supermarkt_link}sortiment/?page={e}")
        soup = BeautifulSoup(page.content, "html.parser")
        products_list = soup.find_all("a", class_="h3", href=True)
        for single_product in products_list:
            product_string = single_product["href"]
            product_page = requests.get(f"https://www.supermarktcheck.de/{product_string}")
            product_soup = BeautifulSoup(product_page.content, "html.parser")
            price = product_soup.find("strong")
            json_string = '{{"name" : "{0}", "price" : "{1}"}}'.format(remove_control_characters(single_product.text), price.string)
            product_json = json.loads(json_string)
            json_list.append(product_json)
            mongo_add(Supermarkt_name, json_list)
        
        
        with open("progress.txt", "w") as f:
            f.write(str(e))
            

            
def supermarkets():
    page = requests.get("https://www.supermarktcheck.de/supermarkt-ketten/")
    soup = BeautifulSoup(page.content, "html.parser")
    markets_list = soup.find_all("div", class_="col-6 col-md-4 col-lg-3")
    for market in markets_list:
        market_link_object = market.find("a")
        market_link = market_link_object["href"]
        sortiment(market_link, market.string)
            
supermarkets()

