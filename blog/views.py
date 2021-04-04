from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404,HttpResponse
from .models import Animal_map, Animal_total_info,district,Animal_Sub_file
from .forms import Animal_mapForm,AnimalmapFormMultiform,Animal_classForm
from django.core.exceptions import ObjectDoesNotExist
from urllib.request import HTTPError
''' 승원 수정 부분 '''
from .forms import Animal_Sub_fileForm
from accounts.models import Profile
from django.db.models import Sum
from django.db.models import Avg
from django.db.models import Max
from django.db.models import Min
''' end 승원 수정 부분 '''
import urllib.request
import json
import re
from django.http import HttpResponseRedirect

from SPARQLWrapper import SPARQLWrapper, JSON
import xml.etree.ElementTree as ET

'''머신러닝'''
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["CUDA_VISIBLE_DEVICES"] = '-1'

import time
import librosa
import numpy as np
import tensorflow as tf
from datetime import datetime
# from modules.models import Model, Solver, nClass, Feature_class, cos_sim
# from modules.models import Model,Solver, nClass, Feature_class, cos_sim
from Aniaml_demo.ISPL_DEMO import Model,Solver,nClass
model_A = Model('A')
sess = tf.Session()
model_A_solver = Solver(sess, model_A)
sess.run(tf.global_variables_initializer())
saver = tf.train.Saver(max_to_keep=1, var_list=tf.global_variables())
saver.restore(sess,tf.train.latest_checkpoint('./Aniaml_demo/CKT_DEMO_mask'))
'''머신러닝'''

import xml.etree.ElementTree as elemTree # LOD
from django_user_agents.utils import get_user_agent

reg_b = re.compile(
    r"(android|bb\\d+|meego).+mobile|avantgo|bada\\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\\.(browser|link)|vodafone|wap|windows ce|xda|xiino",
    re.I | re.M)
reg_v = re.compile(
    r"1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|\\-[a-w])|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|sk\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\\-|your|zeto|zte\\-",
    re.I | re.M)


class DetectMobileBrowser():
    def process_request(self, request):
        request.mobile = False
        if request.META.get('HTTP_USER_AGENT'):
            user_agent = request.META['HTTP_USER_AGENT']
            print(request)
            b = reg_b.search(user_agent)
            v = reg_v.search(user_agent[0:4])
            if b or v:
                return render(request, 'test.html')

def test(request):
    DetectMobileBrowser().process_request(request)
    return render(request, 'test.html')

#@login_required
def home(request):

    # Do stuff here...
    animap = Animal_map.objects.filter()

    file_meta_dict = dict()
    # file size stat
    query = Animal_map.objects.aggregate(file_size_avg=Avg('file_size_input'), file_size_max=Max('file_size_input'),
                                         file_size_min=Min('file_size_input'))

    for p in query:
        # print(p)
        # print(query[p])
        file_meta_dict[p] = query[p]

    # file duration stat
    query = Animal_map.objects.aggregate(file_duration_avg=Avg('duration_input'),
                                         file_duration_max=Max('duration_input'),
                                         file_duration_min=Min('duration_input'))

    for p in query:
        # print(p)
        # print(query[p])
        file_meta_dict[p] = query[p]

    # writer stat
    query = Animal_map.objects.raw("SELECT writer as id, count(*) as cnt FROM blog_animal_map group by writer")
    # print(query)
    writer_dict = dict()
    for p in query:
        # print(p)
        # print(p.id)
        # print(p.cnt)
        writer_dict[p.id] = p.cnt
    file_meta_dict['file_count_writer'] = writer_dict

    query = Animal_map.objects.raw(
        "SELECT writer as id, count(*) as cnt FROM blog_animal_map where observed_date >= '2010-02-10' and observed_date <= '2010-02-10' group by writer")
    # print(query)
    writer_data_dict = dict()
    for p in query:
        # print(p)
        # print(p.id)
        # print(p.cnt)
        writer_data_dict[p.id] = p.cnt
    file_meta_dict['file_count_writer_given_date'] = writer_data_dict

    # file extension stat
    query = Animal_map.objects.raw(
        "SELECT file_ex_input as id, count(*) as cnt FROM blog_animal_map group by file_ex_input")
    # print(query)
    file_ex_dict = dict()
    for p in query:
        # print(p)
        # print(p.id)
        # print(p.cnt)
        file_ex_dict[p.id] = p.cnt
    file_meta_dict['file_count_ex'] = file_ex_dict
    '''
    # class stat
    query = Animal_map.objects.raw(
        "SELECT count(*) as cnt, class as id FROM blog_animal_map group by class")
    print(query)
    for p in query:
        print(p)
        print(p.id)
        print(p.cnt)
    '''

    # title stat
    query = Animal_map.objects.raw(
        "SELECT title as id, count(*) as cnt FROM blog_animal_map group by title")
    # print("query: ",query)
    title_dict = dict()
    for p in query:
        # print(p)
        # print(p.id)
        # print(p.cnt)
        title_dict[p.id] = p.cnt
    file_meta_dict['file_count_ex'] = title_dict

    # address stat
    query = Animal_map.objects.raw(
        "SELECT address as id, count(*) as cnt FROM blog_animal_map group by address")
    # print(query)
    address_dict = dict()
    for p in query:
        # print(p)
        # print(p.id)
        # print(p.cnt)
        # print(Animal_map.ADDRESS_DICT[p.id])
        address_dict[Animal_map.ADDRESS_DICT[p.id]] = p.cnt
    file_meta_dict['file_count_address'] = address_dict
    print(file_meta_dict)
    # json_val = json.dumps(file_meta_dict, ensure_ascii=False)
    # print(json_val)

    animal_maps = Animal_map.objects.filter()
    # 조건이 6가지 (이름, 구분, 지역, 시작날짜, 끝날짜, 맵다시확인)
    count = 100
    query = ""
    sw_lat = "0"
    sw_lng = "0"
    ne_lat = "180"
    ne_lng = "180"
    address = "abcdefghijk"
    class_key = "mbrai"
    startdate = "1900-03-06"
    enddate = "2200-03-06"
    results = []
    print("enddate", enddate)
    if request.GET.get('search_key'):
        query = request.GET['search_key']
        print("search_key")

    if request.GET.get('sw_lat'):
        sw_lat = request.GET['sw_lat']
        sw_lng = request.GET['sw_lng']
        ne_lat = request.GET['ne_lat']
        ne_lng = request.GET['ne_lng']

    if request.GET.get('address_key'):
        address = request.GET['address_key']
        # print("address")

    if request.GET.get('class_key'):
        class_key = request.GET['class_key']
        # print(class_key)

    if request.GET.get('startdate'):
        startdate = request.GET['startdate']
        # print("startdate",startdate)

    if request.GET.get('enddate'):
        enddate = request.GET['enddate']
        # print("enddate",enddate)
    if request.GET.get('count'):
        count = request.GET['count']
        # print("count",count)
    for odject in animal_maps.filter(Longitude__range=(sw_lng, ne_lng), Latitude__range=(sw_lat, ne_lat),
                                     title__contains=query, address__in=address, animalclass__in=class_key,
                                     observed_date__range=(startdate, enddate)).order_by('-observed_date'):
        results.append(odject)

    count = 100

    context = {'animal_maps': results[:count]}

    user_agent = get_user_agent(request)

    if user_agent.is_mobile:
        print("모바일")
        return render(request, 'mobile/home_m.html', context)
        # Do other stuff...
    elif user_agent.is_pc :
        print("pc")
        return render(request, 'home.html', context)



