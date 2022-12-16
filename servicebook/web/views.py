from django.contrib.auth import views
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

def index(request):

    if request.user.is_authenticated:
        full_name = request.user.profile.get_full_name()
    else:
        full_name = ""

    context = {
        'full_name': full_name,
    }

    return render(request, 'core/index.html', context)

def error(request):
    return render(request, 'core/404.html')
