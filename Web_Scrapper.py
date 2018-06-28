# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 21:38:54 2018

@author: Lourenço Neto
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
from time import time
from random import randint
from IPython.core.display import clear_output

#https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168#.WyKR4KdKjIU
"""
page = requests.get("http://dataquestio.github.io/web-scraping-pages/ids_and_classes.html")
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())
#print(list(soup.children))
for item in list(soup.children):
    print(type(item))
#html = list(soup.children)[2]
#body = list(html.children)[3]
#print(list(body.children))
#p = list(body.children)[1]
#print(p.get_text())


#print(soup.find_all('p')[0].get_text())

#print(soup.find_all('p', class_='outer-text'))
print(soup.select("div p"))
"""
"""
url = "https://g1.globo.com/economia/noticia/kassab-diz-que-ainda-e-possivel-fazer-marco-regulatorio-de-telecomunicacoes-em-2018.ghtml"
page = requests.get("https://g1.globo.com/economia/noticia/kassab-diz-que-ainda-e-possivel-fazer-marco-regulatorio-de-telecomunicacoes-em-2018.ghtml")
soup = BeautifulSoup(page.content, 'html.parser')

news_title = soup.find(class_="content-head__title")
print(news_title.get_text())

news_subtitle = soup.find(class_="content-head__subtitle")
print(news_subtitle.get_text())

#first_paragraph = soup.find(class_="content-text__container theme-color-primary-first-letter")
#print(first_paragraph.get_text())

news = soup.select(".content-text__container")
total_news = ""
for paragraph in news:
    print(paragraph.get_text())
    total_news = total_news + paragraph.get_text()

news_dataframe = pd.DataFrame({
        "url": url, 
        "title": news_title.get_text(), 
        "subtitle": news_subtitle.get_text(), 
        "news": [total_news]
    })
    
"""
main_urls = []
main_urls.append("http://g1.globo.com/economia/")
main_urls.append("http://g1.globo.com/politica/")
main_urls.append("http://globoesporte.globo.com/futebol/futebol-internacional/")
main_urls.append("https://gshow.globo.com/Famosos/")
main_urls.append("http://g1.globo.com/pop-arte/cinema/")

titles = []
subtitles = []
news = []
useful_urls = []
real_classification = []
contador = 0
for url in main_urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    #requests = 0
    #start_time = time()
    contador = contador + 1
    urls = soup.select(".feed-post-link")
    
    for links in urls:
        response = requests.get(links.attrs['href'])
        # Pause the loop
        #sleep(randint(8,15))
        
        # Monitor the requests
        #requests += 1
        #elapsed_time = time() - start_time
        #print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
        #clear_output(wait = True)
        new_soup = BeautifulSoup(response.content, 'html.parser')
        #page_html = BeautifulSoup(response.text, 'html.parser')
        news_title = new_soup.find(class_="content-head__title")
        if news_title is not None:
            #print(news_title.get_text())
            useful_urls.append(links.attrs['href'])
            if contador is 1:
                real_classification.append("Economia")
            elif contador is 2:
                real_classification.append("Política")
            elif contador is 3:
                real_classification.append("Futebol")
            elif contador is 4:
                real_classification.append("Celebridades")
            elif contador is 5:
                real_classification.append("Cinema")
            titles.append(news_title.get_text())
            news_subtitle = new_soup.find(class_="content-head__subtitle")
            if news_subtitle is not None:
                subtitles.append(news_subtitle.get_text())
            else:
                subtitles.append(" ")
            news_body = new_soup.select(".content-text__container")
            total_news = ""
            for paragraph in news_body:
                total_news = total_news + paragraph.get_text()
                total_news = total_news + " "
            if total_news is not None:
                news.append(total_news) 
    


news_dataframe = pd.DataFrame({
     "URL": useful_urls, 
     "Título": titles, 
     "SubTítulo": subtitles, 
     "Texto": news,
     "Classificação": real_classification
})
urls_dataframe = pd.DataFrame({
        "url":urls
    })
writer = pd.ExcelWriter('pandas_simple4.xlsx', engine='xlsxwriter')

news_dataframe.to_excel(writer, sheet_name='Sheet1')
writer.save()

print("Quebra")
#print(urls[1].attrs['href'])


#final_paragraph = soup.find(data-track-category_="fim do conteudo")
#print(final_paragraph.prettify())


"""

page = requests.get("http://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")
soup = BeautifulSoup(page.content, 'html.parser')
seven_day = soup.find(id="seven-day-forecast")
forecast_items = seven_day.find_all(class_="tombstone-container")
tonight = forecast_items[0]
print(tonight.prettify())

period = tonight.find(class_="period-name").get_text()
short_desc = tonight.find(class_="short-desc").get_text()
temp = tonight.find(class_="temp").get_text()

print(period)
print(short_desc)
print(temp)

img = tonight.find("img")
desc = img['title']

print(desc)

period_tags = seven_day.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]
for period in periods:
    print(period)

short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]

print(short_descs)
print(temps)
print(descs)

weather = pd.DataFrame({
        "period": periods, 
        "short_desc": short_descs, 
        "temp": temps, 
        "desc":descs
    })
    
temp_nums = weather["temp"].str.extract("(?P<temp_num>\d+)", expand=False)
weather["temp_num"] = temp_nums.astype('int')

is_night = weather["temp"].str.contains("Low")
weather["is_night"] = is_night

"""
"""
for forecast in forecast_items:
    print(forecast.prettify())
    
"""
