from django.urls import path, include
# from .signals import *
from django.contrib.auth import views as auth_views

from servicebook.cars.views import RegisterCarView, details_car, edit_car, delete_car, CarsListView, TaxesListView, ServiceListView

urlpatterns = (
    path('register/', RegisterCarView.as_view(), name='register car'),
    path('cars/', CarsListView.as_view(), name='cars list'),
    # path('info/<int:pk>/', include([
    path('<user_id>/car/<slug:car_slug>/', include([
        path('', details_car, name='details car'),
        path('taxes/', TaxesListView.as_view(), name='taxes car'),
        path('sarvice/', ServiceListView.as_view(), name='service car'),
        path('edit/', edit_car, name='edit car'),
        path('delete/', delete_car, name='delete car'),
        ])),
    # path('register/', RegisterCarView.as_view(), name='register car'),
    # path('taxes/<int:pk>/', include([
    #     path('', CarInfoView.as_view(), name='details car'),
    #     path('edit/', CarEditView.as_view(), name='edit car'),
    #     path('delete/', CarDeleteView.as_view(), name='delete car'),
    #     ])),
    # path('register/', RegisterCarView.as_view(), name='register car'),
    # path('service/<int:pk>/', include([
    #     path('', CarInfoView.as_view(), name='details car'),
    #     path('edit/', CarEditView.as_view(), name='edit car'),
    #     path('delete/', CarDeleteView.as_view(), name='delete car'),
    #     ])),
)
