from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
import json

User = get_user_model()

def index(request):
    return render(request, 'chat/index.html', {})

@login_required
def room(request, room_name):
    person = User.objects.filter(username=request.user.username)
    
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
        'person': person,
    })