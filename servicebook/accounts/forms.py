from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.forms.widgets import DateInput
from django.shortcuts import render

from servicebook.accounts.models import Profile

UserModel = get_user_model()


class RegisterUserForm(auth_forms.UserCreationForm):

    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD, 'password1', 'password2')
        field_classes = {
            'username': auth_forms.UsernameField,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None


class EditUserForm(auth_forms.UserChangeForm):
    # first_name = forms.CharField(required=False, help_text='Optional')
    first_name = forms.CharField(widget=forms.TextInput(attrs={"autofocus":True, "placeholder":"First name"}))
    last_name = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD, 'first_name', 'last_name', 'date_of_birth', 'profile_picture')
        field_classes = {
            'username': auth_forms.UsernameField,
        }
        labels = {
            'first_name': 'First Nscscame',
            'last_name': 'Last Namscsce',
            'date_of_birth': 'Date of Birth',
            'personal_photo': 'Upload Image',
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'First name'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Last name'
                }
            ),
            'date_of_birth': forms.DateInput(
                attrs={
                    'placeholder': 'yyyy-mm-dd',
                    'type': 'date',
                }
            ),
            'personal_photo': forms.URLInput(
                attrs={
                    'placeholder': 'Upload image',
                }
            )
        }

    # save with data for profile
    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            profile_picture=self.cleaned_data['profile_picture'],
            user=user,
        )
        if commit:
            profile.save()

        return user


# class UserPasswordChangeForm(auth_forms.PasswordChangeForm):
#     pass
#     # first_name = forms.CharField(required=False)
#     # last_name = forms.CharField(required=False)
#     #
#     class Meta:
#         model = UserModel
#         fields = (UserModel.USERNAME_FIELD,)
#         # field_classes = {
#         #     'username': auth_forms.UsernameField,
#         # }
#         labels = {
#             'first_name': 'First Name',
#             'last_name': 'Last Name',
#             'date_of_birth': 'Date of Birth',
#             'personal_photo': 'Upload Image',
#         }
#
#     def __init__(self, user, *args, **kwargs):
#         self.user = user
#         super().__init__(*args, **kwargs)


# QwerTy123!