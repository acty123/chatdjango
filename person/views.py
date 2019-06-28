from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import CreateView, FormView
from django.contrib.auth import login
from django.urls import reverse_lazy
from .forms import CreateForm

class CreateUser(CreateView):
    model = User
    template_name = 'person/create.html'
    form_class = CreateForm
    success_url = reverse_lazy('login')
    # success_url = reverse_lazy('chat:room',args=['public'])# user for login

class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('chat:room',args=['public'])

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)