''' 승원 수정 부분 '''
def save(request):
    if request.method == "POST":
        form = AnimalmapFormMultiform(request.POST, request.FILES)
        if form.is_valid():
            animal = form['animal_map'].save(commit=False)

            Latitude = request.POST['animal_map-Latitude']  # 위도
            Longitude = request.POST['animal_map-Longitude']  # 경도
            url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + Latitude + "," + Longitude + "&key=AIzaSyDWV0tlx-1gtFEIJPEdpIFWdGGghKB34xk&language=ko"
            text_data = urllib.request.urlopen(url).read().decode('utf-8')
            address = json.loads(text_data)
            print(address['results'][0]['address_components'][0])
            for a in address['results'][0]['address_components']:
                for i in a['types']:
                    if (i == "administrative_area_level_1"):
                        print("administrative_area_level_1 :", a['long_name'])
                        animal.address1 = a['long_name']
                    elif (i == "locality"):
                        print("locality :", a['long_name'])
                        animal.address2 = a['long_name']
                    elif (i == "sublocality_level_1"):
                        print("sublocality_level_1 :", a['long_name'])
                        animal.address3 = a['long_name']
                    elif (i == "sublocality_level_2"):
                        print("sublocality_level_2 :", a['long_name'])
                        animal.address4 = a['long_name']
                    elif (i == "sublocality_level_3"):
                        print("sublocality_level_3 :", a['long_name'])
                        animal.address5 = a['long_name']
                    elif (i == "sublocality_level_4"):
                        print("sublocality_level_4 :", a['long_name'])
                        animal.address6 = a['long_name']

            animal.writer = request.user
            animal.file_size_input = request.POST['file_size_input']
            animal.file_name_input = request.POST['file_name_input']
            animal.file_ex_input = request.POST['file_ex_input']
            animal.duration_input = request.POST['duration_input']
            animal.Latitude = request.POST['animal_map-Latitude']  # 위도
            animal.Longitude = request.POST['animal_map-Longitude']  # 경도
            animal.title1 = request.POST['animal_map-content']

            animal.save()

            num = 0
            print("request.POST:")
            print(request.POST)
            print(request.POST.get('subfile_meta%d' % num))

            # print("url:",url)

            while request.POST.get('subfile_meta%d' % num):
                subfile = Animal_Sub_fileForm().save(commit=False)
                subfile_meta = request.POST.get('subfile_meta%d' % num)
                tokens = subfile_meta.split(",")
                subfile.Animal_map = animal
                subfile.file = request.FILES.get('subfile%d' % num)
                subfile.label = tokens[6]
                subfile.start_point = float(tokens[3])
                subfile.end_point = float(tokens[4])
                subfile.save()
                print("save")
                num += 1

            return redirect('/')
        else:
            print(form)
            animal = form['animal_map'].save(commit=False)
            animal.writer = request.user
            animal.file_size_input = request.POST['file_size_input']
            animal.file_name_input = request.POST['file_name_input']
            animal.file_ex_input = request.POST['file_ex_input']
            animal.duration_input = request.POST['duration_input']
            animal.save()
            return redirect('/')
    else:
        form = AnimalmapFormMultiform()
    user_agent = get_user_agent(request)

    # 모바일 pc 확인
    if user_agent.is_mobile:
        print("모바일")
        return render(request, 'mobile/animalsave.html', {'form': form})
    if user_agent.is_pc:
        print("pc")
        return render(request, 'animalsave.html', {'form': form})
