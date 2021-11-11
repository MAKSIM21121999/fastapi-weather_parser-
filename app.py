from fastapi import FastAPI

import requests
from transliterate import translit, get_available_language_codes
from bs4 import BeautifulSoup as BS

message = ""

def weather(city):
    r = requests.get('https://sinoptik.ua/погода-' + city)
    html = BS(r.content, 'html.parser')

    for el in html.select('#content'):
        t_min = el.select('.temperature .min')[0].text
        t_max = el.select('.temperature .max')[0].text
        t_nightone = el.select('.temperature .p1 ')[0].text
        text = el.select('.wDescription .description')[0].text
        message = ("Привет, погода на сегодня:" + t_min + ', ' + t_max + ', ' + t_nightone + '' + text)
    return message
app = FastAPI()

@app.get("/weather/{city_name}")
async def read_item(city_name):
    alarm = weather(city=city_name)
    city_name_t = translit(city_name, reversed=True)
    return {"weather_info_for_" + city_name_t : alarm}