from django import forms
from django.forms import ModelForm
from .models import Books, Challenge

class BookForm(forms.Form):   
    title = forms.CharField(max_length=200)
    author = forms.CharField(max_length=200)
    ISBN = forms.IntegerField()
    
    
    class Meta:
         model = Books

    


class ChallengeForm(forms.ModelForm):
    chal_name = forms.CharField(max_length=200)

    class Meta:
        model = Challenge
        fields = ('chal_name',)
 
class ChallengeItemForm(forms.Form):
    book_in_challenge = forms.ModelChoiceField(queryset=Books.objects.all().values())

    class Meta:
        model = Challenge
        fields = ('bookinchallenge',)

    
 
