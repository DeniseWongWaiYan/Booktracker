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
def findbookview(request):
    if request.method == 'POST' and '_search' in request.POST:
        searchform = BookSearchForm(request.POST)
        
        if searchform.is_valid():
            cd = searchform.cleaned_data
            findbooks = Books.objects.filter(Q(title=cd['title']) | Q(author=cd['author']) | Q(ISBN=cd['ISBN']))

            if findbooks.count() == 0:
                if '_add' in request.POST:
                    addbookconfirm = BookCreateForm(request.POST)
                    c_d = addbookconfirm.cleaned_data
                    addbookconfirm.save(commit=False)
                    addbookconfirm.title = c_d['title']
                    addbookconfirm.author = c_d['author']
                    addbookconfirm.ISBN = c_d['ISBN']
                    addbookconfirm.save()

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
