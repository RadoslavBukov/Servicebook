from django.http import HttpResponseForbidden
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
from servicebook.cars.forms import RegisterCarForm, EditCarForm, CarDeleteForm,\
    TaxCreateForm, TaxDeleteForm, ServiceCreateForm, ServiceDeleteForm
from servicebook.cars.utils import get_car_by_slug_and_userid, get_taxes_by_carid_and_userid, \
    get_tax_by_taxid, get_services_by_carid_and_userid, get_service_by_serviceid, user_is_owner
from servicebook.core.model_mixins import UserOwnerMixin
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

    if not user_is_owner(request, user_id):
        return HttpResponseForbidden()

    car = get_car_by_slug_and_userid(car_slug, user_id)

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
    car = get_car_by_slug_and_userid(car_slug, user_id)

    if not user_is_owner(request, user_id):
        return HttpResponseForbidden()

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
    car = get_car_by_slug_and_userid(car_slug, user_id)

    if not user_is_owner(request, user_id):
        return HttpResponseForbidden()

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
        'car_photo': car.car_photo,
    }

    return render(
        request,
        'cars/car-delete-page.html',
        context,
    )

@login_required
def add_car_tax(request, user_id, car_slug):
    car = get_car_by_slug_and_userid(car_slug, user_id)

    if not user_is_owner(request, user_id):
        return HttpResponseForbidden()

    if request.method == 'GET':
        form = TaxCreateForm()
    else:
        form = TaxCreateForm(request.POST)
        if form.is_valid():
            tax = form.save(commit=False)
            tax.user = request.user
            tax.car_id = car.id
            tax.save()
            return redirect('taxes list', user_id=car.user_id, car_slug=car.slug)

    context = {
        'car_slug': car_slug,
        'user_id': user_id,
        'add_form': form,
    }

    return render(request, 'taxes/taxes_list.html', context)

@login_required
def delete_car_tax(request, user_id, car_slug, tax_id):
    car = get_car_by_slug_and_userid(car_slug, user_id)
    tax = get_tax_by_taxid(tax_id)

    if not user_is_owner(request, user_id):
        return HttpResponseForbidden()

    if request.method == 'GET':
        form = TaxDeleteForm(instance=tax)
    else:
        form = TaxDeleteForm(request.POST, instance=tax)
        if form.is_valid():
            form.save()
            return redirect('taxes list', user_id=car.user_id, car_slug=car.slug)

    context = {
        'car_slug': car_slug,
        'user_id': user_id,
        'tax_id': tax_id,
        'del_form': form,
    }

    return render(request, 'taxes/taxes_list.html', context)


@login_required()
def details_car_taxes(request, user_id, car_slug):
    car = get_car_by_slug_and_userid(car_slug, user_id)
    car_id = car.id
    taxes = get_taxes_by_carid_and_userid(car_id, user_id)

    if not user_is_owner(request, user_id):
        return HttpResponseForbidden()

    context = {
        'car': car,
        'taxes': taxes,
        'add_tax_form': TaxCreateForm,
        'car_slug': car_slug,
        'user_id': user_id,
        'is_owner': car.user == request.user,
        'tax_id': 0,
    }

    return render(
        request,
        'taxes/taxes_list.html',
        context,
    )

# class TaxesListView(views.ListView, LoginRequiredMixin):
#     template_name = 'taxes/taxes_list.html'
#     model = CarTaxes
#
#
#     def get_queryset(self):
#         query_set = CarTaxes.objects.filter(user_id=self.request.user.id)
#         return query_set
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         cars_taxes = CarTaxes.objects.filter(user_id=self.request.user.id)
#         context['cars_taxes'] = cars_taxes
#
#         return context


@login_required
def add_car_service(request, user_id, car_slug):
    car = get_car_by_slug_and_userid(car_slug, user_id)

    if not user_is_owner(request, user_id):
        return HttpResponseForbidden()

    if request.method == 'GET':
        form = ServiceCreateForm()
    else:
        form = ServiceCreateForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.user = request.user
            service.car_id = car.id
            service.save()
            return redirect('services list', user_id=car.user_id, car_slug=car.slug)

    context = {
        'car_slug': car_slug,
        'user_id': user_id,
        'add_form': form,
    }

    return render(request, 'taxes/services_list.html', context)

@login_required
def delete_car_service(request, user_id, car_slug, service_id):
    car = get_car_by_slug_and_userid(car_slug, user_id)
    service = get_service_by_serviceid(service_id)

    if not user_is_owner(request, user_id):
        return HttpResponseForbidden()

    if request.method == 'GET':
        form = ServiceDeleteForm(instance=service)
    else:
        form = ServiceDeleteForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('services list', user_id=car.user_id, car_slug=car.slug)

    context = {
        'car_slug': car_slug,
        'user_id': user_id,
        'service_id': service_id,
        'del_service_form': form,
    }

    return render(request, 'taxes/services_list.html', context)

# class TaxesListView(views.ListView, LoginRequiredMixin):
#     template_name = 'taxes/taxes_list.html'
#     model = CarTaxes
#
#
#     def get_queryset(self):
#         query_set = CarTaxes.objects.filter(user_id=self.request.user.id)
#         return query_set
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         cars_taxes = CarTaxes.objects.filter(user_id=self.request.user.id)
#         context['cars_taxes'] = cars_taxes
#
#         return context

@login_required()
def details_car_service(request, user_id, car_slug):
    car = get_car_by_slug_and_userid(car_slug, user_id)
    car_id = car.id
    services = get_services_by_carid_and_userid(car_id, user_id)

    if not user_is_owner(request, user_id):
        return HttpResponseForbidden()

    context = {
        'car': car,
        'services': services,
        'add_service_form': ServiceCreateForm,
        'car_slug': car_slug,
        'user_id': user_id,
        'is_owner': car.user == request.user,
        'service_id': 0,
    }

    return render(
        request,
        'taxes/services_list.html',
        context,
    )


# Asdf123!@