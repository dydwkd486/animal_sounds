import urllib.request
import json

url = 'http://lod.nature.go.kr/data/Pelophylax_chosenicus_Okada_1952?output=json'  # 요청할 주소

text_data = urllib.request.urlopen(url).read().decode('utf-8')

animals = json.loads(text_data)
for i in animals:
    for j in animals[i]:
        #print(j)
        if(animals[i][j][0]["type"]=="literal"):
            print(animals[i][j][0]["value"])