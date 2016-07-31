from django.shortcuts import render
from Books.models import Books
import random

# Create your views here.

def index(request):
    book1 = random.choice(Books.objects.all())
    book2 = random.choice(Books.objects.all())
    book3 = random.choice(Books.objects.all())
    book4 = random.choice(Books.objects.all())

    return render(request, 'home/homes/home.html', {'book1' : book1,'book2' : book2, 'booke' : book3, 'book4' : book4 })
    
