from django.urls import path, include
from .signals import *

from servicebook.accounts.views import SignInView, RegisterView, SignOutView, \
    UserDetailsView, UserEditView, UserDeleteView, ChangePasswordView

urlpatterns = (
    path('login/', SignInView.as_view(), name='login user'),
    path('register/', RegisterView.as_view(), name='register user'),
    path('logout/', SignOutView.as_view(), name='logout user'),
    path('profile/<int:pk>/', include([
        path('', UserDetailsView.as_view(), name='details user'),
        path('change-password/', ChangePasswordView.as_view(), name='password change'),
        path('edit/', UserEditView.as_view(), name='edit user'),
        path('delete/', UserDeleteView.as_view(), name='delete user'),
        ])),
)
