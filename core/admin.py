from django.contrib import admin
from .models import Category, Problem, Application

admin.site.register(Category)
admin.site.register(Problem)
admin.site.register(Application)