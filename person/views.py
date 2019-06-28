from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import CreateView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy
from .forms import CreateForm

class CreateUser(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'person/create.html'
    form_class = CreateForm
    success_url = reverse_lazy('login')
    success_message = 'User created'

    def form_valid(self, form):
        data = form.instance
        data.user_id = self.request.user.id
        self.object = form.save()
        return super(CreateUser, self).form_valid(form)


    def dispatch(self, *args, **kwargs):
        return super(CreateUser, self).dispatch(*args, **kwargs)


class LoginView(SuccessMessageMixin, FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('chat:room',args=['public'])

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    