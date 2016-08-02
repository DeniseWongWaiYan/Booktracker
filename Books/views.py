from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login #, logout, login_then_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Booktracker.common.decorators import ajax_required
from django.views.decorators.http import require_POST
from .forms import BookSearchForm, BookCreateForm, ChallengeForm, ChallengeItemForm
from django.db.models import Count, Q
from .models import Books, Challenge
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from Booktracker.common.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action



# Create your views here.
def dummy(request):
    #oddly necessary for findbookview to work
    pass

def findbookview(request):
    if request.method == 'POST':
        searchform = BookSearchForm(request.POST)
        
        if searchform.is_valid():
            cd = searchform.cleaned_data
            findbooks = Books.objects.filter(Q(title=cd['title']) | Q(author=cd['author']) | Q(ISBN=cd['ISBN']))

            if findbooks.count() == 0:
                if '_add' in request.POST:
                    addbookconfirm = BookCreateForm(data=request.POST, files=request.FILES)
                    if addbookconfirm.is_valid():
                        c_d = addbookconfirm.cleaned_data
                        Books.objects.create(title=c_d['title'], author=c_d['author'], ISBN=c_d['ISBN'], total_likes=0)

                        return render(request, 'book/added.html', {'addbookconfirm': addbookconfirm})

                else:
                    addbook = BookCreateForm()
                    addbook.fields['title'].initial = cd['title']
                    addbook.fields['author'].initial = cd['author']
                    addbook.fields['ISBN'].initial = cd['ISBN']

                    return render(request, 'book/notfound.html', {'addbook': addbook})
                
            else:
                 return render(request, 'book/foundbook.html', {'findbooks': findbooks})           

    else:
        searchform = BookSearchForm()


    return render(request, 'book/book.html', {'searchform': searchform })


@login_required
def BookListView(request):
    books = Books.objects.all()
    paginator = Paginator(books, 8)
    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        books = paginator.page(pagniator.num_pages)
    if request.is_ajax():
        return render(request, 'book/books/list_ajax.html', {'onpage':'books', 'books':books})
    return render(request, 'book/books/list.html', {'onpage':'books', 'books': books})
    


@login_required
def BookDetailView(request, slug, ISBN):
    book = get_object_or_404(Books, slug=slug, ISBN=ISBN)
 #   total_views = r.incr('book:{}:views'.format(book.id))
    reviews = Books.reviews.filter(active=True)
    
    return render(request, 'book/books/detail.html', {'section': 'challenges', 'book': book, })

@ajax_required
@login_required
@require_POST
def book_like(request):
    book_id = request.POST.get('id')
    action = request.POST.get('action')
    
    if book_id and action:
        try:
            book = Books.objects.get(id=book_id)
            if action == 'like':
                book.users_like.add(request.user)
            else:
                book.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})



@login_required
def ChallengeCreateView(request):
    if request.method == 'POST':
        new_chal = ChallengeForm(request.POST)
        if new_chal.is_valid():
            cd = new_chal.cleaned_data
            
            challenge = new_chal.save(commit=False)
            challenge.chalname=cd['chal_name']
            challenge.save()

            books = Books.objects.all()

            return render(request, 'book/books/additems.html', {'challenge': challenge, 'new_chal': new_chal, 'books': books})
    else:
        new_chal = ChallengeForm()
    return render(request, 'book/books/challengecreate.html', {'new_chal': new_chal, 'new_chal': new_chal})
        
@ajax_required
@login_required
@require_POST
def add_book(request):
    challenge_id = request.POST.get('id')
    book_id = request.POST.get('bookid')
    action = request.POST.get('action')
    
    if challenge_id and book_id and action:
        try:
            challenge = Challenge.objects.get(id=challenge_id)
            book = Books.objects.get(id=book_id)
            if action == 'add':
                challenge.bookinchallenge.add(book)
            else:
                challenge.bookinchallenge.remove(book)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})
       
     

