from django.http import HttpResponseForbidden
from servicebook.cars.models import CarInfo

#TODO: user_is_owner decorator
def user_is_owner(func):
    def check_and_call(request, *args, **kwargs):
        #user = request.user
        #print user.id
        pk = kwargs["pk"]
        car = CarInfo.objects.get(pk=pk)
        if not (car.user.id == request.user.id):
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return check_and_call
