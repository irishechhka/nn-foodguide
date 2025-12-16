from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """Категории заведений"""
    name = models.CharField(max_length=50, verbose_name="Название")
    icon = models.CharField(max_length=50, default="🍴", verbose_name="Иконка")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Place(models.Model):
    """Заведение"""
    PRICE_LEVEL = [
        (1, '💰 - Бюджетно'),
        (2, '💰💰 - Средние цены'),
        (3, '💰💰💰 - Дорого'),
    ]

    name = models.CharField(max_length=100, verbose_name="Название")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    address = models.CharField(max_length=200, verbose_name="Адрес")
    description = models.TextField(verbose_name="Описание", blank=True)
    price_level = models.IntegerField(choices=PRICE_LEVEL, default=2, verbose_name="Ценовой уровень")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    website = models.URLField(blank=True, verbose_name="Сайт")
    opening_hours = models.CharField(max_length=100, blank=True, verbose_name="Часы работы")

    # Координаты для будущей карты
    latitude = models.FloatField(null=True, blank=True, verbose_name="Широта")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Долгота")

    # Изображение
    image = models.ImageField(upload_to='places/', blank=True, null=True, verbose_name="Фото")

    # Автоматические поля
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Вычисляемое поле для среднего рейтинга
    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum([r.rating for r in reviews]) / len(reviews)
        return 0

    class Meta:
        verbose_name = "Заведение"
        verbose_name_plural = "Заведения"
        ordering = ['name']

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзыв о заведении"""
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='reviews', verbose_name="Заведение")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Автор")
    author_name = models.CharField(max_length=50, verbose_name="Имя", default="Аноним")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Рейтинг",
        help_text="Оценка от 1 до 5"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв от {self.author_name} для {self.place.name}"