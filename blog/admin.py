from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
# admin.site.register(Blog)
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title')
    
admin.site.register(Comment)
admin.site.register(Reply)
