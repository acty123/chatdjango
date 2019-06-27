from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreateForm

class CreateUser(CreateView):
    model = User
    template_name = 'person/create.html'
    form_class = CreateForm
    # success_url = reverse_lazy('person:login')
    success_url = reverse_lazy('chat:room',args=['public'])# user for login