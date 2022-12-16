from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

from django.contrib.auth.forms import AuthenticationForm, UsernameField


from servicebook.accounts.models import Profile

UserModel = get_user_model()


class LoginForm(AuthenticationForm):
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


class EditUserForm(auth_forms.UserChangeForm):

    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
                    'first_name': forms.TextInput(
                        attrs={
                            'class': 'form_control',
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
                            'placeholder': 'mm/dd/yyyy',
                            'type': 'date',
                        }
                    ),
                    'profile_picture': forms.ImageField(
                        required=False
                    ),
                }