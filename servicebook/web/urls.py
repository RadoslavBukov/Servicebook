from django.urls import path, include
from django.views.generic import CreateView

from servicebook.web.views import index, error

urlpatterns = (
    path('', index, name='index'),
    path('error/', error, name='404'),
)

