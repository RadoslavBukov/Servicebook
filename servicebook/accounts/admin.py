from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model

from servicebook.accounts.forms import RegisterUserForm, EditUserForm
from servicebook.accounts.models import Profile

UserModel = get_user_model()

class UserProfileInline(admin.StackedInline):
    model = Profile

@admin.register(UserModel)
class AppUserAdmin(auth_admin.UserAdmin):
    ordering = ('email',)
    list_display = ['email', 'date_joined', 'last_login',]
    list_filter = ()
    # inlines = [UserProfileInline, ]
    form = EditUserForm
    add_form = RegisterUserForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'email',
                    'password',
                ),
            }),
        (
            'Permissions',
            {
                'fields': (
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (
            'Important dates',
            {
                'fields': (
                    'last_login',
                    'date_joined',
                ),
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        return super().get_form(request, obj, **kwargs)


admin.site.register(Profile)