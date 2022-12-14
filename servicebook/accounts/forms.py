from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UsernameField
# from django.forms.widgets import DateInput
# from django.shortcuts import render

from servicebook.accounts.models import Profile

UserModel = get_user_model()


class LoginForm(AuthenticationForm):
    # Another way for adding a placeholders:
    # username = UsernameField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "autofocus":True,
    #             'placeholder': 'Email',
    #         }
    #     )
    # )
    # password = forms.CharField(
    #     strip=False,
    #     widget=forms.PasswordInput(
    #         attrs={
    #             'autocomplete': 'current-password',
    #             'placeholder': 'Password',
    #         }
    #     ),
    # )

    # Adding a placeholders with rewriting the __init__ method
    username = UsernameField()
    password = forms.PasswordInput()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})


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
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Repeat Password'})


# class EditUserForm(auth_forms.UserChangeForm):
#     class Meta:
#         model = Profile
#         # fields = '__all__' (not the case, we want to skip `slug`)
#         fields = ('first_name', 'last_name', 'date_of_birth', 'profile_picture')
#         # exclude = ('slug',)
#         labels = {
#             'first_name': 'First Name',
#             'last_name': 'Last Name',
#             'date_of_birth': 'Date of Birth',
#             'profile_picture': 'Profile Picture',
#
#         }
#         widgets = {
#             'first_name': forms.TextInput(
#                 attrs={
#                     'placeholder': 'First name'
#                 }
#             ),
#             'last_name': forms.TextInput(
#                 attrs={
#                     'placeholder': 'Last name'
#                 }
#             ),
#             'date_of_birth': forms.DateInput(
#                 attrs={
#                     'placeholder': 'mm/dd/yyyy',
#                     'type': 'date',
#                 }
#             ),
#             # 'profile_picture': forms.ImageField(
#             #     required=False
#             # ),
#         }


class EditUserForm(auth_forms.UserChangeForm):

    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'date_of_birth', 'profile_picture')
        field_classes = {
            # 'username': auth_forms.UsernameField,
            # 'profile_picture': forms.DateField,
        }

        # labels = {
        #     'first_name': 'First Name',
        #     'last_name': 'Last Name',
        #     'date_of_birth': 'Date of Birth',
        #     'profile_picture': 'Upload Image',
        # }
        #
        # widgets = {'date_of_birth': forms.DateInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter your First name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter your Last name'})
        self.fields['date_of_birth'].widget.attrs.update({'placeholder': 'Enter your Date of birth'})
        self.fields['date_of_birth'].help_text = "Note: Date should be in format YYYY-MM-DD !"
        self.fields['profile_picture'].widget.attrs.update({'placeholder': 'Profile picture'})
        self.fields['password'].help_text = None

# save the data for profile
#     def save(self, commit=True):
#         user = super().save(commit=commit)
#
#         profile = Profile(
#             first_name=self.cleaned_data['first_name'],
#             last_name=self.cleaned_data['last_name'],
#             date_of_birth=self.cleaned_data['date_of_birth'],
#             profile_picture=self.cleaned_data['profile_picture'],
#             user=user,
#         )
#         if commit:
#             profile.save()
#
#         return user


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