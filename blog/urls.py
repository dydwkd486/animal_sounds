from django.urls import path,include 
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('animalsave/', views.save , name='animalsave'),
	path('animallist/', views.list , name='animallist'),
	path('<int:pk>/',views.animal_detail,name='animal_detail'),
	path('<int:pk>/remove',views.animal_remove,name='animal_remove'),
	path('<int:pk>/edit',views.animal_edit,name='animal_edit'),
	path('search/',views.search_table,name="search_table"),
	path('statistics/',views.statistics,name="statistics"),
]




