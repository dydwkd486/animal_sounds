from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .models import Animal_map
from .forms import Animal_mapForm
import json


@login_required
def home(request):
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
        return render(request, 'home.html',context)

    if request.GET.get('search_key'):
        results =[]
        query = request.GET['search_key']
        
        for odject in animal_maps.filter(title__contains=query):
            results.append(odject)
        context = {'animal_maps':results} 
        return render(request, 'home.html',context)

    if request.GET.get('sw_lat'):
        results =[]
        sw_lat = request.GET['sw_lat']
        sw_lng = request.GET['sw_lng']
        ne_lat = request.GET['ne_lat']
        ne_lng = request.GET['ne_lng']
        for odject in animal_maps.filter(Longitude__range=(sw_lng,ne_lng),Latitude__range=(sw_lat,ne_lat)):
            results.append(odject)
        context = {'animal_maps':results} 
        return render(request, 'home.html',context)

    return render(request, 'home.html',{'animal_maps':animal_maps})


def save(request):
    if request.method == "POST":
        form = Animal_mapForm(request.POST, request.FILES)
        if form.is_valid():
            animal = form.save(commit=False)
            animal.writer = request.user
            animal.save()
            return redirect('/')
    else:
        form = Animal_mapForm()
    return render(request, 'animalsave.html', {'form': form})


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
    return render(request, 'animal_detail.html', {'animal_map': animal_map})

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
        return redirect(f'/animal_detail/{ article.pk }')

    return render(request, 'animal_edit.html', {'feed': article})
