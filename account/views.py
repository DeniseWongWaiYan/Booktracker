from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login #, logout, login_then_logout
from .forms import LoginForm, UserRegistrationForm, UserEdit, ProfileEdit
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from django.contrib.auth.models import User
from actions.utils import create_action
from Booktracker.common.decorators import ajax_required
from django.views.decorators.http import require_POST
from .models import Connection
from actions.models import Action

# Create your views here.
def LoginView(request):

    if request.method =='POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active():
                    login(request, user)
                    return HttpResponse("Welcome aboard - suckers! I am Hexachlorophene J. Goodforttune, Kidnapper At-Large, and Devourer of Tortoises par Excellence, at your service.")

                else:
                    return HttpResponse("You're like the limit in this function. DNE!")
            else:
                return HttpResponse("If at first you don't succeed, try, try, try again. (Your login is invalid.)")

    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def UserRegistrationView(request):

    if request.method == 'POST':
        create_user_form = UserRegistrationForm(request.POST)

        if create_user_form.is_valid():
            new_user = create_user_form.save(commit=False)

            new_user.set_password(
                create_user_form.cleaned_data['password'])

            new_user.save()
            create_action(new_user, 'has created an account')
            profile = Profile.objects.create(user=new_user)

            return render(request, 'account/register_done.html', {'new_user': new_user})

    else:
        create_user_form = UserRegistrationForm()

    return render(request, 'account/register.html', {'create_user_form': create_user_form})

#@login_required
def TableofContents(request):
    actions = Action.objects.all()
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids).select_related('user', 'user__profile').prefetch_related('target')
    actions = actions[:20]

    return render(request, 'account/dashboard.html', {'onpage': 'dashboard',
                                                      'actions': actions})

@login_required
def UserEditView(request):
    if request.method == 'POST':
        user_edit_form = UserEdit(instance=request.user, data=request.POST)
        profile_edit_form = ProfileEdit(instance=request.user.profile, data=request.POST, files=request.FILES)
                

        if user_edit_form.is_valid() and profile_edit_form.is_valid():
            user_edit_form.save()
            profile_edit_form.save()
            messages.success(request, 'Profile sucessfully edited.')

    else:
        user_edit_form = UserEdit(instance=request.user)
        profile_edit_form = ProfileEdit(instance=request.user.profile)
        messages.error(request, 'Whoops...there was an error updating your profile.')

    return render(request, 'account/edit.html', {'user_edit_form': user_edit_form, 'profile_edit_form': profile_edit_form} )
   
@login_required
def nerds_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'account/user/list.html', {'onpage':'nerds', 'users': users} )

@login_required
def nerds_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)

    return render(request,
'account/user/detail.html',
{'onpage': 'people',
'user': user})

@ajax_required
@require_POST
@login_required
def nerds_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')

    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                create_action(request.user, 'is following', user)
                Connection.objects.get_or_create(user_from=request.user, user_to=user)
                
            else:
                Connection.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})

                               

"""
#Code for following nerds
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .models import Connection

@ajax_required
@require_POST
@login_required

def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')

    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Connection.objects.get_or_create(user_from = request.user,user_to=user)

            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()

            return JsonResponse({'status':'ok'})
        
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})

"""
