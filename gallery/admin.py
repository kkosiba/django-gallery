from django.contrib import admin

from .models import Category
from .models import Picture
from .models import Profile

# Register your models here.
admin.site.register(Category)
admin.site.register(Picture)
admin.site.register(Profile)