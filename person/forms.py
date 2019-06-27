from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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
