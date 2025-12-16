from django.urls import path
from . import views

app_name = 'food'

urlpatterns = [
    path('', views.home, name='home'),
    path('places/', views.place_list, name='place_list'),
    path('places/<int:pk>/', views.place_detail, name='place_detail'),
    path('places/add/', views.add_place, name='add_place'),
    path('about/', views.about, name='about'),
]