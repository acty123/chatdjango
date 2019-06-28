from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class CreateForm(UserCreationForm):

    class Meta:
        model= User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
        labels = {
            'username': 'User',
            'first_name': 'Name',
            'last_name': 'Last name',
            'email': 'Email',
        }

    # validations for registration
    
    def clean_email(self):
        check_email = self.cleaned_data['email']
        storage_email = User.objects.filter(email=check_email)

        if storage_email.exists():
            raise forms.ValidationError('Email already exists')

        if check_email.isspace():
            raise forms.ValidationError('Email cannot contain spaces')

        if len(check_email) == 0:
            raise forms.ValidationError('Email required')

        return check_email

    def clean_username(self):
        check_username = self.cleaned_data['username']

        if len(check_username) < 3:
            raise forms.ValidationError('User must has 4 characters or more')

        return check_username

