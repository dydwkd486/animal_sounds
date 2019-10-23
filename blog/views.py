from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404,HttpResponse
from .models import Animal_map, Animal_total_info,district,Animal_Sub_file
from .forms import Animal_mapForm,AnimalmapFormMultiform
from django.core.exceptions import ObjectDoesNotExist
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

from SPARQLWrapper import SPARQLWrapper, JSON
import xml.etree.ElementTree as ET

def test(request):
    return render(request, 'test.html')
#@login_required
def home(request):
    animap = Animal_map.objects.filter()

    file_meta_dict = dict()
    # file size stat
    testing = Animal_map.objects.aggregate(file_size_avg=Avg('file_size_input'), file_size_max=Max('file_size_input'),
                                           file_size_min=Min('file_size_input'))

    for p in testing:
        print(p)
        print(testing[p])
        file_meta_dict[p] = testing[p]

    # file duration stat
    testing = Animal_map.objects.aggregate(file_duration_avg=Avg('duration_input'),
                                           file_duration_max=Max('duration_input'),
                                           file_duration_min=Min('duration_input'))

    for p in testing:
        print(p)
        print(testing[p])
        file_meta_dict[p] = testing[p]

    # writer stat
    testing = Animal_map.objects.raw("SELECT writer as id, count(*) as cnt FROM blog_animal_map group by writer")
    print(testing)
    writer_dict = dict()
    for p in testing:
        print(p)
        print(p.id)
        print(p.cnt)
        writer_dict[p.id] = p.cnt
    file_meta_dict['file_count_writer'] = writer_dict

    testing = Animal_map.objects.raw(
        "SELECT writer as id, count(*) as cnt FROM blog_animal_map where observed_date >= '2010-02-10' and observed_date <= '2010-02-10' group by writer")
    print(testing)
    writer_data_dict = dict()
    for p in testing:
        print(p)
        print(p.id)
        print(p.cnt)
        writer_data_dict[p.id] = p.cnt
    file_meta_dict['file_count_writer_given_date'] = writer_data_dict

    # file extension stat
    testing = Animal_map.objects.raw(
        "SELECT file_ex_input as id, count(*) as cnt FROM blog_animal_map group by file_ex_input")
    print(testing)
    file_ex_dict = dict()
    for p in testing:
        print(p)
        print(p.id)
        print(p.cnt)
        file_ex_dict[p.id] = p.cnt
    file_meta_dict['file_count_ex'] = file_ex_dict
    '''
    # class stat
    testing = Animal_map.objects.raw(
        "SELECT count(*) as cnt, class as id FROM blog_animal_map group by class")
    print(testing)
    for p in testing:
        print(p)
        print(p.id)
        print(p.cnt)
    '''

    # title stat
    testing = Animal_map.objects.raw(
        "SELECT title as id, count(*) as cnt FROM blog_animal_map group by title")
    print("testing: ",testing)
    title_dict = dict()
    for p in testing:
        print(p)
        print(p.id)
        print(p.cnt)
        title_dict[p.id] = p.cnt
    file_meta_dict['file_count_ex'] = title_dict

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

    animal_maps=Animal_map.objects.filter()
    #조건이 6가지 (이름, 구분, 지역, 시작날짜, 끝날짜, 맵다시확인)
    count = 100
    query=""
    sw_lat="0"
    sw_lng="0"
    ne_lat="180"
    ne_lng="180"
    address="abcdefghijk"
    class_key="mbrai"
    startdate="1900-03-06"
    enddate="2200-03-06"
    results =[]
    print("enddate", enddate)
    if request.GET.get('search_key'):
        query=request.GET['search_key']
        print("search_key")

    if request.GET.get('sw_lat'):
        sw_lat = request.GET['sw_lat']
        sw_lng = request.GET['sw_lng']
        ne_lat = request.GET['ne_lat']
        ne_lng = request.GET['ne_lng']

    if request.GET.get('address_key'):
        address=request.GET['address_key']
        print("address")

    if request.GET.get('class_key'):
        class_key=request.GET['class_key']
        print(class_key)

    if request.GET.get('startdate'):
        startdate=request.GET['startdate']
        print("startdate",startdate)

    if request.GET.get('enddate'):
        enddate=request.GET['enddate']
        print("enddate",enddate)
    if request.GET.get('count'):
        count=request.GET['count']
        print("count",count)
    for odject in animal_maps.filter(Longitude__range=(sw_lng,ne_lng),Latitude__range=(sw_lat,ne_lat),title__contains=query,address__in=address,animalclass__in=class_key,observed_date__range=(startdate,enddate)).order_by('-observed_date'):
        results.append(odject)
        #print(odject.title)
    print(count)
    if count == "0":
        count = len(results)

    context = {'animal_maps':results[:count]}

    return render(request, 'home.html',context)

