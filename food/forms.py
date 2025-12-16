from django import forms
from .models import Place, Review

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = [
            'name', 'category', 'address', 'description',
            'price_level', 'phone', 'website', 'opening_hours',
            'latitude', 'longitude', 'image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.TextInput(attrs={'placeholder': 'ул. Примерная, д. 1'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 (999) 123-45-67'}),
        }
        labels = {
            'name': 'Название заведения*',
            'category': 'Категория*',
            'address': 'Адрес*',
            'description': 'Описание',
            'price_level': 'Ценовой уровень',
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author_name', 'text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Поделитесь вашими впечатлениями...'
            }),
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
        }
        labels = {
            'author_name': 'Ваше имя*',
            'text': 'Текст отзыва*',
            'rating': 'Оценка*',
        }