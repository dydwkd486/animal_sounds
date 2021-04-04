#-*- coding: cp949 -*-
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
from PIL import Image,ImageDraw,ImageFont
import psycopg2
import argparse
import math

'''
1. �̹��� ���� 0
2. ������ �̹����� ���۱� �����ֱ� 0
3. ������ ���̽��� �����Ҽ��ְ� �ڵ�ȭ 0
4. �������� �ٷ� �����Ҽ��ְ� �����ϱ�
DELETE FROM public.blog_animal_map WHERE id BETWEEN 382226 AND 383755;
DELETE FROM public.blog_animal_map;
DELETE FROM public.blog_animal_sub_file ;
DELETE FROM blog_animal_sub_file ;
DELETE FROM blog_animal_map;

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
    font = ImageFont.truetype("gulim.ttf",size=30)
    draw.text((0,0),y,font=font,fill='blue')
    target_image.save("./"+args.folder+x+".jpg")

args= parse.parse_args()

print(args.startpage)
print(args.id)
print(args.passward)
print(args.folder)
html = urlopen("https://www.naturing.net/o/thumbnail?observation_name=&order_code=mammals%2Cbirds%2Creptilia%2Camphibians%2Cbugs&habitat_code=&area=&help_name_yn=N&match_case=N&observe_date1=&observe_date2=&create_date1=&create_date2=&obs_filter=0&follow_yn=&photo_yn=Y&type=&draft_yn=&lat1=&lng1=&lat2=&lng2=&page=0")
bsObject = BeautifulSoup(html, "html.parser")
last_page=float(bsObject.find("div",{"id":"paging"}).get("data-total-count"))/float(bsObject.find("div",{"id":"paging"}).get("data-page-size"))
print(math.ceil(last_page))

for page in range(math.ceil(last_page)):
    print(page)
    # ���� ������ ����
    html = urlopen("https://www.naturing.net/o/thumbnail?observation_name=&order_code=mammals%2Cbirds%2Creptilia%2Camphibians%2Cbugs&habitat_code=&area=&help_name_yn=N&match_case=N&observe_date1=&observe_date2=&create_date1=&create_date2=&obs_filter=0&follow_yn=&photo_yn=Y&type=&draft_yn=&lat1=&lng1=&lat2=&lng2=&page="+str(page))
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
            Latitude=("{:.7f}".format(float(Latitude)))
            print(Latitude)  # ��ǥ lat
            Longitude=bsObject_sub.find("div", {"id": "map"}).get("data-lng")
            Longitude = ("{:.7f}".format(float(Longitude)))
            print(Longitude)  # ��ǥ lng
            title=bsObject_sub.find("meta", {"property": "og:title"}).get("content")
            print(title)  # �ѱ� �̸�.
            try:
                print(bsObject_sub.find_all("a", {"class": "obsinfo__link b-btn"})[1].get("href").split("https://en.wikipedia.org/wiki/")[1])  # ���� �̸�. ���� ���ϴ� ��...
            except IndexError:
                pass
            #print(bsObject_sub.find("meta", {"property": "og:image"}).get("content"))  # ���� �ϳ�
            image_save(bsObject_sub.find("meta", {"property": "og:image"}).get("content"),id)

            animalclass=bsObject_sub.find("div", {"id": "map"}).get("data-order_code")
            if animalclass=='bugs': #����
                animalclass="i"
            elif animalclass=='birds': #��
                animalclass="b"
            elif animalclass=='mammals': #������
                animalclass="m"
            elif animalclass=='amphibians': #�缭��
                animalclass="a"
            elif animalclass=='reptilia': #�����
                animalclass="r"

            print(animalclass)  # ���� �з� ����

            print(" ".join(bsObject_sub.find("div", {"class": "obsinfo__item-content"}).text.split()))  # �ּ�
            address = " ".join(bsObject_sub.find("div", {"class": "obsinfo__item-content"}).text.split())
            addresssub = address.split(" ")[0]
            print(addresssub)
            if addresssub=='����':
                addresssub="a"
            elif addresssub=='���'or addresssub=='��⵵': #��
                addresssub="b"
            elif addresssub=='����': #������
                addresssub="c"
            elif addresssub=='�泲' or addresssub=='��û����': #�缭��
                addresssub="d"
            elif addresssub=='���' or addresssub=='��û�ϵ�': #�����
                addresssub="e"
            elif addresssub=='�泲' or addresssub=='��󳲵�': #��
                addresssub="f"
            elif addresssub=='���' or addresssub=='���ϵ�': #������
                addresssub="g"
            elif addresssub=='����' or addresssub=='���󳲵�' or addresssub=='����': #�缭��
                addresssub="h"
            elif addresssub=='����' or  addresssub == '����ϵ�': #�����
                addresssub="i"
            elif addresssub=='����Ư����ġ��': #��
                addresssub="j"
            elif addresssub=='����Ư����ġ��': #������
                addresssub="l"
            elif addresssub=='��õ������' or addresssub=='��õ': #�缭��
                addresssub="m"
            elif addresssub=='����': #�����
                addresssub="n"
            elif addresssub=='���': #��
                addresssub="o"
            elif addresssub=='�뱸': #������
                addresssub="p"
            elif addresssub=='�λ�' or addresssub == '�λ걤����': #�缭��
                addresssub="q"
            observed_date=bsObject_sub.find_all("div", {"class": "obsinfo__item-content"})[3].text.strip()

            created_date=bsObject_sub.find("p", {"class": "obsauthor__post-time"}).text.strip()
            created_date = created_date.replace("�� ", "-").replace("�� ", "-").split("�� ")[0]
            #print(created_date)  # ��� ��¥
            observed_date = observed_date.replace("�� ", "-").replace("�� ", "-").split("�� ")[0]
            if observed_date == '0000-0-0':
                observed_date=created_date

            #print(observed_date)  # ���� ��¥


            writer=bsObject_sub.find("p", {"class": "obsauthor__name"}).text.strip()
            #print(writer)  # �����
            cc="(C) " + bsObject_sub.find("p", {"class": "obsauthor__name"}).text.strip() + " at ����ó��"
            modify(id,cc)


            imagefile="/img/"+id+".jpg"
            soundfile="sound/170605_������_�ݰ�����1.wav"
            file = 'subsound/subFile0.wav'
            start_point = "6.4319340"
            end_point = "16.3211867"

            # ������ ���̽��� ����
            conn_string = "host='localhost' dbname ='django_test' user='"+args.id+"' password='"+args.passward+"'"
            conn = psycopg2.connect(conn_string)
            cur= conn.cursor()
            cur.execute('select id from blog_animal_map where id='+id+';')
            result= cur.fetchall()
            if result==[]:
                print('insert into blog_animal_map(id, writer , animalclass, title, "Latitude", "Longitude", address, imagefile, soundfile, observed_date, created_date ) values ('+id+",'"+writer+"','"+animalclass+"','"+title+"','"+Latitude+"','"+Longitude+"','"+addresssub+"','"+imagefile+"','"+soundfile+"','"+observed_date+"','"+created_date+"');")
                cur.execute('insert into blog_animal_map(id, writer , animalclass, title, "Latitude", "Longitude", address, imagefile, soundfile, observed_date, created_date ) values ('+id+",'"+writer+"','"+animalclass+"','"+title+"','"+Latitude+"','"+Longitude+"','"+addresssub+"','"+imagefile+"','"+soundfile+"','"+observed_date+"','"+created_date+"');")
                cur.execute('insert into blog_animal_sub_file(id,file,start_point,end_point,"Animal_map_id") values ('+id+",'"+file+"','"+start_point+"','"+end_point+"','"+id+"');")
                conn.commit()

        except AttributeError:
            pass
    break

