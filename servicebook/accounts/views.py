import profile

from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views, get_user_model, login
from django.contrib.auth.decorators import login_required

from servicebook.cars.utils import user_is_owner
from servicebook.accounts.forms import RegisterUserForm, EditUserForm, LoginForm
from servicebook.accounts.models import Profile
from servicebook.core.model_mixins import UserOwnerMixin

# Always get the *user model* with `get_user_model`
UserModel = get_user_model()


class RegisterView(views.CreateView):
    template_name = 'accounts/register-page.html'
    # form_class = UserCreateForm
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')

    # Signs the user in, after successful regisration
    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result

    # def post(self, request, *args, **kwargs):
    #     response = super().post(request, *args, **kwargs)
    #     login(request, self.object)
    #     return response


class SignInView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'accounts/login-page.html'
    success_url = reverse_lazy('index')


class SignOutView(auth_views.LogoutView, LoginRequiredMixin):
    next_page = reverse_lazy('index')


class UserDetailsView(views.DetailView, LoginRequiredMixin, UserOwnerMixin):
    template_name = 'accounts/profile-details-page.html'
    model = UserModel
    # form_class = EditUserForm

    # profile = Profile.objects.filter(pk=object.id).get()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = Profile.objects.filter(pk=self.request.user).get()

        context['is_owner'] = self.request.user == self.object
        context['full_name'] = profile.get_full_name()
        context['date_of_birth'] = profile.date_of_birth
        context['profile_picture'] = profile.profile_picture

        return context

    def get(self, *args, **kwargs):
        user_id = kwargs['pk']

        if not user_is_owner(self.request, user_id):
            return redirect('details user', pk=self.request.user.pk)

        return super().get(*args, **kwargs)


class UserEditView(views.UpdateView, LoginRequiredMixin):
    template_name = 'accounts/profile-edit-page.html'
    model = Profile
    # form_class = EditUserForm
    fields = ('first_name', 'last_name', 'date_of_birth', 'profile_picture')

    def get_success_url(self):
        return reverse_lazy('details user', kwargs={
            'pk': self.request.user.pk,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = Profile.objects.filter(pk=self.request.user).get()

        context['profile_picture'] = profile.profile_picture

        return context

    def get(self, *args, **kwargs):
        user_id = kwargs['pk']

        if not user_is_owner(self.request, user_id):
            return redirect('edit user', pk=self.request.user.pk)

        return super().get(*args, **kwargs)
class UserDeleteView(views.DeleteView, LoginRequiredMixin, UserOwnerMixin):
    template_name = 'accounts/profile-delete-page.html'
    model = UserModel
    success_url = reverse_lazy('index')

    def get(self, *args, **kwargs):
        user_id = kwargs['pk']

        if not user_is_owner(self.request, user_id):
            return redirect('delete user', pk=self.request.user.pk)

        return super().get(*args, **kwargs)


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'accounts/profile-change-password-page.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('index')

    def get(self, *args, **kwargs):
        user_id = kwargs['pk']

        if not user_is_owner(self.request, user_id):
            return redirect('password change', pk=self.request.user.pk)

        return super().get(*args, **kwargs)


# Asdf123!@