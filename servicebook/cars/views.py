from django.shortcuts import render, redirect
import profile

from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views, get_user_model, login
from django.contrib.auth.decorators import login_required

from servicebook.cars.models import CarInfo, CarTaxes, CarService
from servicebook.cars.forms import RegisterCarForm, EditCarForm, CarDeleteForm
from servicebook.cars.utils import get_car_by_name_and_username
from servicebook.core.utils import is_owner

# Always get the *user model* with `get_user_model`
UserModel = get_user_model()


class RegisterCarView(views.CreateView, LoginRequiredMixin):
    template_name = 'cars/car-create-page.html'
    form_class = RegisterCarForm
    success_url = reverse_lazy('cars list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# @login_required
# def add_car(request):
#     if request.method == 'GET':
#         form = RegisterCarForm()
#     else:
#         form = RegisterCarForm(request.POST)
#         if form.is_valid():
#             car = form.save(commit=False)
#             car.user = request.user
#             car.save()
#             return redirect('cars list', pk=request.user.pk)
#
#     context = {
#         'form': form,
#     }
#
#     return render(request, 'cars/car-create-page.html', context)



class CarsListView(views.ListView, LoginRequiredMixin):
    model = CarInfo
    paginate_by = 3
    context_object_name = 'cars_list'

    def get_queryset(self):
        query_set = CarInfo.objects.filter(user_id=self.request.user.id)

        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cars_count = CarInfo.objects.filter(user_id=self.request.user.id)
        context['cars_count'] = cars_count.count()

        return context

# class CarInfoView(views.DetailView, LoginRequiredMixin):
#     template_name = 'cars/car-details-page.html'
#     model = CarInfo
#     # form_class = EditCarForm
#
#     def get_queryset(self):
#         queryset = super(CarInfoView, self).get_queryset()
#         x = queryset.filter(slug=CarInfo.slug, user_id=self.request.user)
#         return queryset.filter(user_id=self.request.user)

@login_required()
def details_car(request, user_id, car_slug):
    car = get_car_by_name_and_username(car_slug, user_id)

    context = {
        'car': car,
        'brand': car.brand,
        'model': car.model,
        'year': car.year_of_manufacture,
        'engine': car.engine,
        'fuel': car.fuel,
        'car_photo': car.car_photo,
        'is_owner': car.user == request.user,
    }

    return render(
        request,
        'cars/car-details-page.html',
        context,
    )


@login_required()
def edit_car(request, user_id, car_slug):
    car = get_car_by_name_and_username(car_slug, user_id)

    if request.method == 'GET':
        form = EditCarForm(instance=car)
    else:
        form = EditCarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('details car', user_id=user_id, car_slug=car_slug)

    context = {
        'form': form,
        'car_photo': car.car_photo,
        'car_slug': car_slug,
        'user_id': user_id,
    }

    return render(
        request,
        'cars/car-edit-page.html',
        context,
    )

@login_required()
def delete_car(request, user_id, car_slug):
    car = get_car_by_name_and_username(car_slug, user_id)

    if request.method == 'GET':
        form = CarDeleteForm(instance=car)
    else:
        form = CarDeleteForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('cars list')

    context = {
        'form': form,
        'car_slug': car_slug,
        'user_id': user_id,
        'brand': car.brand,
        'model': car.model,
    }

    return render(
        request,
        'cars/car-delete-page.html',
        context,
    )



class TaxesListView(views.ListView, LoginRequiredMixin):
    model = CarTaxes
    paginate_by = 3

    def get_queryset(self):
        query_set = CarInfo.objects.filter(user_id=self.request.user.id)

        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cars_count = CarInfo.objects.filter(user_id=self.request.user.id)
        context['cars_count'] = cars_count.count()

        return context

class ServiceListView(views.ListView, LoginRequiredMixin):
    model = CarService
    paginate_by = 3

    def get_queryset(self):
        query_set = CarInfo.objects.filter(user_id=self.request.user.id)

        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cars_count = CarInfo.objects.filter(user_id=self.request.user.id)
        context['cars_count'] = cars_count.count()

        return context

# Asdf123!@