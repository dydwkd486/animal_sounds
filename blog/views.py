from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .models import Animal_map, Animal_total_info
from .forms import Animal_mapForm,AnimalmapFormMultiform
from django.core.exceptions import ObjectDoesNotExist
''' 승원 수정 부분 '''
from .forms import Animal_Sub_file
''' end 승원 수정 부분 '''
import json


#@login_required
def home(request):
    animal_maps=Animal_map.objects.filter()
    #조건이 6가지 (이름, 구분, 지역, 시작날짜, 끝날짜, 맵다시확인)
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
        print("startdate")

    if request.GET.get('enddate'):
        enddate=request.GET['enddate']
        print("enddate")

    for odject in animal_maps.filter(Longitude__range=(sw_lng,ne_lng),Latitude__range=(sw_lat,ne_lat),title__contains=query,address__in=address,Class__in=class_key,observed_date__range=(startdate,enddate)):
        results.append(odject)
    context = {'animal_maps':results} 

    return render(request, 'home.html',context)

''' 승원 수정 부분 '''
def save(request):
    if request.method == "POST":
        form = AnimalmapFormMultiform(request.POST, request.FILES)
        if form.is_valid():
            animal = form['animal_map'].save(commit=False)
            animal.writer = request.user
            animal.file_size_input = request.POST['file_size_input']
            animal.file_name_input = request.POST['file_name_input']
            animal.file_ex_input = request.POST['file_ex_input']
            animal.duration_input = request.POST['duration_input']
            animal.save()

            num=0
            print("request.POST:")
            print(request.POST)
            print(request.POST.get('subfile_meta%d' % num))
            Latitude = request.POST['animal_map-Latitude']
            Longitude = request.POST['animal_map-Longitude']

            while request.POST.get('subfile_meta%d' % num):
                subfile = Animal_Sub_file().save(commit=False)
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
    animal_maps=Animal_map.objects.filter()
    if request.GET.get('sw_lat'):
        results =[]
        sw_lat = request.GET['sw_lat']
        sw_lng = request.GET['sw_lng']
        ne_lat = request.GET['ne_lat']
        ne_lng = request.GET['ne_lng']
        for odject in animal_maps.filter(Longitude__range=(sw_lng,ne_lng),Latitude__range=(sw_lat,ne_lat)):
            results.append(odject)
        context = {'animal_maps':results} 
        return render(request, 'homelist.html',context)

    if request.GET.get('search_key'):
        results =[]
        query = request.GET['search_key']
        
        for odject in animal_maps.filter(title__contains=query):
            results.append(odject)
        context = {'animal_maps':results} 
        return render(request, 'homelist.html',context)

    if request.GET.get('sw_lat'):
        results =[]
        sw_lat = request.GET['sw_lat']
        sw_lng = request.GET['sw_lng']
        ne_lat = request.GET['ne_lat']
        ne_lng = request.GET['ne_lng']
        for odject in animal_maps.filter(Longitude__range=(sw_lng,ne_lng),Latitude__range=(sw_lat,ne_lat)):
            results.append(odject)
        context = {'animal_maps':results} 
        return render(request, 'homelist.html',context)

    return render(request, 'homelist.html',{'animal_maps':animal_maps})

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
        animal_total_info=Animal_total_info.objects.get(name__contains=animal_maps.title)
    except ObjectDoesNotExist:
        animal_total_info=None

    print("bb",animal_total_info)


    return render(request, 'animal_detail.html', {'animal_map': animal_map,'total_info':animal_total_info})

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
