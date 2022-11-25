from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views, get_user_model, login

from servicebook.accounts.forms import RegisterUserForm
from servicebook.accounts.models import Profile

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


class SignInView(auth_views.LoginView):
    template_name = 'accounts/login-page.html'
    success_url = reverse_lazy('index')

class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('index')


class UserDetailsView(views.DetailView):
    template_name = 'accounts/profile-details-page.html'
    model = UserModel

    profile = Profile.objects.get(pk=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_owner'] = self.request.user == self.object
        context['full_name'] = self.profile.get_full_name()

        return context


class UserEditView(views.UpdateView):
    template_name = 'accounts/profile-edit-page.html'
    model = UserModel
    fields = ('first_name', 'last_name', 'email',)

    def get_success_url(self):
        return reverse_lazy('details user', kwargs={
            'pk': self.request.user.pk,
        })


class UserDeleteView(views.DeleteView):
    template_name = 'accounts/profile-delete-page.html'
    model = UserModel
    success_url = reverse_lazy('index')
