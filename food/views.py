from django.shortcuts import render, get_object_or_404
from .models import Place, Category, Review

def home(request):
    # Простая главная страница
    places = Place.objects.all()[:3]  # 3 последних места
    return render(request, 'food/home.html', {'places': places})

def place_list(request):
    places = Place.objects.all()
    return render(request, 'food/place_list.html', {'places': places})

def place_detail(request, pk):
    place = get_object_or_404(Place, pk=pk)
    return render(request, 'food/place_detail.html', {'place': place})

def add_place(request):
    # Простая страница-заглушка
    return render(request, 'food/add_place.html')

def about(request):
    return render(request, 'food/about.html')