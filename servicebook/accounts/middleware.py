from django.shortcuts import redirect
from servicebook.accounts.models import Profile

# TODO: get profile info with user info
def connect_user_to_profile_by_id(get_response):
    def middleware(request, *args, **kwargs):
        if request.user.is_authenticated:
            profile = Profile.objects.filter(pk=request.user.id).get()
        print(get_response)
        return get_response(request, *args, **kwargs)

    return middleware

