from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count, Avg
from .models import Category, Place, Review
from .forms import PlaceForm, ReviewForm


def home(request):
    """Главная страница"""
    categories = Category.objects.annotate(num_places=Count('place'))
    top_places = Place.objects.all()[:6]  # Первые 6 мест

    # Статистика
    total_places = Place.objects.count()
    total_reviews = Review.objects.count()

    # Средний рейтинг всех мест
    avg_rating = Place.objects.aggregate(avg=Avg('reviews__rating'))['avg'] or 0

    context = {
        'categories': categories,
        'top_places': top_places,
        'total_places': total_places,
        'total_reviews': total_reviews,
        'avg_rating': avg_rating,
    }
    return render(request, 'food/home.html', context)


def place_list(request):
    """Список всех заведений"""
    places = Place.objects.all()

    # Фильтрация по категории
    category_id = request.GET.get('category')
    if category_id:
        places = places.filter(category_id=category_id)

    # Поиск
    search_query = request.GET.get('search')
    if search_query:
        places = places.filter(name__icontains=search_query)

    # Сортировка
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'rating':
        # Сортируем по вычисляемому полю average_rating
        places = sorted(places, key=lambda x: x.average_rating, reverse=True)
    elif sort_by == 'price_low':
        places = places.order_by('price_level')
    elif sort_by == 'price_high':
        places = places.order_by('-price_level')
    else:
        places = places.order_by('name')

    categories = Category.objects.all()

    context = {
        'places': places,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'search_query': search_query or '',
        'sort_by': sort_by,
    }
    return render(request, 'food/place_list.html', context)


def place_detail(request, pk):
    """Детальная страница заведения"""
    place = get_object_or_404(Place, pk=pk)

    # Форма для добавления отзыва
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.place = place
            if request.user.is_authenticated:
                review.author = request.user
                review.author_name = request.user.username
            review.save()
            messages.success(request, 'Ваш отзыв успешно добавлен!')
            return redirect('place_detail', pk=pk)
    else:
        form = ReviewForm()

    context = {
        'place': place,
        'form': form,
        'reviews': place.reviews.all(),
    }
    return render(request, 'food/place_detail.html', context)


def add_place(request):
    """Добавление нового заведения"""
    if request.method == 'POST':
        form = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            place = form.save()
            messages.success(request, f'Заведение "{place.name}" успешно добавлено!')
            return redirect('place_detail', pk=place.pk)
    else:
        form = PlaceForm()

    context = {'form': form}
    return render(request, 'food/add_place.html', context)


def about(request):
    """Страница "О проекте" """
    return render(request, 'food/about.html')