from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'email')
admin.site.register(Follow)
