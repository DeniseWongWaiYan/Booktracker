from django.contrib import admin
from .models import Books, Challenge

# Register your models here.

class BooksAdmin(admin.ModelAdmin):
    list_display = ['title','author', 'ISBN']


admin.site.register(Books, BooksAdmin)

class ChalAdmin(admin.ModelAdmin):
    list_display = ['chalname']
    
admin.site.register(Challenge, ChalAdmin)

