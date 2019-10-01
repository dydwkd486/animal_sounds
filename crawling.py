#-*- coding: cp949 -*-
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
from PIL import Image,ImageDraw,ImageFont
import psycopg2
import argparse

'''
1. �̹��� ���� 0
2. ������ �̹����� ���۱� �����ֱ� 0
3. ������ ���̽��� �����Ҽ��ְ� �ڵ�ȭ 0
4. �������� �ٷ� �����Ҽ��ְ� �����ϱ�

'''
## ���� ������, ������ ������, ��� ���̵�, ��й�ȣ, �̹��� ����
parse = argparse.ArgumentParser(description="�׽�Ʈ�Դϴ�.")
parse.add_argument('--startpage',required=False, default=1, help="���� ������ ��")
parse.add_argument('--id',required=False, default='postgres',help="��� ���̵�")
parse.add_argument('--passward',required=False,default='password', help="��� ��й�ȣ")
parse.add_argument('--folder',required=False, default='./', help="�̹��� ���� ��ġ")

def image_save(x,y):

    urllib.request.urlretrieve(x,"./"+args.folder+y+".jpg")

def modify(x,y):
    target_image=Image.open("./"+args.folder+x+".jpg")
    width, height = target_image.size
    draw = ImageDraw.Draw(target_image)
    font = ImageFont.truetype("gulim.ttc",size=30)
    draw.text((0,0),y,font=font,fill='blue')
    target_image.save("./"+args.folder+x+".jpg")

args= parse.parse_args()

print(args.startpage)
print(args.id)
print(args.passward)
print(args.folder)

# ���� ������ ����
html = urlopen("https://www.naturing.net/o/thumbnail?observation_name=&order_code=mammals%2Cbirds%2Creptilia%2Camphibians%2Cbugs&habitat_code=&area=&help_name_yn=N&match_case=N&observe_date1=&observe_date2=&create_date1=&create_date2=&obs_filter=0&follow_yn=&photo_yn=Y&type=&draft_yn=&lat1=&lng1=&lat2=&lng2=&page=0")
bsObject = BeautifulSoup(html, "html.parser")

#print(bsObject)
# �� ������ ����
for link in bsObject.find_all("a", {"class":"observationView b-itemlist__item__link observation-item__link"}):
    # print("https://www.naturing.net/o/"+link.get('href'))
    html_sub = urlopen("https://www.naturing.net/o/" + link.get('href'))
    bsObject_sub = BeautifulSoup(html_sub, "html.parser")
    try:
        id = link.get('href')
        print(id)  # id
        Latitude=bsObject_sub.find("div", {"id": "map"}).get("data-lat")
        print(Latitude)  # ��ǥ lat
        Longitude=bsObject_sub.find("div", {"id": "map"}).get("data-lng")
        print(Longitude)  # ��ǥ lng
        title=bsObject_sub.find("meta", {"property": "og:title"}).get("content")
        print(title)  # �ѱ� �̸�.
        try:
            print(bsObject_sub.find_all("a", {"class": "obsinfo__link b-btn"})[1].get("href").split("https://en.wikipedia.org/wiki/")[1])  # ���� �̸�. ���� ���ϴ� ��...
        except IndexError:
            pass
        print(bsObject_sub.find("meta", {"property": "og:image"}).get("content"))  # ���� �ϳ�
        image_save(bsObject_sub.find("meta", {"property": "og:image"}).get("content"),id)

        animalclass=bsObject_sub.find("div", {"id": "map"}).get("data-order_code")
        print(animalclass)  # ���� �з� ����

        print(" ".join(bsObject_sub.find("div", {"class": "obsinfo__item-content"}).text.split()))  # �ּ�
        observed_date=bsObject_sub.find_all("div", {"class": "obsinfo__item-content"})[3].text.strip()
        observed_date=observed_date.replace("�� ","-").replace("�� ","-").split("�� ")[0]
        print(observed_date)  # ���� ��¥
        created_date=bsObject_sub.find("p", {"class": "obsauthor__post-time"}).text.strip()
        created_date = created_date.replace("�� ", "-").replace("�� ", "-").split("�� ")[0]
        print(created_date)  # ��� ��¥
        writer=bsObject_sub.find("p", {"class": "obsauthor__name"}).text.strip()
        print(writer)  # �����
        cc="(C) " + bsObject_sub.find("p", {"class": "obsauthor__name"}).text.strip() + " at ����ó��"
        modify(id,cc)

        animalclass="i"
        address="a"
        imagefile="/img/"+id+".jpg"
        soundfile="sound/170605_������_�ݰ�����1.wav"
        #������ ���̽��� ����
        conn_string = "host='localhost' dbname ='django_test' user='"+args.id+"' password='"+args.passward+"'"
        conn = psycopg2.connect(conn_string)
        cur= conn.cursor()
        cur.execute('select id from blog_animal_map where id='+id+';')
        result= cur.fetchall()
        if result==[]:
            cur.execute('insert into blog_animal_map(id, writer , animalclass, title, "Latitude", "Longitude", address, imagefile, soundfile, observed_date, created_date ) values ('+id+",'"+writer+"','"+animalclass+"','"+title+"','"+Latitude+"','"+Longitude+"','"+address+"','"+imagefile+"','"+soundfile+"','"+observed_date+"','"+created_date+"');")
            conn.commit()
    except AttributeError:
        pass



