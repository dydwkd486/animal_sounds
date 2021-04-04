import sys
#-*- coding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
from PIL import Image,ImageDraw,ImageFont
import psycopg2
import argparse
import math
import pandas as pd
from collections import Counter

# url= urlopen('https://www.naturing.net/o/card?observation_name&order_code=mammals%2Cbirds%2Creptilia%2Camphibians%2Cbugs&habitat_code&area&help_name_yn&match_case=N&observe_date1&observe_date2&create_date1&create_date2&obs_filter=0&follow_yn&photo_yn=Y&type&draft_yn&lat1&lng1&lat2&lng2&page=0')
# bsObject = BeautifulSoup(url, "html.parser")
# last_page=float(bsObject.find("div",{"id":"paging"}).get("data-total-count"))/float(bsObject.find("div",{"id":"paging"}).get("data-page-size"))
# print(math.ceil(last_page))
#
# name=[]
# for page in range(math.ceil(last_page)):
#     print(page)
#     html = urlopen(
#         "https://www.naturing.net/o/card?observation_name&order_code=mammals%2Cbirds%2Creptilia%2Camphibians%2Cbugs&habitat_code&area&help_name_yn&match_case=N&observe_date1&observe_date2&create_date1&create_date2&obs_filter=0&follow_yn&photo_yn=Y&type&draft_yn&lat1&lng1&lat2&lng2&page=" + str(
#             page))
#     bsObject = BeautifulSoup(html, "html.parser")
#     for link in bsObject.find_all("div", {"class": "observation-item__name"}):
#         # print(link.text.strip())
#         name.append(link.text.strip())
#
#
# for w, c in Counter(name).most_common(100):
#         print(w, c)
namelist=['제비','멧비둘기','참새','왜가리','직박구리','도롱뇽','저어새','까치','박새','흰뺨검둥오리','계곡산개구리','청둥오리','물까치','북방산개구리','청개구리']
# Hirundo rustica , Streptopelia orientalis ,Passer montanus , Ardea cinerea , Hypsipetes amaurotis , Hynobius leechii , Platalea minor , Pica serica , Parus minor , Anas zonorhyncha , Rana huanrenensis , Anas platyrhynchos, ,Cyanopica cyanus,Rana dybowskii, Hyla japonica
namelist=['저어새']
for name in namelist:
    data = pd.DataFrame()
    print(type(str(name)))
    path = "https://www.naturing.net/o/card?observation_name="+urllib.parse.quote_plus(name)+"&order_code=&habitat_code=&area=&help_name_yn=&match_case=Y&observe_date1=&observe_date2=&create_date1=&create_date2=&obs_filter=0&follow_yn=&photo_yn=Y&type=&draft_yn=&lat1=&lng1=&lat2=&lng2=&page=0"
    print(path)
    url= urlopen(path)
    bsObject = BeautifulSoup(url, "html.parser")
    last_page=float(bsObject.find("div",{"id":"paging"}).get("data-total-count"))/float(bsObject.find("div",{"id":"paging"}).get("data-page-size"))
    print(math.ceil(last_page))
    for page in range(math.ceil(last_page)):
        print(page)
        html = urlopen(
            'https://www.naturing.net/o/card?observation_name='+urllib.parse.quote_plus(name)+'&order_code=&habitat_code=&area=&help_name_yn=&match_case=Y&observe_date1=&observe_date2=&create_date1=&create_date2=&obs_filter=0&follow_yn=&photo_yn=Y&type=&draft_yn=&lat1=&lng1=&lat2=&lng2=&page=' + str(
                page))
        bsObject = BeautifulSoup(html, "html.parser")
        for link in bsObject.find_all("a", {"class": "observationView b-itemlist__item__link observation-item__link"}):
            # print("https://www.naturing.net/o/"+link.get('href'))
            html_sub = urlopen("https://www.naturing.net/o/" + link.get('href'))
            bsObject_sub = BeautifulSoup(html_sub, "html.parser")
            try:
                id = link.get('href')
                # print(id)  # id
                Latitude = bsObject_sub.find("div", {"id": "map"}).get("data-lat")
                Latitude = ("{:.7f}".format(float(Latitude)))
                # print(Latitude)  # 좌표 lat
                Longitude = bsObject_sub.find("div", {"id": "map"}).get("data-lng")
                Longitude = ("{:.7f}".format(float(Longitude)))
                # print(Longitude)  # 좌표 lng
                data=data.append(pd.DataFrame({'id':[id],'name':[name],'latitude':[Latitude],'longitude':[Longitude]}))
            except AttributeError:
                pass
            except ValueError:
                pass

    data.to_csv(name+".csv")