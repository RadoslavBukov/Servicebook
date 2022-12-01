import profile

from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views, get_user_model, login
from django.contrib.auth.decorators import login_required

from servicebook.accounts.forms import RegisterUserForm, EditUserForm
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


class SignOutView(auth_views.LogoutView, LoginRequiredMixin):
    next_page = reverse_lazy('index')


class UserDetailsView(views.DetailView, LoginRequiredMixin):
    template_name = 'accounts/profile-details-page.html'
    model = UserModel
    form_class = EditUserForm

    # profile = Profile.objects.filter(pk=object.id).get()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = Profile.objects.filter(pk=self.request.user).get()

        context['is_owner'] = self.request.user == self.object
        context['full_name'] = profile.get_full_name()
        context['date_of_birth'] = profile.date_of_birth
        context['profile_picture'] = profile.profile_picture

        return context


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


class UserDeleteView(views.DeleteView, LoginRequiredMixin):
    template_name = 'accounts/profile-delete-page.html'
    model = UserModel
    success_url = reverse_lazy('index')


# @login_required
def password_change(request, pk):
    user = request.user
    form = PasswordChangeForm(user)
    return render(request, 'accounts/profile-change-password-page.html', {'form': form})


#
# class UserPasswordChangeView(views.UpdateView):
#     model = UserModel
#     template_name = 'accounts/profile-change-password-page.html'
#     form = UserPasswordChangeForm
#     fields = ('password',)
#
#     # def get_context_data(self, *args, **kwargs):
#     #     data = super().get_context_data(**kwargs)
#     #     data['PasswordChangeForm'] = UserPasswordChangeForm(self.request.user)
#     #     return data
#     #
#     # def post(self, request, *args, **kwargs):
#     #     u = self.request.user
#     #     u.set_password(request.POST.get('id_new_password1'))
#     #     u.save()
#     #
#     #     return super().post(request, *args, **kwargs)
#     #
#     # def get_object(self):
#     #     return self.request.user
#
#     def get_success_url(self):
#         return reverse_lazy('details user', kwargs={
#             'pk': self.request.user.pk,
#         })
#
#     # def get_form_kwargs(self):
#     #     kwargs = super().get_form_kwargs()
#     #     kwargs['user'] = self.user
#     #     return kwargs


# Asdf123!@