''' end 승원 수정 부분 '''

def list1(request):
    count = 1
    if request.GET.get('page'):
        count = int(request.GET['page'])
    animal_maps = Animal_map.objects.filter().order_by('-observed_date')[(count - 1) * 10:count * 10]
    print(animal_maps)
    sub_results = []
    for odject in animal_maps:
        sub_file = Animal_Sub_file.objects.get(Animal_map_id=odject.id)
        sub_results.append(sub_file)
    user_agent = get_user_agent(request)

    # 모바일 pc 확인
    if user_agent.is_mobile:
        print("모바일")
        return render(request, 'mobile/homelist.html', {'animal_maps': animal_maps, 'sub_results': sub_results})
    elif user_agent.is_pc:
        print("pc")
        return render(request, 'homelist.html', {'animal_maps': animal_maps, 'sub_results': sub_results})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def animal_detail(request, pk):

    animal_map = get_object_or_404(Animal_map, pk=pk)
    animal_maps = animal_map
    print("aa", animal_maps.title)
    try:
        subfile = Animal_Sub_file.objects.get(Animal_map_id=animal_maps.id)
        print("subfile:", subfile)
        animal_total_info = Animal_total_info.objects.get(name__startswith=animal_maps.title)
    except ObjectDoesNotExist:
        animal_total_info = None

    ##json
    ##
    animal = animal_maps.title
    # print("animal", animal.strip().replace(" ", "_"))
    print("animal: ",animal.strip())
    sparql = SPARQLWrapper("http://lod.nature.go.kr/main/sparql/index.jsp")
    sparql.setQuery("""
        prefix wlo: <http://lod.nature.go.kr/ontology/>
        select ?species ?sName where { 
          ?species wlo:scientificName '""" + animal.strip() + """' . 
          ?species wlo:scientificName ?sName .
        }
        """)
    print("""
        prefix wlo: <http://lod.nature.go.kr/ontology/>
        select ?species ?sName where { 
          ?species wlo:scientificName '""" + animal.strip() + """' . 
          ?species wlo:scientificName ?sName .
        }
        """)
    # """
    #             prefix wlo: <http://lod.nature.go.kr/ontology/>
    #             select ?species ?sName where {
    #               ?species wlo:commonName '""" + animal + """'@ko .
    #               ?species wlo:scientificName ?sName .
    #             }
    #             """
    '''
    prefix wildlife: <http://lod.nature.go.kr/resource/>
    prefix wlo: <http://lod.nature.go.kr/ontology/>
    select ?species ?sName where { 
      ?species wlo:commonName '""" + animal + """'@ko . 
      ?species wlo:scientificName ?sName .
    }
    prefix wildlife: <http://lod.nature.go.kr/resource/>
    prefix wlo: <http://lod.nature.go.kr/ontology/>
    select ?species ?sName where { 
      ?species wlo:commonName '구상나무'@ko . 
      ?species wlo:scientificName ?sName .
    }
    '''

    '''
    sparql = SPARQLWrapper("http://ko.dbpedia.org/sparql")
    sparql.setQuery("""
        prefix kdbr: <http://ko.dbpedia.org/resource/>
    prefix dbr: <http://dbpedia.org/resource/>
    prefix dbo: <http://dbpedia.org/ontology/>
    select ?species ?id where { 
      ?species dbo:class kdbr:양서류 . 
      ?species dbo:division kdbr:척삭동물 .
      ?species dbo:wikiPageID ?id .
    }limit 10
    """)
    '''

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    report_file_name = "./sparql_test.tsv"
    report_file = open(report_file_name, mode='w', encoding='utf-8')
    print("report file name : %s" % report_file_name)

    test = results.decode("utf-8")
    print(test)

    tree = ET.fromstring(test)

    # for child in tree.iter('{http://www.w3.org/2005/sparql-results#}results/result'):
    #    print(child.tag, child.attrib)
    spe = tree.find(
        './{http://www.w3.org/2005/sparql-results#}results/{http://www.w3.org/2005/sparql-results#}result/{http://www.w3.org/2005/sparql-results#}binding[@name="species"]/{http://www.w3.org/2005/sparql-results#}uri')
    spename = tree.find(
        './{http://www.w3.org/2005/sparql-results#}results/{http://www.w3.org/2005/sparql-results#}result/{http://www.w3.org/2005/sparql-results#}binding[@name="sName"]/{http://www.w3.org/2005/sparql-results#}literal')
    if (spe == None or spename == None):
        print("이상발생")
        animalsinfo = "LOD 정보를 찾을 수 없었습니다..."
        urlpage = ""
        spename = animal_map.title
    else:
        species_uri = spe.text
        spename = spename.text.split('(')[0]
        print("spe.text:", spe.text)
        print("name:", spename)

        tokens = species_uri.split('/')
        species_name = tokens[-1]

        url = 'http://lod.nature.go.kr/data/' + species_name + '?output=json'  # 요청할 주소

        text_data = urllib.request.urlopen(url).read().decode('utf-8')

        animals = json.loads(text_data)
        animalsinfo = ""
        print(type(animals))
        for i in animals:
            for j in animals[i]:
                # print(j)
                if (animals[i][j][0]["type"] == "literal"):
                    print(animals[i][j][0]["value"])
                    animalsinfo = animalsinfo + "\n" + animals[i][j][0]["value"]
        urlpage = 'http://lod.nature.go.kr/page/' + species_name
    # report_file.write(results)

    # for result in results["results"]["bindings"]:
    #    report_file.write('%s: %s\n' % (result["label"]["xml:lang"], result["label"]["value"]))
    ##
    ###
    name = animal.strip().replace(" ", "_")
    try:
        req = urllib.request.urlopen(
            "http://lod.nature.go.kr/data/" + animal.strip().replace(" ", "_") + "?output=xml")
        tll = req.read().decode("utf-8")
        root = elemTree.fromstring(tll)

        triples = "["
        # print("[")
        for child in root[0]:
            if child.tag.split("}")[1] == "sameAs" or child.tag.split("}")[1] == "depiction":
                continue
            elif child.text == None:
                text = child.attrib
                try:
                    text = str(text).split("nature.go.kr/resource/")[1].split("}")[0].replace("'", "")
                    print("http://lod.nature.go.kr/data/" + text + "?output=xml")
                except IndexError:
                    print("오류:", text)
                    continue

                # classnode(child.tag.split("}")[1],"http:"+text)
                req1 = urllib.request.urlopen("http://lod.nature.go.kr/data/" + text + "?output=xml")
                print(text)
                tll1 = req1.read().decode("utf-8")
                root1 = elemTree.fromstring(tll1)
                for child1 in root1[0]:
                    print(child1)
                    if child1.tag.split("}")[1] == "sameAs":
                        continue
                    elif child1.text == None:
                        continue
                    else:
                        text1 = child1.text.replace('\n', '').replace('\r', '').replace('"', '').replace(
                            "RDF description of ", "")
                        if ''.join(text1.split()) == "":
                            continue
                        print(text1)
                        Class = "node"
                    triples += '{ subject: "' + text + '",predicate:"' + child1.tag.split("}")[
                        1] + '",object:"' + text1 + '",class:"' + Class + '"},'
                    print(text)
                # text=child.tag.split("}")[1]
                print(text)
                Class = "class"
            else:
                text = child.text.replace('\n', '').replace('\r', '').replace('"', '')
                Class = "node"
            triples += '{ subject: "' + (name) + '",predicate:"' + child.tag.split("}")[
                1] + '",object:"' + text + '",class:"' + Class + '"},'
            # print('{ subject: "',name,'",predicate:"',child.tag.split("}")[1],'",object:"',text,'"},')
        triples += "];"
        # print("];")

        print(triples)
    except HTTPError:
        triples = '[{ subject: "' + (name) + '",predicate:"' + (name) + '",object:"' + (name) + '",class:"node"}];'

    # 모바일 pc 확인
    user_agent = get_user_agent(request)
    if user_agent.is_mobile:
        return render(request, 'mobile/animal_detail.html',
                      {'animal_map': animal_map, 'total_info': animal_total_info, 'animals': animalsinfo,
                       'url': urlpage, 'spename': spename, 'subfile': subfile, 'triples': triples})
    if user_agent.is_pc:
        return render(request, 'animal_detail.html',
                      {'animal_map': animal_map, 'total_info': animal_total_info, 'animals': animalsinfo,
                       'url': urlpage, 'spename': spename, 'subfile': subfile, 'triples': triples})

