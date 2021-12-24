from django.contrib import admin

from .models import User, Title, Genre, Category

admin.site.register(User)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
