import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

class DataManager:

    def __init__(self):
        load_dotenv()
        url = os.getenv("URL_REAL")
        self.HEADERS={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,pl;q=0.6",
            "Priority": "u=0, i",
            "Sec-Ch-Ua": "\"Not;A=Brand\";v=\"99\", \"Opera GX\";v=\"123\", \"Chromium\";v=\"139\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 OPR/123.0.0.0",
            "X-Amzn-Trace-Id": "Root=1-6922ca0f-73396a857071a8bf739fe5f1"
        }
        response = requests.get(url, headers=self.HEADERS)
        response.raise_for_status()
        self.soup = BeautifulSoup(response.text, "html.parser")
        self.list_of_properties = None
        self.info = []
        self.isOk = True

    def get_price(self, item):
        price = item.select_one('span[class^="PropertyCardWrapper__StyledPriceLine"]')
        if price:
            price = price.getText()
            index = price.index(price[-1])
            try:
                index = price.index("+")
            except ValueError:
                index = price.index("/")
            finally:
                price = price[:index]
        else:
            self.isOk = False
        return price

    def get_link(self, item):
        link = item.select_one('a[class^="Anchor-c11n"]')
        if link:
            link = link.get_attribute_list("href")[0]
        else:
            self.isOk = False
        return link

    def get_address(self, item):
        address = item.find("address")
        if address:
            address = address.getText().replace("| ", "").strip()
        else:
            self.isOk = False
        return address

    def update_info(self):
        self.list_of_properties = self.soup.select('ul li[class^="ListItem-c11n"]')
        print(self.list_of_properties)
        self.info=[]
        for flat in self.list_of_properties:
            self.isOk=True
            new_record={
                "address" : self.get_address(flat),
                "price" : self.get_price(flat),
                "link" : self.get_link(flat)
            }
            if self.isOk:
                self.info.append(new_record)

    def get_info(self):
        return self.info
