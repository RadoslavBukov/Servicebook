from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

from servicebook.accounts.models import Profile

UserModel = get_user_model()


class RegisterUserForm(auth_forms.UserCreationForm):

    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD, 'password1', 'password2')

    # save with empty profile
    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(
            user=user,
        )
        if commit:
            profile.save()

        return user


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

class EditUserForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD, 'password1', 'password2', 'first_name', 'last_name', 'profile_picture')

    # save with data for profile
    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            profile_picture=self.cleaned_data['profile_picture'],
            user=user,
        )
        if commit:
            profile.save()

        return user



# QwerTy123!