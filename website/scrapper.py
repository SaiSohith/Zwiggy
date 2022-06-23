import requests
import json
from bs4 import BeautifulSoup


def getrestaurant_img(name):
    page = requests.get(
        f'https://www.google.com/search?q={name}+restaurant+images')
    soup = BeautifulSoup(page.content, 'html.parser')
    img = soup.find_all("img", {"class": "WddBJd"})
    print(img)
    return img
