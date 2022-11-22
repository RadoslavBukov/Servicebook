from django.contrib.auth import views
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def error(request):
    return render(request, 'core/404_1.html')
