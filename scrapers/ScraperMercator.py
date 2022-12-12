import json
import sys
from random import randint
from time import sleep

import requests
from bs4 import BeautifulSoup


class ScraperMercator():
    def __init__(self, fetch_limit, fetch_offset, waiting_time):
        self.fetch_limit = fetch_limit
        self.fetch_offset = fetch_offset
        self.url = \
            f"https://trgovina.mercator.si/market/products/browseProducts/getProducts?limit={self.fetch_limit}&offset={self.fetch_offset}&filterData%5Bcategories%5D=14535405%2C14535446%2C14535463%2C14535481%2C14535505%2C14535512%2C14535548%2C14535588%2C14535612%2C14535637%2C14535661%2C14535681%2C14535711%2C14535736%2C14535749%2C14535803%2C14535810%2C16873196&filterData%5Boffset%5D=2&from={self.fetch_offset * self.fetch_limit}&_=1656771045265"
        self.waiting_time = waiting_time

        self.api_endpoint = "http://localhost:8082/product/add"

    def fetch_data(self):
        response = requests.get(self.url)
        data = response.json()
        return data if len(data) > 0 else None

    def get_allergens(self, data):
        allergens = ""
        for allergen_data in data["data"]["allergens"]:
            allergen = allergen_data["value"]
            if "70_true" in allergen or "70_mixed" in allergen:
                allergens += "jajca, "
            elif "71_true" in allergen or "71_mixed" in allergen:
                allergens += "oreščke, "
            elif "72_true" in allergen or "72_mixed" in allergen:
                allergens += "gluten, "
            elif "73_true" in allergen or "73_mixed" in allergen:
                allergens += "mleko, "
            elif "74_true" in allergen or "74_mixed" in allergen:
                allergens += "sojo, "
            elif "75_true" in allergen or "75_mixed" in allergen:
                allergens += "arašide, "
            elif "76_true" in allergen or "76_mixed" in allergen:
                allergens += "zeleno, "
            elif "77_true" in allergen or "77_mixed" in allergen:
                allergens += "ribe, "
            elif "78_true" in allergen or "78_mixed" in allergen:
                allergens += "rake, "
            elif "79_true" in allergen or "79_mixed" in allergen:
                allergens += "gorčično seme, "
            elif "80_true" in allergen or "80_mixed" in allergen:
                allergens += "sezam, "
            elif "81_true" in allergen or "81_mixed" in allergen:
                allergens += "SO2 - Žveplov dioksid (več kot 10mg/kg ali 10mg/l), "
            elif "82_true" in allergen or "82_mixed" in allergen:
                allergens += "volčji bob, "
            elif "83_true" in allergen or "83_mixed" in allergen:
                allergens += "mehkužce, "

        return "Izdelek vsebuje " + allergens[0: allergens.rfind(", ")] if len(allergens) > 0 else None

    def get_ingredients(self, data):
        url = "https://trgovina.mercator.si" + data["url"][0: str(data["url"]).rfind("/")]
        response = requests.get(url)
        doc = BeautifulSoup(response.text, "html.parser")
        return doc.find(id="product_group_2").text.strip() if doc.find(
            id="product_group_2") is not None else None  # preveri ali izdelek vsebuje sestavine

    def get_nutrition_values(self,
                             data):  # pridobi tabelo hranilnih vrednosti, podatki so shranjeni v naslednji obliki [ime hranilne vrednosti:količina:enota$] (: loči stolpce, $ loči vrstice)

        url = "https://trgovina.mercator.si" + data["url"][0: str(data["url"]).rfind("/")]
        response = requests.get(url)
        doc = BeautifulSoup(response.text, "html.parser")

        nutrition_values = ""
        for line in doc.find_all("tr"):
            for col in line.find_all("th"):  # dobi header tabele
                if str(col.text) != "\n":
                    nutrition_values += str(col.text).lstrip().strip() + ":"
            for col in line.find_all("td"):  # dobi vsebino tabele
                if str(col.text) != "\n":
                    nutrition_values += str(col.text).lstrip().strip() + ":"
            nutrition_values += "$"

        return nutrition_values.replace(":$", "$") if len(nutrition_values) > 0 else None

    def extract_data(self, data):  # izlušči samo zanimive podatke
        extraced_data = dict()
        if "data" in data:
            for barcode in data["data"]["gtins"]:
                extraced_data[barcode["gtin"]] = {
                    "barcode": barcode["gtin"],
                    "itemId": data["itemId"],
                    "name": data["data"]["name"],
                    "brandName": data["data"]["brand_name"],
                    "mainImageSrc": data["mainImageSrc"],
                    "allergens": self.get_allergens(data),
                    "ingredients": self.get_ingredients(data),
                    "nutritionValues": self.get_nutrition_values(data),
                    "url": "https://trgovina.mercator.si" + data["url"][0: str(data["url"]).rfind("/")],
                }
            return extraced_data
        else:
            return None  # v primeru da api vrne reklamo vrni None

    def to_json(self, data: dict):
        return json.dumps(data)

    def save(self, data: dict):  # shrani podatke na reddis preko POST requesta
        for k, v in data.items():
            r = requests.post(url=self.api_endpoint, data=v)
            with open('output.log', 'a') as sys.stdout:
                print(r.text)
                sys.stdout.flush()

    def work(self):
        response = self.fetch_data()  # pridobi podatke
        while response is not None:
            with open('output.log', 'a') as sys.stdout:
                print()
                print("OFFSET: ", self.fetch_offset)
                print("URL: ", self.url)
                print()
                sys.stdout.flush()
            for data in response:
                exctracted_data = self.extract_data(data)  # izlušči potrebne podatke
                if exctracted_data is not None:
                    self.save(exctracted_data)  # shrani podatke

            self.fetch_offset += 1  # povečamo odmik da dobimo nove izdelke
            self.url = \
                f"https://trgovina.mercator.si/market/products/browseProducts/getProducts?limit={self.fetch_limit}&offset={self.fetch_offset}&filterData%5Bcategories%5D=14535405%2C14535446%2C14535463%2C14535481%2C14535505%2C14535512%2C14535548%2C14535588%2C14535612%2C14535637%2C14535661%2C14535681%2C14535711%2C14535736%2C14535749%2C14535803%2C14535810%2C16873196&filterData%5Boffset%5D=2&from={self.fetch_offset * self.fetch_limit}&_=1656771045265"

            sleep(randint(0, self.waiting_time))  # naključni interval čakanja
            # exit(0)
            response = self.fetch_data()
