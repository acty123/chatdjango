from django.urls import path, re_path
from .views import CreateUser

app_name = 'person'

urlpatterns = [
    # path('', index, name="index"),
    re_path(r'^create/$', CreateUser.as_view(), name='create'),
]