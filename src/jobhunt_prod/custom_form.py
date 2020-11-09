from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.utils.translation import gettext, gettext_lazy as _
class UserForm(UserCreationForm):
    username=forms.CharField(max_length=15)
    email=forms.CharField(max_length=30)
    first_name=forms.CharField(max_length=20)
    last_name=forms.CharField(max_length=20)
    custom_messages = {
        'email_dups': _('Email is already registered'),
    }

    class Meta:
        model=User
        fields=("username"  , "first_name", "last_name" ,  "email" )

    #is django identifying the clean" or can i make the name arbitrary?
    def clean_email(self ):
        email=self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                self.custom_messages['email_dups'], 
                code='invalid')
        return email
            
            
            
        