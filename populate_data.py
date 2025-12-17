import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from food.models import Category, Place, Review
from django.contrib.auth.models import User


def create_categories():
    categories = [
        {'name': 'Ресторан', 'icon': '🍽️'},
        {'name': 'Кафе', 'icon': '☕'},
        {'name': 'Фастфуд', 'icon': '🍔'},
        {'name': 'Бар', 'icon': '🍸'},
        {'name': 'Пиццерия', 'icon': '🍕'},
        {'name': 'Суши', 'icon': '🍣'},
        {'name': 'Кофейня', 'icon': '🥤'},
        {'name': 'Столовая', 'icon': '🍲'},
    ]

    for cat in categories:
        Category.objects.get_or_create(
            name=cat['name'],
            defaults={'icon': cat['icon']}
        )
    print(f"Создано {Category.objects.count()} категорий")


def create_places():
    # Примеры заведений НН
    places_data = [
        {
            'name': 'Бургер Кинг',
            'category': 'Фастфуд',
            'address': 'ул. Большая Покровская, 82',
            'description': 'Сеть ресторанов быстрого питания, специализирующаяся на бургерах.',
            'price_level': 1,
            'phone': '+7 (831) 277-77-77',
            'website': 'https://burgerking.ru',
            'opening_hours': '10:00-22:00',
        },
        {
            'name': 'Итальянский дворик',
            'category': 'Ресторан',
            'address': 'ул. Рождественская, 45',
            'description': 'Уютный ресторан итальянской кухни в историческом центре.',
            'price_level': 3,
            'phone': '+7 (831) 430-20-30',
            'opening_hours': '12:00-23:00',
        },
        {
            'name': 'Кофе Хауз',
            'category': 'Кофейня',
            'address': 'пл. Горького, 2',
            'description': 'Сетевая кофейня с большим выбором напитков и десертов.',
            'price_level': 2,
            'phone': '+7 (831) 414-44-44',
            'opening_hours': '8:00-22:00',
        },
        {
            'name': 'Токио-City',
            'category': 'Суши',
            'address': 'пр. Ленина, 33',
            'description': 'Доставка и ресторан японской кухни.',
            'price_level': 2,
            'phone': '+7 (831) 215-55-55',
            'website': 'https://tokyo-city.ru',
            'opening_hours': '11:00-23:00',
        },
        {
            'name': 'Пивной ресторан «Бочка»',
            'category': 'Бар',
            'address': 'ул. Пискунова, 21',
            'description': 'Пивной ресторан с собственной пивоварней.',
            'price_level': 2,
            'opening_hours': '12:00-02:00',
        },
        {
            'name': 'Столовая №1',
            'category': 'Столовая',
            'address': 'ул. Варварская, 32',
            'description': 'Бюджетная столовая с домашней кухней.',
            'price_level': 1,
            'opening_hours': '9:00-20:00',
        },
        # Добавьте еще 10-15 мест по аналогии
    ]

    for place_data in places_data:
        category = Category.objects.get(name=place_data.pop('category'))
        Place.objects.get_or_create(
            name=place_data['name'],
            defaults={
                'category': category,
                **place_data
            }
        )
    print(f"Создано {Place.objects.count()} заведений")


def create_reviews():
    # Создаем тестовые отзывы
    places = Place.objects.all()
    review_texts = [
        "Отличное место! Обязательно вернусь еще.",
        "Неплохо, но есть куда расти.",
        "Очень понравилось, рекомендую всем!",
        "Цены завышены, еда среднего качества.",
        "Лучшее заведение в городе!",
        "Уютная атмосфера, приветливый персонал.",
        "Было вкусно, но обслуживание медленное.",
    ]

    for place in places:
        for i in range(3):  # По 3 отзыва на заведение
            Review.objects.get_or_create(
                place=place,
                author_name=f'Гость_{place.id}_{i}',
                defaults={
                    'text': review_texts[i % len(review_texts)],
                    'rating': (place.id + i) % 5 + 1,  # Рейтинг от 1 до 5
                }
            )
    print(f"Создано {Review.objects.count()} отзывов")


if __name__ == '__main__':
    print("Начинаем наполнение базы данных...")
    create_categories()
    create_places()
    create_reviews()
    print("Готово! База данных заполнена.")