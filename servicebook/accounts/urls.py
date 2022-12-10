from django.urls import path, include
from .signals import *
from django.contrib.auth import views as auth_views

from servicebook.accounts.views import SignInView, RegisterView, SignOutView, \
    UserDetailsView, UserEditView, UserDeleteView, password_change

urlpatterns = (
    path('login/', SignInView.as_view(), name='login user'),
    path('register/', RegisterView.as_view(), name='register user'),
    path('logout/', SignOutView.as_view(), name='logout user'),
    path('profile/<int:pk>/', include([
        path('', UserDetailsView.as_view(), name='details user'),
        path('edit/', UserEditView.as_view(), name='edit user'),
        path('delete/', UserDeleteView.as_view(), name='delete user'),
        # path('change_password/', password_change, name='password change'),
        ])),
)
