from django.urls import path,include 
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('animalsave/', views.save , name='animalsave'),
	path('test/', views.test , name='test'),
	path('animallist/', views.list1 , name='animallist'),
	path('<int:pk>/',views.animal_detail,name='animal_detail'),
	path('<int:pk>/remove',views.animal_remove,name='animal_remove'),
	path('<int:pk>/edit',views.animal_edit,name='animal_edit'),
	path('search/',views.search_table,name="search_table"),
	path('statistics/',views.statistics,name="statistics"),
	path('detailsearch/',views.detailsearch,name="detailsearch"),
	path('dn/',views.list_dn,name="dn"),
	path('detail_dn/',views.detail_dn,name="detail_dn"),
	path('classification/',views.classification,name="classification"),
	path('animalclassificationresult/',views.animalclassificationresult,name="animalclassificationresult")
]