def search_table(request):
    all_class=Animal_map.objects.filter()
    q = request.GET['search_key']
    results =[]
    for odject in all_class.filter(title__contains=q):
        results.append(odject)
    context = {'results':results} 
    return render(request,'only_table.html',context)

def animal_remove(request, pk):
    article = get_object_or_404(Animal_map, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('/')
    return render(request, 'animal_remove.html',{'feed': article})


def animal_edit(request,pk):
    article = get_object_or_404(Animal_map, pk=pk)
    if request.method == 'POST':
        article.title = request.POST['title']
        article.content = request.POST['content']
        article.save()
        return redirect('animal_detail', pk=article.pk )

    return render(request, 'animal_edit.html', {'feed': article})

def statistics(request):

    s = request.GET.get('s', None)
    print("s는 무엇일까요??:", s)
    animaldistrict = district.objects.filter()

    file_meta_dict = dict()
    if s == 'all' or s == None:
        # address stat
        testing = Animal_map.objects.raw(
            "SELECT address as id, count(*) as cnt FROM blog_animal_map group by address")
        print(testing)
        address_dict = dict()
        for p in testing:
            print(p)
            print(p.id)
            print(p.cnt)
            print(Animal_map.ADDRESS_DICT[p.id])
            address_dict[Animal_map.ADDRESS_DICT[p.id]] = p.cnt
        file_meta_dict['file_count_address'] = address_dict
        print(file_meta_dict)
        json_val = json.dumps(file_meta_dict, ensure_ascii=False)
        print(json_val)
    else:
        # address stat
        testing = Animal_map.objects.raw(
            "SELECT address as id, count(*) as cnt FROM blog_animal_map where animalclass='" + s + "' group by address")
        print(testing)
        address_dict = dict()
        for p in testing:
            print(p)
            print(p.id)
            print(p.cnt)
            print(Animal_map.ADDRESS_DICT[p.id])
            address_dict[Animal_map.ADDRESS_DICT[p.id]] = p.cnt
        file_meta_dict['file_count_address'] = address_dict
        print(file_meta_dict)
        json_val = json.dumps(file_meta_dict, ensure_ascii=False)
        print(json_val)
    context = {'animaldistricts': animaldistrict, 'file_meta_dict': file_meta_dict}

    # 모바일 pc 확인
    user_agent = get_user_agent(request)
    if user_agent.is_mobile:
        return render(request, 'mobile/statistics.html', context)
    elif user_agent.is_pc:
        return render(request,'statistics.html',context)
#
require_POST
def list_dn(request):
    pk = request.POST.get('pk', None)
    statistics=request.POST.get('statistics', None)
    print('pk:',pk,"   statistics:",statistics)
    file_meta_dict = dict()
    if statistics=='all'or statistics=="":
        # title stat
        testing = Animal_map.objects.raw(
            "SELECT animalclass as id, count(*) as cnt FROM blog_animal_map where address='"+pk+"' group by animalclass;")
        print("testing: ", testing)
        title_dict = dict()
        for p in testing:
            print(p)
            print(p.id)
            print(p.cnt)
            title_dict[p.id] = p.cnt
        file_meta_dict['region_count_ex'] = title_dict
    else:
        # title stat
        testing = Animal_map.objects.raw(
            "SELECT to_char(observed_date,'YYYY') as id, count(*) as cnt FROM blog_animal_map where animalclass='"+statistics+"'and address='"+pk+"' group by to_char(observed_date,'YYYY')")
        print("testing: ", testing)
        title_dict = dict()
        for p in testing:
            print(p)
            print(p.id)
            print(p.cnt)
            title_dict[p.id] = p.cnt
        file_meta_dict['year_count_ex'] = title_dict

        # title stat
        testing = Animal_map.objects.raw(
            "SELECT to_char(observed_date,'YYYY-MM') as id, count(*) as cnt FROM blog_animal_map where animalclass='" + statistics + "'and address='" + pk + "' group by to_char(observed_date,'YYYY-MM')")
        print("testing: ", testing)
        title_dict = dict()
        for p in testing:
            print(p)
            print(p.id)
            print(p.cnt)
            title_dict[p.id] = p.cnt
        file_meta_dict['month_count_ex'] = title_dict

    context = file_meta_dict
    # json_val = json.dumps(context, ensure_ascii=False)
    # print(json_val)
    return HttpResponse(json.dumps(context), content_type="application/json")

def detail_dn(request):
    formDatas = request.POST.get('formData', None)
    formData = formDatas.split('&')
    name = formData[0].split('=')[1]
    division =formData[1].split('=')[1]
    sido=formData[2].split('=')[1]
    gugun=formData[3].split('=')[1]
    dong =formData[4].split('=')[1]
    startdate=formData[5].split('=')[1]
    enddate=formData[6].split('=')[1]
    print('formData:',formData)
    print("name:",name)
    print("division:",division)
    print("sido:",sido)
    print("gugun:",gugun)
    print("dong:", dong)
    print("startdate:",startdate)
    print("enddate:", enddate)
    if sido == "시/도+선택":
        sido = ""
    if gugun == "전체":
        gugun = ""
    if startdate == "" :
        startdate = "1900-03-06"
    if enddate == "":
        enddate = "2200-03-06"
    print("aaa",type(division))
    file_meta_dict = dict()

    testing = Animal_map.objects.raw("SELECT * FROM blog_animal_map where title LIKE '%%"+name+"%%'and animalclass like '%%"+division+"%%' and (address1 like '%%"+sido+"%%') and (address2 like '%%"+gugun+"%%' or address2 is null and address3 like '%%"+gugun+"%%' or address3 is null) and (address4 like '%%"+dong+"%%' or address4 is null and address5 like '%%"+dong+"%%' or address5 is null and address6 like '%%"+dong+"%%' or address6 is null) and observed_date >='"+startdate+"' and observed_date <='"+enddate+"'")
    print("testing: ", testing)
    title_dict = dict()
    observed_date_dict = dict()
    img_dict = dict()
    address_dict = dict()
    for p in testing:
        print(p)
        print(p.id)
        print(p.title)
        print(p.observed_date)
        title_dict[p.id] = p.title
        observed_date_dict[p.id] = str(p.observed_date)
        img_dict[p.id]=str(p.imagefile)
        address_dict[p.id]=p.address
    file_meta_dict['title'] = title_dict
    file_meta_dict['observed_date'] = observed_date_dict
    file_meta_dict['image'] = img_dict
    file_meta_dict['address'] = address_dict
    context = file_meta_dict

    return HttpResponse(json.dumps(context), content_type="application/json")

def detailsearch(request):
    return render(request, 'detailsearch.html')

def classification(request):

    if request.method == "POST":
        form = Animal_classForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            Animal_classForm.soundfile = request.FILES['soundfile']
            fs = 44100

            return HttpResponseRedirect('/animalclassificationresult')
            # return render(request, 'animalclassificationresult.html', {'form': form})
    else:
        # 데이터 삭제
        if os.path.exists('./media/temporary'):
            for file in os.scandir('./media/temporary'):
                os.remove(file.path)
        form = Animal_classForm()

    # 모바일 pc 확인
    user_agent = get_user_agent(request)
    if user_agent.is_mobile:
        return render(request, 'mobile/animalclassification.html', {'form': form})
    elif user_agent.is_pc:
        return render(request, 'animalclassification.html', {'form': form})




from collections import Counter
from pydub import AudioSegment

def time_string():
    return datetime.now().strftime('%Y/%m/%d-%H:%M:%S')

def animalclassificationresult(request):
    color = ['#9DC8C866', '#519D9E66', '#D1B6E166', '#30A9DE66', '#A593E066', '#F6B35266', '#56627066', '#D7FFF166',
             '#FDD69266', '#791E9466',
             '#EE778566', '#75D70166', '#8EC0E466', '#9B828166', '#ABD0CE66', '#f9320c66', '#8283a766', '#a7a7a266',
             '#fbd14b66', '#c0354666',
             '#3ac56966', '#e97f0266', '#f9a11b66', '#a79c8e66', '#004e6666', '#ef9e9f66','#9DC8C866', '#519D9E66', '#D1B6E166', '#30A9DE66', '#A593E066', '#F6B35266', '#56627066', '#D7FFF166',
             '#FDD69266', '#791E9466',
             '#EE778566', '#75D70166', '#8EC0E466', '#9B828166', '#ABD0CE66', '#f9320c66', '#8283a766', '#a7a7a266',
             '#fbd14b66', '#c0354666',
             '#3ac56966', '#e97f0266', '#f9a11b66', '#a79c8e66', '#004e6666', '#ef9e9f66','#9DC8C866', '#519D9E66', '#D1B6E166', '#30A9DE66', '#A593E066', '#F6B35266', '#56627066', '#D7FFF166',
             '#FDD69266', '#791E9466',
             '#EE778566', '#75D70166', '#8EC0E466', '#9B828166', '#ABD0CE66', '#f9320c66', '#8283a766', '#a7a7a266',
             '#fbd14b66', '#c0354666',
             '#3ac56966', '#e97f0266', '#f9a11b66', '#a79c8e66', '#004e6666', '#ef9e9f66','#9DC8C866', '#519D9E66', '#D1B6E166', '#30A9DE66', '#A593E066', '#F6B35266', '#56627066', '#D7FFF166',
             '#FDD69266', '#791E9466',
             '#EE778566', '#75D70166', '#8EC0E466', '#9B828166', '#ABD0CE66', '#f9320c66', '#8283a766', '#a7a7a266',
             '#fbd14b66', '#c0354666',
             '#3ac56966', '#e97f0266', '#f9a11b66', '#a79c8e66', '#004e6666', '#ef9e9f66','#9DC8C866', '#519D9E66', '#D1B6E166', '#30A9DE66', '#A593E066', '#F6B35266', '#56627066', '#D7FFF166',
             '#FDD69266', '#791E9466',
             '#EE778566', '#75D70166', '#8EC0E466', '#9B828166', '#ABD0CE66', '#f9320c66', '#8283a766', '#a7a7a266',
             '#fbd14b66', '#c0354666',
             '#3ac56966', '#e97f0266', '#f9a11b66', '#a79c8e66', '#004e6666', '#ef9e9f66','#9DC8C866', '#519D9E66', '#D1B6E166', '#30A9DE66', '#A593E066', '#F6B35266', '#56627066', '#D7FFF166',
             '#FDD69266', '#791E9466',
             '#EE778566', '#75D70166', '#8EC0E466', '#9B828166', '#ABD0CE66', '#f9320c66', '#8283a766', '#a7a7a266',
             '#fbd14b66', '#c0354666',
             '#3ac56966', '#e97f0266', '#f9a11b66', '#a79c8e66', '#004e6666', '#ef9e9f66','#9DC8C866', '#519D9E66', '#D1B6E166', '#30A9DE66', '#A593E066', '#F6B35266', '#56627066', '#D7FFF166',
             '#FDD69266', '#791E9466',
             '#EE778566', '#75D70166', '#8EC0E466', '#9B828166', '#ABD0CE66', '#f9320c66', '#8283a766', '#a7a7a266',
             '#fbd14b66', '#c0354666',
             '#3ac56966', '#e97f0266', '#f9a11b66', '#a79c8e66', '#004e6666', '#ef9e9f66','#9DC8C866', '#519D9E66', '#D1B6E166', '#30A9DE66', '#A593E066', '#F6B35266', '#56627066', '#D7FFF166',
             '#FDD69266', '#791E9466',
             '#EE778566', '#75D70166', '#8EC0E466', '#9B828166', '#ABD0CE66', '#f9320c66', '#8283a766', '#a7a7a266',
             '#fbd14b66', '#c0354666',
             '#3ac56966', '#e97f0266', '#f9a11b66', '#a79c8e66', '#004e6666', '#ef9e9f66','#9DC8C866', '#519D9E66', '#D1B6E166', '#30A9DE66', '#A593E066', '#F6B35266', '#56627066', '#D7FFF166',
             '#FDD69266', '#791E9466',
             '#EE778566', '#75D70166', '#8EC0E466', '#9B828166', '#ABD0CE66', '#f9320c66', '#8283a766', '#a7a7a266',
             '#fbd14b66', '#c0354666',
             '#3ac56966', '#e97f0266', '#f9a11b66', '#a79c8e66', '#004e6666', '#ef9e9f66']

    fs = 44100
    inp_wav = os.path.join(os.listdir('./media/temporary')[0]) # 데이터 가져오기
    print(os.listdir('./media/temporary')[0]) # 데이터 가져오는거 확인
    print('./media/temporary/' + inp_wav)
    if inp_wav.split(".")[1] == "mp3":
        sound = AudioSegment.from_mp3('./media/temporary/' + inp_wav)
        sound.export('./media/temporary/' + inp_wav.split(".")[0] + ".wav", format="wav")
        os.remove('./media/temporary/' + inp_wav)
    elif inp_wav.split(".")[1] == "m4a":
        sound = AudioSegment.from_file('./media/temporary/' + inp_wav, "m4a")
        sound.export('./media/temporary/' + inp_wav.split(".")[0] + ".wav", format="wav")
        os.remove('./media/temporary/' + inp_wav)
    inp_wav = os.path.join(os.listdir('./media/temporary')[0])

    logPath = './Aniaml_demo/Animal.log'
    log_fp = open(logPath, 'w')
    myrecording, sr = librosa.load("./media/temporary/" + inp_wav, sr=22050)
    audio_length = len(myrecording)
    class_list = open("./Aniaml_demo/list_115.txt", 'r', encoding='UTF8')
    myrecording = np.expand_dims(myrecording, 0)


    animal_count = []
    animal_count_real = []
    animal_totalcount = []
    animal_start = [0]
    animal_end = []
    animal_data = []
    animal_color = []
    lists = []
    for i6 in range(nClass):
        classes = class_list.readline()
        lists.append(classes)
    lists = np.block(lists)
    lists = list(map(lambda s: s.strip(), lists))
    # duration=8
    a = time.time()
    temps = np.mod(audio_length, 22050)
    myrecording = np.concatenate([myrecording, np.zeros([1, 22050 - temps])], 1)
    tt = np.shape(myrecording)
    Nchunk = np.floor(tt[1] / 22050)
    file_size = Nchunk * 2 - 1
    outputs = []
    file_size = np.asarray(file_size, dtype=np.int32)

    for i in range(file_size):
        inputs = myrecording[:, i * 11025:((i) * 11025 + 22050)]
        out, reg, pre = model_A_solver.evaluate_dev(inputs)

        # print('Time: ,{0:0.6f}',time.time()-a)
        Sc = np.asarray(out, dtype=np.int32)
        Sc = Sc[0]

        # Sc=np.squeeze(Sc-np.mean(Sc)/(np.var(Sc)+0.001))
        # print(reg[0])
        if reg[0] < 0.5:
            state = 'blank'
            animal_totalcount.append(999)
            print(state)
        else:
            if pre < 0.5:
                state = 'blank'
                animal_totalcount.append(999)
            else:
                print(Sc)
                temp = lists[Sc]
                state = str(temp)
                print(state)
                animal_count.append(state)
                # print(labels[classs.item()])
                animal_totalcount.append(Sc)
        outputs.append(state)
        log = '[Step {0:2d}] ,Time: {1:.4f} Sec ,Target: {2:s}\n'.format((i + 1), (i + 1) * 0.5, state)
        print(log)
        log_fp.write(log)
    result = Counter(animal_count)
    print(result)
    print("animal_totalcount", animal_totalcount)

    '''
    # inp_wav = os.path.join('./test1.wav')
    out_txt = os.path.join('./animal.log')
    prev_state = None
    with open("./class_name.txt", "r", encoding='UTF8') as f:
        labels = f.readlines()
    labels = np.block(labels)
    labels = list(map(lambda s: s.strip(), labels))
    # print(labels)

    curr_state = os.path.getatime("./media/temporary/" + inp_wav)
    if curr_state != prev_state:
        print(time_string(), end=' ')
        print("New recorded file arrived!")
        prev_state = curr_state

        wav, _ = librosa.load("./media/temporary/" + inp_wav, sr=fs)
        duration = len(wav) // fs
        wav = wav[np.newaxis, :]

        hop_size = fs // 2
        total_steps = duration * 2 - 1

        for i in range(total_steps):
            inp = wav[:, i * hop_size:(i + 1) * hop_size + hop_size]
            Sc = model_A_solver.evaluate(inp)
            Sc = np.asarray(Sc, dtype=np.float32)[0]
            rres = list()
            for ii in range(nClass):
                rres.append(cos_sim(Sc, Feature_class[ii]))
            rres = np.transpose(np.block(np.transpose(rres)))
            classs = np.where(rres > 0.92)[0]

            if not classs:
                # print('No animal sound detected')
                animal_totalcount.append(99)
            else:
                curr_time = time.gmtime(curr_state + (i * .5))
                with open(out_txt, 'a', encoding='UTF8') as f:
                    f.write(str(labels[classs.item()]) + ' sound detected at '
                            + time.strftime('%Y/%m/%d-%H:%M:%S', curr_time) + '\n')
                # print(time_string(), end=' ')
                # print(str(labels[classs.item()]) + ' sound detected')


                animal_count.append(labels[classs.item()])
                # print(labels[classs.item()])
                animal_totalcount.append(classs.item())
    result = Counter(animal_count)
    print(result)
    print("animal_totalcount", animal_totalcount)
    '''
    count = 1
    length = ""
    if len(animal_totalcount) > 1:
        for i in range(1, len(animal_totalcount)):
            if animal_totalcount[i - 1] == animal_totalcount[i]:
                count += 1
            else:
                length += str(animal_totalcount[i - 1]) + ":" + str(count) + ", "
                count = 1
        length += (str(animal_totalcount[i]) + ":" + str(count))
    else:
        i = 0
        length += (str(animal_totalcount[i]) + ":" + str(count))
    print(length)
    sumcount = 0
    for len1 in length.split(","):
        len1.split(":")[0]  # data
        len1.split(":")[1]  # count
        sumcount = (sumcount + int(len1.split(":")[1]) * 0.50)
        if int(len1.split(":")[0]) == 999:
            animal_data.append('')
            animal_color.append('')
        else:
            animal_data.append('note:"' + lists[int(len1.split(":")[0])] + '"')
            animal_color.append(int(len1.split(":")[0]))
            animal_count_real.append(lists[int(len1.split(":")[0])])
        animal_start.append(sumcount)
        animal_end.append(sumcount)

    animal_class = []
    for key in Counter(animal_totalcount):
        print(key)
        animal_class.append(key)
    del animal_class[animal_class.index(999)]
    for key in result:
        print(key, result[key])
        # print(labels[key])
    animal_start.pop()
    print(animal_data)
    print(animal_start)
    print(animal_end)
    result1 = Counter(animal_count_real)
    print("result1", result1)
    print("result", result)

    # json 생성
    f = open("./media/animal.json", 'w')
    f.write('[')
    for i in range(len(animal_data) - 1):
        if animal_data[i] != '':
            print(animal_color[i])
            f.write('{ "start": ' + str(animal_start[i]) + ', "end": ' + str(animal_end[i]) + ', "data": {' +
                    animal_data[i] + '}, color: "' + str(color[animal_color[i]]) + '","attributes": { "label": "' +
                    animal_data[i].split('"')[1].split('"')[0] + '","highlight": true} },')
    if animal_data[len(animal_data) - 1] != '':
        f.write('{ "start": ' + str(animal_start[len(animal_data) - 1]) + ', "end": ' + str(
            animal_end[len(animal_data) - 1]) + ', "data": {' + animal_data[
                    len(animal_data) - 1] + '},color:"' + str(
            color[animal_color[len(animal_data) - 1]]) + '" ,"attributes": { "label": "' +
                animal_data[len(animal_data) - 1].split('"')[1].split('"')[0] + '"},"highlight": true}]')
    else:
        f.write(']')
    f.close()
    # 생성된 json 불러오기
    json1 = open("./media/animal.json", 'r')
    json2 = json1.read()
    print(json2)
    json1.close()

    #모바일 pc 확인
    user_agent = get_user_agent(request)
    if user_agent.is_mobile:
        return render(request, 'mobile/animalclassificationresult.html',
                      {'labelsdata': result, 'labelsdata1': result1, 'inp_wav': inp_wav, 'json2': json2,
                       'animal_class': animal_class})
    if user_agent.is_pc:
        return render(request, 'animalclassificationresult.html',{'labelsdata':result,'labelsdata1':result1,'inp_wav':inp_wav,'json2':json2,'animal_class':animal_class})
    # dic 형식을 json 형식으로 바꾸어 전달한다.