''' 승원 수정 부분 '''
def save(request):
    if request.method == "POST":
        form = AnimalmapFormMultiform(request.POST, request.FILES)
        if form.is_valid():
            animal = form['animal_map'].save(commit=False)

            Latitude = request.POST['animal_map-Latitude'] #위도
            Longitude = request.POST['animal_map-Longitude'] #경도
            url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+Latitude+","+Longitude+"&key=AIzaSyDWV0tlx-1gtFEIJPEdpIFWdGGghKB34xk&language=ko"
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
            animal.save()

            num=0
            print("request.POST:")
            print(request.POST)
            print(request.POST.get('subfile_meta%d' % num))

            #print("url:",url)

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
    return render(request, 'animalsave.html', {'form': form})
''' end 승원 수정 부분 '''

def list(request):
    animal_maps=Animal_map.objects.filter().order_by('-observed_date')

    count = 1
    sub_results = []
    for odject in animal_maps:
        try:
            sub_file = Animal_Sub_file.objects.get(Animal_map_id=odject.id)
            sub_results.append(sub_file)
        except ObjectDoesNotExist:
            sub_file = Animal_Sub_file.objects.get(id=5000)
            sub_results.append(sub_file)
    if request.GET.get('page'):
        count = int(request.GET['page'])
        print(count)
    if request.GET.get('sw_lat'):
        results =[]

        sw_lat = request.GET['sw_lat']
        sw_lng = request.GET['sw_lng']
        ne_lat = request.GET['ne_lat']
        ne_lng = request.GET['ne_lng']
        for odject in animal_maps.filter(Longitude__range=(sw_lng,ne_lng),Latitude__range=(sw_lat,ne_lat)).order_by('-observed_date'):
            results.append(odject)

        context = {'animal_maps':results}
        return render(request, 'homelist.html',context)

    if request.GET.get('search_key'):
        results =[]
        query = request.GET['search_key']
        
        for odject in animal_maps.filter(title__startswith=query).order_by('-observed_date'):
            results.append(odject)
        context = {'animal_maps':results} 
        return render(request, 'homelist.html',context)

    if request.GET.get('sw_lat'):
        results =[]
        sw_lat = request.GET['sw_lat']
        sw_lng = request.GET['sw_lng']
        ne_lat = request.GET['ne_lat']
        ne_lng = request.GET['ne_lng']
        for odject in animal_maps.filter(Longitude__range=(sw_lng,ne_lng),Latitude__range=(sw_lat,ne_lat)).order_by('-observed_date'):
            results.append(odject)
        context = {'animal_maps':results}
        return render(request, 'homelist.html',context)
    return render(request, 'homelist.html',{'animal_maps':animal_maps[(count-1)*10:count*10],'sub_results':sub_results[(count-1)*10:count*10]})

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
    print("aa",animal_maps.title)
    try:
        subfile=Animal_Sub_file.objects.get(Animal_map_id=animal_maps.id)
        print("subfile:", subfile)
        animal_total_info=Animal_total_info.objects.get(name__startswith=animal_maps.title)
    except ObjectDoesNotExist:
        animal_total_info=None

    ##json
    ##
    animal = animal_maps.title

    sparql = SPARQLWrapper("http://lod.nature.go.kr/main/sparql/index.jsp")
    sparql.setQuery("""
        prefix wildlife: <http://lod.nature.go.kr/resource/>
    prefix wlo: <http://lod.nature.go.kr/ontology/>
    select ?species ?sName where { 
      ?species wlo:commonName '""" + animal + """'@ko . 
      ?species wlo:scientificName ?sName .
    }
    """)

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
    if(spe==None or spename==None):
        print("이상발생")
        animalsinfo = "LOD 정보를 찾을 수 없었습니다..."
        urlpage =""
        spename=animal_map.title
    else:
        species_uri = spe.text
        spename=spename.text.split('(')[0]
        print("spe.text:", spe.text)
        print("name:" ,spename)

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

    return render(request, 'animal_detail.html', {'animal_map': animal_map,'total_info':animal_total_info,'animals':animalsinfo ,'url':urlpage,'spename':spename, 'subfile':subfile})

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
    s=request.GET.get('s', None)
    print("s는 무엇일까요??:",s)
    animaldistrict = district.objects.filter()

    file_meta_dict = dict()
    if s=='all' or s==None:
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
    else:
        # address stat
        testing = Animal_map.objects.raw(
            "SELECT address as id, count(*) as cnt FROM blog_animal_map where animalclass='"+s+"' group by address")
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

    context = {'animaldistricts':animaldistrict,'file_meta_dict':file_meta_dict}
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