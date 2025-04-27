from atexit import register
from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    search_fields=['name']

class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']


admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)
admin.site,register(Favourite)