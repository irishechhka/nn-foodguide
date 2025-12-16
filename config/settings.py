# Добавляем приложение
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'food',  # НАШЕ ПРИЛОЖЕНИЕ
]

# Настройки языка и времени
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'

# Настройки статических файлов
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # создадим папку позже

# Медиа файлы (для загрузки изображений)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# В конце файла добавляем
import os
if not os.path.exists('media'):
    os.makedirs('media')