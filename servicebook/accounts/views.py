from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views, get_user_model, login

from servicebook.cars.utils import user_is_owner
from servicebook.accounts.forms import RegisterUserForm, LoginForm
from servicebook.accounts.models import Profile
from servicebook.core.model_mixins import UserOwnerMixin

UserModel = get_user_model()


class RegisterView(views.CreateView):
    template_name = 'accounts/register-page.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class SignInView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'accounts/login-page.html'
    success_url = reverse_lazy('index')


class SignOutView(auth_views.LogoutView, LoginRequiredMixin):
    next_page = reverse_lazy('index')


class UserDetailsView(views.DetailView, LoginRequiredMixin, UserOwnerMixin):
    template_name = 'accounts/profile-details-page.html'
    model = UserModel

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