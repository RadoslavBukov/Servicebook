from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm, AuthenticationForm, UsernameField
from django.forms.widgets import DateInput
from django.shortcuts import render

from servicebook.cars.models import CarInfo, CarTaxes, CarService
from servicebook.core.form_mixins import DisabledFormMixin

UserModel = get_user_model()

class RegisterCarForm(forms.ModelForm):

    class Meta:
        model = CarInfo
        fields = ('brand', 'model', 'year_of_manufacture', 'engine', 'fuel', 'car_photo')


class CarBaseForm(forms.ModelForm):
    class Meta:
        model = CarInfo
        fields = ('brand', 'model', 'year_of_manufacture', 'engine', 'fuel', 'car_photo')
        labels = {
            'brand': 'Brand',
            'model': 'Model',
            'year_of_manufacture': 'Year of Manufacture',
            'engine': 'Engine',
            'fuel': 'Fuel',
            'car_photo': 'Car Photo',
        }
        widgets = {
            'brand': forms.TextInput(
                attrs={
                    'placeholder': 'Car Brand'
                }
            ),
            'model': forms.TextInput(
                attrs={
                    'placeholder': 'Car model'
                }
            ),
            'year_of_manufacture': forms.TextInput(
                attrs={
                    'placeholder': 'Year of manufacture',
                    # 'type': 'date',
                }
            ),
            'engine': forms.TextInput(
                attrs={
                    'placeholder': 'Car Engine'
                }
            ),
            'fuel': forms.TextInput(
                attrs={
                    'placeholder': 'Car Fuel'
                }
            ),
            'car_photo': forms.URLInput(
                attrs={
                    'placeholder': 'URL Car Photo',
                }
            )
        }


class EditCarForm(DisabledFormMixin, CarBaseForm):
    disabled_fields = ('brand',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._disable_fields()


class CarDeleteForm(CarBaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__set_hidden_fields()

    def save(self, commit=True):
        if commit:

            CarTaxes.objects.filter(car_id=self.instance.id) \
                .delete()  # one-to-many
            CarService.objects.filter(car_id=self.instance.id) \
                .delete()  # one-to-many

            self.instance.delete()
        return self.instance

    def __set_hidden_fields(self):
        for _, field in self.fields.items():
            field.widget = forms.HiddenInput()

class TaxCreateForm(forms.ModelForm):
    class Meta:
        model = CarTaxes
        fields = ('type', 'valid_to', 'price')
        labels = {
            'type': 'Type:',
            'valid_to': 'Valid to:',
            'price': 'Price:',
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['type'].widget.attrs.update({'placeholder': 'Type'})
            self.fields['valid_to'].widget.attrs.update({'placeholder': 'Valid to'})
            self.fields['valid_to'].help_text = "Date should be in format yyyy-mm-dd"
            self.fields['price'].widget.attrs.update({'placeholder': 'price'})


class TaxDeleteForm(TaxCreateForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__set_hidden_fields()

    def save(self, commit=True):
        if commit:
            self.instance.delete()
        return self.instance

    def __set_hidden_fields(self):
        for _, field in self.fields.items():
            field.widget = forms.HiddenInput()


class ServiceCreateForm(forms.ModelForm):
    class Meta:
        model = CarService
        fields = ('date_of_service', 'mileage', 'symptoms', 'root_cause', 'repair', 'price')
        widgets = {'date_of_service': forms.DateInput}


class ServiceDeleteForm(TaxCreateForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__set_hidden_fields()

    def save(self, commit=True):
        if commit:
            self.instance.delete()
        return self.instance

    def __set_hidden_fields(self):
        for _, field in self.fields.items():
            field.widget = forms.HiddenInput()