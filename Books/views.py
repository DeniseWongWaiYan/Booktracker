from django.shortcuts import render
from .models import Books, Challenge
from .forms import BookSearchForm, ChallengeForm, ChallengeItemForm
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.forms.formsets import formset_factory, BaseFormSet
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from Booktracker.common.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action
"""
#Redis
import redis
from django.conf import settings
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_HOST, db=settings.REDIS_DB)


"""

# Create your views here.

def findbookview(request):
    if request.method == 'POST':
        searchform = BookSearchForm(request.POST)

        if searchform.is_valid():
            cd = searchform.cleaned_data
            findbooks = Books.objects.filter(title=cd['title'])

            if findbooks.count() != 0:
                return render(request, 'book/foundbook.html', {'findbooks': findbooks})

            else:
                return render(request, 'book/notfound.html', {'findbooks': findbooks})

                

    else:
        searchform = BookSearchForm()

    return render(request, 'book/book.html', {'searchform': searchform})

"""
@login_required
def SearchBookView(request):
    if request.method == 'POST':
        bookform = BookForm(request.POST)
        if bookform.is_valid():
            cd = bookform.cleaned_data
            try:
                findbook = Books.objects.get(title=cd['title'], author=cd['author'], ISBN=cd['ISBN'])
                num_likes = findbook.users_like.count()
                slug = findbook.slug

                return render(request, 'book/foundbook.html', {'findbook': findbook, 'title':findbook.title, 'num_likes' : num_likes})

            except Books.DoesNotExist:
                book = Books.objects.create(title=cd['title'], author=cd['author'], ISBN=cd['ISBN'])
    else:
        bookform = BookForm()

    return render(request, 'book/book.html', {'onpage': 'books', 'bookform': bookform})
"""

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
       
     


"""

 if request.method == 'POST':
        chal_item = ChallengeItemForm(request.POST)
        if chal_item.is_valid():
            chal_item.save(commit=False)
            chal_item.booksinchallenge = cd['book_in_challenge']
            new_chal.booksinchallenge.save_m2m()

        return render(request, 'book/books/dashboard.html', {'challenge': challenge, 'new_chal': new_chal, 'chal_item': chal_item, 'books' : books})

    else:
        chal_item = ChallengeItemForm()



    ChalItemFormSet = modelformset_factory(Challenge, form=ChallengeItemForm)
    if request.method == 'POST':
        try:
            whole_chal_form = ChallengeForm(request.POST)
            chal_item_formset = ChalItemFormSet(book_in_challenge=request.POST.get('book_in_challenge'))

            if whole_chal_form.is_valid and chal_item_formset.is_valid():

                chal_items = chal_item_formset.save()
                      
                for chal_item in chal_items:
                    chal_item.save()

                whole_chal_form.save_m2m()
               
                return render(request, 'books/done.html', {'chal_item_formset': chal_item_formset}) # Redirect to a 'success' page

        except ValidationError:
            whole_chal_form = ChallengeForm()
            chal_item_formset = ChalItemFormSet()
            return HttpResponse({'chal_item_formset': chal_item_formset, 'whole_chal_form': whole_chal_form} , chal_item_formset.errors)
        
            #return render(request, 'base.html', {'chal_item_formset': chal_item_formset, 'whole_chal_form': whole_chal_form} )


    else:
        whole_chal_form = ChallengeForm()
        chal_item_formset = ChalItemFormSet()

    return render(request, 'book/books/challengecreate.html', {'chal_item_formset': chal_item_formset, 'whole_chal_form': whole_chal_form})


@login_required
def ChallengeCreateView(request):
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False
    ChallengeFormset = formset_factory(ChallengeForm, max_num=53, formset=RequiredFormSet)
    if request.method == 'POST': # If the form has been submitted...
        chal_create_form = ChallengeForm(request.POST) # A form bound to the POST data
        # Create a formset from the submitted data
        chal_create_formset = ChallengeFormset(request.POST)

        if chal_create_form.is_valid() and chal_create_formset.is_valid():
            chal_list = chal_create_form.save()
            for form in chal_create_formset.forms:
                book_chal= form.save(commit=False)
                book_chal.list = chal_list
                book_chal.save()
            return HttpResponseRedirect('thanks') # Redirect to a 'success' page
    else:
        chal_create_form= ChallengeForm()
        chal_create_formset = ChallengeFormset()

    return render_to_response('book/books/challengecreate.html', {'chal_create_form': chal_create_form, 'chal_create_formset': chal_create_formset

def ChallengeCreateView(request):
    books = get_books(request)
    form  = ChallengeForm(request.Post or None, extra=books)
    if form.is_valid():
        for (book) in form.books():
            save_bookinchal(request, book)
        return redirect('chal sucess')
    return render_to_response('book/challenge.html', {'form': form}) """
