from django.contrib import admin
from .models import Category, Place, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'address', 'price_level', 'average_rating_display')
    list_filter = ('category', 'price_level')
    search_fields = ('name', 'address', 'description')
    readonly_fields = ('created_at', 'updated_at')

    def average_rating_display(self, obj):
        return f"{obj.average_rating:.1f} ⭐"

    average_rating_display.short_description = "Рейтинг"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('place', 'author_name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('text', 'author_name', 'place__name')
