from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('change/', views.Change.as_view(), name='change'),
    path('singup_success/', views.SignUp_success.as_view(), name='singup_success'),
]