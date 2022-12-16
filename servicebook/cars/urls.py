from django.urls import path, include
from django.contrib.auth import views as auth_views

from servicebook.cars.views import RegisterCarView, details_car, edit_car, \
    delete_car, CarsListView, delete_car_tax, add_car_tax,\
    details_car_taxes, details_car_service, add_car_service, delete_car_service

urlpatterns = (
    path('register/', RegisterCarView.as_view(), name='register car'),
    path('cars/', CarsListView.as_view(), name='cars list'),
    path('<user_id>/car/<slug:car_slug>/', include([
        path('', details_car, name='details car'),
        path('taxes/', include([
            path('', details_car_taxes, name='taxes list'),
            path('add/', add_car_tax, name='add tax'),
            path('delete/<tax_id>/', delete_car_tax, name='delete car tax'),
        ])),
        path('sarvice/', include([
            path('', details_car_service, name='services list'),
            path('add/', add_car_service, name='add service'),
            path('delete/<service_id>/', delete_car_service, name='delete car service'),
        ])),
        path('edit/', edit_car, name='edit car'),
        path('delete/', delete_car, name='delete car'),
    ])),
)
